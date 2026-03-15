"""
Sphinx extension: pyscript_editor
----------------------------------
Adds a ``.. py-editor::`` directive that renders a PyScript editor
wrapped in the same ``div.highlight.highlight-python`` structure that
Sphinx/Pygments produces, so it inherits your theme's code-block styling.

The hidden ``<pre>`` inside each editor div is compatible with
``sphinx_copybutton``: that extension's JS selector finds ``div.highlight pre``
and wires a clipboard copy button automatically.

Usage in conf.py
----------------
    extensions = [..., "pyscript_editor"]

    # Optional global defaults (all overridable per-directive):
    pyscript_version      = "2026.2.1"   # PyScript release tag
    pyscript_env          = "shared"     # default py-editor env name
    pyscript_config       = "pyscript.json"  # default PyScript config file;
                                             # set to "" to omit
    pyscript_mini_coi     = "mini-coi.js"   # path to mini-coi shim;
                                             # set to "" to skip
    pyscript_hide_gutters  = True        # hide CodeMirror line-number gutters
    pyscript_hide_env_label = True       # hide the "pyodide-<env>" label
                                         # rendered above each editor box

Usage in .rst files
-------------------
Basic (uses global defaults from conf.py)::

    .. py-editor::

        import numpy as np
        print(np.__version__)

Override any option per block::

    .. py-editor::
        :env: myenv
        :config: my_pyscript.json

        print("hello")

Directive options
-----------------
:env:    PyScript environment name (``env=`` attribute on ``<script
         type="py-editor">``).  All editors sharing the same ``env`` on a page
         run in the same Python interpreter session.
:config: Path to a PyScript JSON config file.  **Required when** ``:setup:``
         **is used** — the setup block owns configuration for its env and must
         declare it explicitly.  For non-setup editors, ``config=`` is emitted
         only if no setup block has already claimed the env; otherwise it is
         omitted entirely.  PyScript reads the config once per named environment.
:src:    Path (relative to the docs source directory) to an external ``.py``
         file whose contents are read at build time and inlined into the
         editor.  The directive body is ignored when ``:src:`` is given.
         Sphinx will rebuild the page automatically when the file changes.
:target: If given, an empty ``<div id="<value>">`` is appended after the
         editor, useful as a display target for PyScript output.
:setup:  If present, adds the ``setup`` attribute to the ``<script>`` tag.
         PyScript will run the code automatically when the environment
         initialises, without requiring the user to click Run.  The block
         is still rendered visually so readers can see and copy the code.

Notes
-----
* The ``mini-coi.js`` shim, PyScript stylesheet, and ``core.js`` module are
  injected once per page regardless of how many ``.. py-editor::`` directives
  appear.
* Each editor receives a unique ``pyscript-codecellN`` id (build-global counter,
  consistent with Sphinx/Pygments ``codecell0``, ``codecell1``, … naming).
"""

from __future__ import annotations

import html as html_mod
import os
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.application import Sphinx
from sphinx.util import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Raw-HTML node helpers
# ---------------------------------------------------------------------------


def _raw(html: str) -> nodes.raw:
    return nodes.raw("", html, format="html")


# ---------------------------------------------------------------------------
# One-per-page head injection (idempotent via env metadata)
# ---------------------------------------------------------------------------

_HEAD_KEY = "pyscript_head_injected"
_ENV_KEY = "pyscript_env_config_registered"
_SETUP_ENV_KEY = "pyscript_setup_env_registered"
_CELL_COUNTER_KEY = "pyscript_cell_counter"


_HIDE_ENV_LABEL_CSS = """\
<style>.py-editor-box::before { display: none !important; }</style>
"""



_HIDE_GUTTERS_JS = """
<script>
(function() {
    var observer = new MutationObserver(function() {
        document.querySelectorAll('py-editor').forEach(function(el) {
            el.querySelectorAll('*').forEach(function(child) {
                if (child.shadowRoot && !child.shadowRoot.querySelector('style.gutter-hide')) {
                    var style = document.createElement('style');
                    style.className = 'gutter-hide';
                    style.textContent = '.cm-gutters { display: none !important; } .cm-content { min-height: 60px; }';
                    child.shadowRoot.appendChild(style);
                }
            });
        });
    });
    observer.observe(document.body, { childList: true, subtree: true });
})();
</script>
"""


def _head_html(mini_coi: str, version: str, hide_gutters: bool, hide_env_label: bool) -> str:
    parts = []
    if mini_coi:
        parts.append(f'<script src="{mini_coi}"></script>')
    parts.append(
        f'<link rel="stylesheet" '
        f'href="https://pyscript.net/releases/{version}/core.css" />'
    )
    parts.append(
        f'<script type="module" '
        f'src="https://pyscript.net/releases/{version}/core.js"></script>'
    )
    if hide_env_label:
        parts.append(_HIDE_ENV_LABEL_CSS)
    if hide_gutters:
        parts.append(_HIDE_GUTTERS_JS)
    return "\n".join(parts) + "\n"


# ---------------------------------------------------------------------------
# Directive
# ---------------------------------------------------------------------------


class PyEditorDirective(Directive):
    """``.. py-editor::`` directive."""

    has_content = True
    optional_arguments = 0
    option_spec = {
        "env": directives.unchanged,
        "config": directives.unchanged,
        "src": directives.unchanged,
        "target": directives.unchanged,
        "setup": directives.flag,
    }

    def run(self) -> list[nodes.Node]:
        env = self.state.document.settings.env  # Sphinx BuildEnvironment
        cfg = env.config

        # ---- resolve options, falling back to conf.py values ----
        version = cfg.pyscript_version
        mini_coi = cfg.pyscript_mini_coi
        hide_gutters = cfg.pyscript_hide_gutters
        hide_env_label = cfg.pyscript_hide_env_label
        ed_env = self.options.get("env", cfg.pyscript_env)
        ed_cfg = self.options.get("config", cfg.pyscript_config)
        ed_src = self.options.get("src", None)
        ed_target = self.options.get("target", None)
        ed_setup = "setup" in self.options

        result: list[nodes.Node] = []

        # ---- inject <head> assets once per document ----
        injected = getattr(env, _HEAD_KEY, set())
        if env.docname not in injected:
            result.append(_raw(_head_html(mini_coi, version, hide_gutters, hide_env_label)))
            injected.add(env.docname)
            setattr(env, _HEAD_KEY, injected)

        # ---- emit config= exactly once per (page, env) pair ----
        # Setup blocks own config for their env and must declare it explicitly.
        # Regular blocks get config= only if no setup block has claimed the env.
        if ed_setup and "config" not in self.options:
            raise self.error(":setup: requires :config: to be explicitly specified")

        setup_envs = getattr(env, _SETUP_ENV_KEY, set())
        env_configs = getattr(env, _ENV_KEY, set())
        env_key = (env.docname, ed_env)
        if ed_setup:
            config_part = f' config="{ed_cfg}"'
            setup_envs.add(env_key)
            env_configs.add(env_key)
            setattr(env, _SETUP_ENV_KEY, setup_envs)
            setattr(env, _ENV_KEY, env_configs)
        elif env_key not in setup_envs and env_key not in env_configs:
            config_part = f' config="{ed_cfg}"' if ed_cfg else ""
            env_configs.add(env_key)
            setattr(env, _ENV_KEY, env_configs)
        else:
            config_part = ""

        # ---- build the editor HTML ----
        if ed_src:
            abs_src = os.path.join(env.srcdir, ed_src)
            try:
                with open(abs_src, encoding="utf-8") as fh:
                    code = fh.read()
            except OSError as exc:
                raise self.error(f":src: could not read file {abs_src!r}: {exc}") from exc
            env.note_dependency(abs_src)
        else:
            code = "\n".join(self.content)
        indented = "\n".join("    " + line for line in code.splitlines())

        # Assign a unique ID so sphinx_copybutton can target the hidden <pre>.
        # The counter is global across all documents in a build (matching how
        # Sphinx/Pygments numbers codecell0, codecell1, …).
        cell_num = getattr(env, _CELL_COUNTER_KEY, 0)
        cell_id = f"pyscript-codecell{cell_num}"
        setattr(env, _CELL_COUNTER_KEY, cell_num + 1)

        # sphinx_copybutton looks for `div.highlight pre` and wires a copy
        # button to it via data-clipboard-target.  The <pre> is hidden
        # visually; clipboard.js reads textContent regardless of visibility.
        escaped_code = html_mod.escape(code)

        editor_html = (
            '<div class="highlight highlight-python notranslate">\n'
            '<div class="highlight">\n'
            f'<pre id="{cell_id}" style="display:none">{escaped_code}</pre>\n'
            f'<script type="py-editor" env="{ed_env}"{config_part}{"  setup" if ed_setup else ""}>\n'
            f"{indented}\n"
            "</script>\n"
            "</div>\n"
            "</div>\n"
        )
        if ed_target:
            editor_html += f'<div id="{ed_target}"></div>\n'

        result.append(_raw(editor_html))
        return result


# ---------------------------------------------------------------------------
# Extension setup
# ---------------------------------------------------------------------------


def setup(app: Sphinx) -> dict:
    app.add_config_value("pyscript_version", "2026.2.1", "html")
    app.add_config_value("pyscript_env", "shared", "html")
    app.add_config_value("pyscript_config", "pyscript.json", "html")
    app.add_config_value("pyscript_mini_coi", "mini-coi.js", "html")
    app.add_config_value("pyscript_hide_gutters", True, "html")
    app.add_config_value("pyscript_hide_env_label", True, "html")

    app.add_directive("py-editor", PyEditorDirective)

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
