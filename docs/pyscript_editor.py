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
    pyscript_version      = "2026.7.3"   # PyScript release tag
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
:placeholder: Path (relative to the docs source directory) to an image file
         shown inside the ``:target:`` div as a pre-rendered preview.
         Replaced when ``display(..., append=False)`` writes to the target.
         Requires ``:target:`` to also be set.
:setup:  If present, adds the ``setup`` attribute to the ``<script>`` tag.
         PyScript will run the code automatically when the environment
         initialises, without requiring the user to click Run.  The block
         is still rendered visually so readers can see and copy the code.

sphinx-gallery examples
-----------------------
When ``sphinx_gallery.gen_gallery`` is also enabled, every Python code block on
a generated gallery page becomes a live editor.  To add an example, put two
files in the examples directory (``examples/`` here):

``plot_<name>.py``
    An ordinary sphinx-gallery script (``# %%`` cells).  sphinx-gallery runs it
    natively at build time, so the page shows real output under each cell and
    the gallery card gets a thumbnail from its first figure.
``plot_<name>.pyscript.json``
    The PyScript config for that page's editors (all of a page's editors share
    one env, named after the example).  Its ``files`` map is also honoured
    natively: before sphinx-gallery runs, remote URLs are downloaded to their
    destination paths under the examples directory (gitignore them), so the
    script finds the same files in both places.  Prefer relative URLs
    (``"./data/x.bsp": "data/x.bsp"``) for files committed beside the example:
    they are copied next to the built page and fetched same-origin, which
    avoids CORS/COEP trouble entirely.

Things that differ between the two runtimes:

* ``from pyscript import display`` is stubbed natively.  Plot with
  ``display(fig, target="<id>", append=False)``: the cell's build-time output
  is wrapped in a ``<div id="<id>">`` that the live plot replaces.  Other
  cells' build-time output is hidden once the reader runs the cell.
* Editors on a page share one interpreter, so state carries between cells
  in the browser.  Natively, sphinx-gallery restores the working directory
  after every cell, so keep an ``os.chdir`` in the cell that needs it, and
  guard it (``if os.path.isdir(...)``) so a re-run in the browser still works.
* Pages live in a subdirectory, so ``mini-coi.js`` is referenced relative to
  the page's depth; without it the page is not cross-origin isolated.
* Cross-origin assets (e.g. map tiles) fail under ``mini-coi``'s COEP
  ``require-corp`` unless the host sends CORS/CORP headers.

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
import json
import os
import re
import shutil
import sys
import types
import urllib.request
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
_PLACEHOLDER_IMAGES_KEY = "pyscript_placeholder_images"


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


def _head_html(
    mini_coi: str, version: str, hide_gutters: bool, hide_env_label: bool
) -> str:
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


def _head_once(env) -> list[nodes.Node]:
    """The <head> assets as a raw node, or nothing if this page has them."""
    injected = getattr(env, _HEAD_KEY, set())
    if env.docname in injected:
        return []
    injected.add(env.docname)
    setattr(env, _HEAD_KEY, injected)
    cfg = env.config
    mini_coi = cfg.pyscript_mini_coi
    if mini_coi and "://" not in mini_coi and not mini_coi.startswith("/"):
        # mini-coi.js lives at the site root (html_extra_path); a page in a
        # subdirectory such as the gallery must reach back up to it, or the
        # service worker never registers and the page is not cross-origin
        # isolated.
        mini_coi = "../" * env.docname.count("/") + mini_coi
    return [
        _raw(
            _head_html(
                mini_coi,
                cfg.pyscript_version,
                cfg.pyscript_hide_gutters,
                cfg.pyscript_hide_env_label,
            )
        )
    ]


def _next_cell_id(env) -> str:
    # The counter is global across all documents in a build (matching how
    # Sphinx/Pygments numbers codecell0, codecell1, …).
    cell_num = getattr(env, _CELL_COUNTER_KEY, 0)
    setattr(env, _CELL_COUNTER_KEY, cell_num + 1)
    return f"pyscript-codecell{cell_num}"


def _editor_html(
    code: str, ed_env: str, config_part: str, ed_setup: bool, cell_id: str,
    has_target: bool, output_id: str | None = None,
) -> str:
    indented = "\n".join("    " + line for line in code.splitlines())

    # sphinx_copybutton looks for `div.highlight pre` and wires a copy
    # button to it via data-clipboard-target.  The <pre> is hidden
    # visually; clipboard.js reads textContent regardless of visibility.
    escaped_code = html_mod.escape(code)

    outer_classes = "highlight highlight-python notranslate"
    if has_target:
        outer_classes += " has-target"
    # output= is read by PyScript's py-editor (seen in the 2026.7.3 source, not
    # documented): it adopts that element as the editor's output area instead
    # of creating one.  Re-check it if pyscript_version is bumped.
    output_part = f' output="{output_id}"' if output_id else ""

    return (
        f'<div class="{outer_classes}">\n'
        '<div class="highlight">\n'
        f'<pre id="{cell_id}" style="display:none">{escaped_code}</pre>\n'
        f'<script type="py-editor" env="{ed_env}"{config_part}{output_part}{"  setup" if ed_setup else ""}>\n'
        f"{indented}\n"
        "</script>\n"
        "</div>\n"
        "</div>\n"
    )


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
        "placeholder": directives.unchanged,
        "setup": directives.flag,
    }

    def run(self) -> list[nodes.Node]:
        env = self.state.document.settings.env  # Sphinx BuildEnvironment
        cfg = env.config

        # ---- resolve options, falling back to conf.py values ----
        ed_env = self.options.get("env", cfg.pyscript_env)
        ed_cfg = self.options.get("config", cfg.pyscript_config)
        ed_src = self.options.get("src", None)
        ed_target = self.options.get("target", None)
        ed_placeholder = self.options.get("placeholder", None)
        ed_setup = "setup" in self.options

        if ed_placeholder and not ed_target:
            raise self.error(":placeholder: requires :target: to also be set")

        # ---- inject <head> assets once per document ----
        result: list[nodes.Node] = _head_once(env)

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
                raise self.error(
                    f":src: could not read file {abs_src!r}: {exc}"
                ) from exc
            env.note_dependency(abs_src)
        else:
            code = "\n".join(self.content)

        # Assign a unique ID so sphinx_copybutton can target the hidden <pre>.
        editor_html = _editor_html(
            code, ed_env, config_part, ed_setup, _next_cell_id(env), bool(ed_target)
        )
        if ed_target:
            if ed_placeholder:
                # Track the image so _copy_placeholder_images can copy it
                placeholders = getattr(env, _PLACEHOLDER_IMAGES_KEY, set())
                placeholders.add(ed_placeholder)
                setattr(env, _PLACEHOLDER_IMAGES_KEY, placeholders)

                depth = env.docname.count("/")
                img_src = "../" * depth + "_images/" + os.path.basename(ed_placeholder)
                escaped_src = html_mod.escape(img_src)
                editor_html += (
                    f'<div id="{ed_target}">'
                    f'<img src="{escaped_src}" alt="Pre-rendered output" />'
                    f"</div>\n"
                )
            else:
                editor_html += f'<div id="{ed_target}"></div>\n'

        result.append(_raw(editor_html))
        return result


# ---------------------------------------------------------------------------
# Copy placeholder images into the build output
# ---------------------------------------------------------------------------


def _copy_placeholder_images(app: Sphinx, exception: Exception | None) -> None:
    if exception:
        return
    placeholders = getattr(app.env, _PLACEHOLDER_IMAGES_KEY, set())
    if not placeholders:
        return
    img_dir = os.path.join(app.outdir, "_images")
    os.makedirs(img_dir, exist_ok=True)
    for src_rel in placeholders:
        src_abs = os.path.join(app.srcdir, src_rel)
        dest = os.path.join(img_dir, os.path.basename(src_rel))
        try:
            shutil.copy2(src_abs, dest)
        except OSError as exc:
            logger.warning(
                "pyscript_editor: cannot copy placeholder %r: %s", src_rel, exc
            )


# ---------------------------------------------------------------------------
# sphinx-gallery integration
# ---------------------------------------------------------------------------
#
# Gallery examples are plain sphinx-gallery scripts, executed natively at build
# time so their pages carry real output and their cards real thumbnails.  Each
# ``<stem>.py`` has a ``<stem>.pyscript.json`` beside it, which is both the
# PyScript config for the page's editors and, natively, the list of files the
# script expects to find relative to the examples directory (sphinx-gallery
# runs each example from there).  After parsing, every Python code block on a
# gallery page is swapped for a live editor.

_GALLERY_CONFIG_SUFFIX = ".pyscript.json"


def _gallery_dirs(app: Sphinx) -> list[tuple[str, str]]:
    """(examples_dir, gallery_dir) pairs from ``sphinx_gallery_conf``."""
    conf = getattr(app.config, "sphinx_gallery_conf", None) or {}
    examples = conf.get("examples_dirs", [])
    galleries = conf.get("gallery_dirs", [])
    if isinstance(examples, str):
        examples = [examples]
    if isinstance(galleries, str):
        galleries = [galleries]
    return list(zip(examples, galleries))


def _gallery_configs(app: Sphinx) -> list[tuple[str, str, str]]:
    """(examples_dir, gallery_dir, config filename) for every example config."""
    found = []
    for examples_dir, gallery_dir in _gallery_dirs(app):
        abs_dir = os.path.join(app.srcdir, examples_dir)
        if not os.path.isdir(abs_dir):
            continue
        for name in sorted(os.listdir(abs_dir)):
            if name.endswith(_GALLERY_CONFIG_SUFFIX):
                found.append((examples_dir, gallery_dir, name))
    return found


def _read_config(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _install_pyscript_stub() -> None:
    """Make ``from pyscript import display`` work in native gallery runs.

    The stub returns what it was given, so a cell ending in
    ``display(folium_map, ...)`` has the map as its last expression and
    sphinx-gallery renders its HTML repr.  matplotlib figures are scraped by
    sphinx-gallery on its own (their ``_repr_html_`` returns None).
    """
    try:
        import pyscript  # noqa: F401
    except ImportError:
        stub = types.ModuleType("pyscript")

        def display(*values, target=None, append=True):
            return values[0] if len(values) == 1 else None

        stub.display = display
        sys.modules["pyscript"] = stub


def _prefetch_gallery_files(app: Sphinx) -> None:
    """Fetch each example's PyScript ``files`` so it also runs natively.

    Runs on builder-inited ahead of sphinx-gallery, which executes the examples.
    Remote files are downloaded once and kept (they are build artifacts; keep
    them out of version control).  Relative URLs name files that already live
    in the examples directory and are served from the built gallery directory.
    """
    _install_pyscript_stub()
    for examples_dir, _, name in _gallery_configs(app):
        abs_dir = os.path.join(app.srcdir, examples_dir)
        files = _read_config(os.path.join(abs_dir, name)).get("files", {})
        for url, dest in files.items():
            abs_dest = os.path.join(abs_dir, dest)
            if os.path.exists(abs_dest):
                continue
            os.makedirs(os.path.dirname(abs_dest), exist_ok=True)
            if url.startswith(("http://", "https://")):
                logger.info("pyscript_editor: fetching %s", url)
                urllib.request.urlretrieve(url, abs_dest)
            else:
                shutil.copy2(os.path.join(abs_dir, url), abs_dest)


# Gallery pages show each cell's build-time output beneath its editor.  Running
# a cell hides that output (its live output appears in the editor instead);
# for cells that ``display(..., target=...)``, the output container *is* the
# target, so the live result simply replaces it.
_GALLERY_JS = """
<script>
document.addEventListener('click', function(e) {
    if (!e.target.closest('.py-editor-run-button')) return;
    var cell = e.target.closest('.highlight-python');
    var out = cell && cell.nextElementSibling;
    if (!out || !out.classList.contains('pyscript-build-output')) return;
    if (!out.id) {
        out.style.display = 'none';
    } else {
        // a display target stays visible for live plots; only its stale
        // build-time printed text goes
        out.querySelectorAll('.sphx-glr-script-out').forEach(function(el) {
            el.style.display = 'none';
        });
    }
}, true);
// Pages with inline output (pyscript_gallery_inline_output): PyScript moves an
// editor's output= element inside the editor box.  Put it back under the cell,
// where the build-time output was; PyScript keeps writing to the same element.
new MutationObserver(function() {
    document.querySelectorAll('.py-editor-box .pyscript-inline-output').forEach(function(out) {
        out.closest('.highlight-python').after(out);
    });
}).observe(document.documentElement, { childList: true, subtree: true });
</script>
"""

_DISPLAY_TARGET = re.compile(r"""display\([^)]*target\s*=\s*["']([^"']+)["']""")


def _is_build_output(node: nodes.Node) -> bool:
    """Is this one of the nodes sphinx-gallery emits for a cell's output?"""
    if type(node).__name__ == "imgsgnode":  # .. image-sg::
        return True
    if isinstance(node, nodes.raw):  # captured _repr_html_
        return "rendered_html" in node.astext()
    if isinstance(node, nodes.Element):  # stdout, multi-figure lists
        classes = node.get("classes", [])
        if "sphx-glr-timing" in classes:  # the page's "Total running time"
            return False
        return any(c.startswith("sphx-glr") for c in classes)
    return False


def _gallery_page(app: Sphinx, docname: str) -> tuple[str, str] | None:
    """(env name, config filename) if docname is a gallery example page."""
    for examples_dir, gallery_dir in _gallery_dirs(app):
        prefix = gallery_dir.rstrip("/") + "/"
        if not docname.startswith(prefix):
            continue
        stem = docname[len(prefix):]
        name = stem + _GALLERY_CONFIG_SUFFIX
        if os.path.exists(os.path.join(app.srcdir, examples_dir, name)):
            return os.path.basename(stem), os.path.basename(name)
    return None


def _convert_gallery_code(app: Sphinx, doctree: nodes.document) -> None:
    """Swap each Python code block on a gallery page for a live editor."""
    env = app.env
    page = _gallery_page(app, env.docname)
    if page is None:
        return
    ed_env, config = page
    config_part = f' config="{config}"'
    inline = app.config.pyscript_gallery_inline_output
    inline = inline is True or ed_env in (inline or ())
    for block in list(doctree.findall(nodes.literal_block)):
        if block.get("language", "").lower() != "python":
            continue
        parent = block.parent
        index = parent.index(block)
        outputs = []
        for sibling in parent.children[index + 1 :]:
            if isinstance(sibling, nodes.comment):
                continue
            if not _is_build_output(sibling):
                break
            outputs.append(sibling)

        for node in outputs:
            parent.remove(node)
        code = block.astext()
        targets = _DISPLAY_TARGET.findall(code)
        cell_id = _next_cell_id(env)
        replacement = _head_once(env)
        if len(replacement):
            replacement.append(_raw(_GALLERY_JS))
        replacement.append(
            _raw(
                _editor_html(
                    code, ed_env, config_part, False, cell_id, bool(targets),
                    output_id=f"{cell_id}-output" if inline else None,
                )
            )
        )
        config_part = ""  # PyScript reads the config once, from the first editor
        if inline:
            # printed text goes in the editor's own output box, which a run
            # clears and refills; figures go in their display target below it
            printed = [n for n in outputs if "sphx-glr-script-out" in n.get("classes", [])]
            outputs = [n for n in outputs if n not in printed]
            box = nodes.container(classes=["pyscript-inline-output"])
            box["ids"] = [f"{cell_id}-output"]
            box.extend(printed)
            replacement.append(box)
        if outputs or (inline and targets):
            container = nodes.container(classes=["pyscript-build-output"])
            if targets:
                container["ids"] = [targets[-1]]
            container.extend(outputs)
            replacement.append(container)
        parent.replace(block, replacement)


def _copy_gallery_files(app: Sphinx, exception: Exception | None) -> None:
    """Serve each example's config, and its same-origin files, beside its page."""
    if exception or app.builder.format != "html":
        return
    for examples_dir, gallery_dir, name in _gallery_configs(app):
        abs_dir = os.path.join(app.srcdir, examples_dir)
        out_dir = os.path.join(app.outdir, gallery_dir)
        os.makedirs(out_dir, exist_ok=True)
        shutil.copy2(os.path.join(abs_dir, name), out_dir)
        for url in _read_config(os.path.join(abs_dir, name)).get("files", {}):
            if url.startswith(("http://", "https://")):
                continue
            dest = os.path.join(out_dir, url)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(os.path.join(abs_dir, url), dest)


# ---------------------------------------------------------------------------
# Per-page state bookkeeping
# ---------------------------------------------------------------------------
#
# The once-per-page markers live on the build environment, which Sphinx
# pickles between builds.  A page that is re-read (edited, or regenerated by
# sphinx-gallery) must lose its markers first, or the incremental build emits
# it without the PyScript <head> assets or its config= attribute.


def _purge_doc(app: Sphinx, env, docname: str) -> None:
    injected = getattr(env, _HEAD_KEY, set())
    injected.discard(docname)
    for key in (_ENV_KEY, _SETUP_ENV_KEY):
        pairs = getattr(env, key, set())
        setattr(env, key, {pair for pair in pairs if pair[0] != docname})


def _merge_info(app: Sphinx, env, docnames, other) -> None:
    """Fold a parallel reader's markers back into the main environment."""
    for key in (_HEAD_KEY, _ENV_KEY, _SETUP_ENV_KEY, _PLACEHOLDER_IMAGES_KEY):
        merged = getattr(env, key, set()) | getattr(other, key, set())
        setattr(env, key, merged)


# ---------------------------------------------------------------------------
# Extension setup
# ---------------------------------------------------------------------------


def setup(app: Sphinx) -> dict:
    app.add_config_value("pyscript_version", "2026.7.3", "html")
    app.add_config_value("pyscript_env", "shared", "html")
    app.add_config_value("pyscript_config", "pyscript.json", "html")
    app.add_config_value("pyscript_mini_coi", "mini-coi.js", "html")
    app.add_config_value("pyscript_hide_gutters", True, "html")
    app.add_config_value("pyscript_hide_env_label", True, "html")
    # gallery examples (by file stem, or True for all) whose live output is
    # written into the box holding the build-time output, instead of PyScript's
    # nested output box
    app.add_config_value("pyscript_gallery_inline_output", [], "env")

    app.add_directive("py-editor", PyEditorDirective)
    app.connect("build-finished", _copy_placeholder_images)
    app.connect("env-purge-doc", _purge_doc)
    app.connect("env-merge-info", _merge_info)
    # sphinx-gallery generates its pages on builder-inited at the default
    # priority (500); the examples' files must be in place before that.
    app.connect("builder-inited", _prefetch_gallery_files, priority=400)
    app.connect("doctree-read", _convert_gallery_code)
    app.connect("build-finished", _copy_gallery_files)

    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
