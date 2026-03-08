"""
Sphinx extension: pyscript_editor
----------------------------------
Adds a ``.. py-editor::`` directive that renders a PyScript editor
wrapped in the same ``div.highlight.highlight-python`` structure that
Sphinx/Pygments produces, so it inherits your theme's code-block styling.

Usage in conf.py
----------------
    extensions = [..., "pyscript_editor"]

    # Optional global defaults (all overridable per-directive):
    pyscript_version  = "2026.2.1"          # PyScript release
    pyscript_env      = "shared"            # py-editor env attribute
    pyscript_config   = "pyscript.json"     # py-editor config attribute
    pyscript_mini_coi = "mini-coi.js"       # path to mini-coi shim;
                                            # set to "" to skip

Usage in .rst files
-------------------
Basic (uses global defaults from conf.py)::

    .. py-editor::

        import numpy as np
        print(np.__version__)

Override any option per block::

    .. py-editor::
        :env: isolated
        :config: other.json

        print("hello")

The ``mini-coi.js`` script and the PyScript stylesheet/module are injected
only once per page, no matter how many ``.. py-editor::`` directives appear.
"""

from __future__ import annotations

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


_HIDE_GUTTERS_JS = """
<script>
(function() {
    var observer = new MutationObserver(function() {
        document.querySelectorAll('py-editor').forEach(function(el) {
            el.querySelectorAll('*').forEach(function(child) {
                if (child.shadowRoot && !child.shadowRoot.querySelector('style.gutter-hide')) {
                    var style = document.createElement('style');
                    style.className = 'gutter-hide';
                    style.textContent = '.cm-gutters { display: none !important; }';
                    child.shadowRoot.appendChild(style);
                }
            });
        });
    });
    observer.observe(document.body, { childList: true, subtree: true });
})();
</script>
"""


def _head_html(mini_coi: str, version: str, hide_gutters: bool) -> str:
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
        "target": directives.unchanged,
    }

    def run(self) -> list[nodes.Node]:
        env = self.state.document.settings.env  # Sphinx BuildEnvironment
        cfg = env.config

        # ---- resolve options, falling back to conf.py values ----
        version = cfg.pyscript_version
        mini_coi = cfg.pyscript_mini_coi
        hide_gutters = cfg.pyscript_hide_gutters
        ed_env = self.options.get("env", cfg.pyscript_env)
        ed_cfg = self.options.get("config", cfg.pyscript_config)
        ed_target = self.options.get("target", None)

        result: list[nodes.Node] = []

        # ---- inject <head> assets once per document ----
        injected = getattr(env, _HEAD_KEY, set())
        if env.docname not in injected:
            result.append(_raw(_head_html(mini_coi, version, hide_gutters)))
            injected.add(env.docname)
            setattr(env, _HEAD_KEY, injected)

        # ---- emit config attr only on the first editor for each (page, env) ----
        # PyScript reads the config once per named environment; repeating it is harmless
        # but emitting it only on the first occurrence keeps the HTML clean.
        env_configs = getattr(env, _ENV_KEY, set())
        env_key = (env.docname, ed_env)
        if env_key not in env_configs:
            config_part = f' config="{ed_cfg}"' if ed_cfg else ""
            env_configs.add(env_key)
            setattr(env, _ENV_KEY, env_configs)
        else:
            config_part = ""

        # ---- build the editor HTML ----
        code = "\n".join(self.content)
        indented = "\n".join("    " + line for line in code.splitlines())

        editor_html = (
            '<div class="highlight highlight-python notranslate">\n'
            '<div class="highlight">\n'
            f'<script type="py-editor" env="{ed_env}"{config_part}>\n'
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

    app.add_directive("py-editor", PyEditorDirective)

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
