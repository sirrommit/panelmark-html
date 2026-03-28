"""panelmark-html — static HTML/CSS renderer for panelmark shells.

This package converts a panelmark Shell into an HTML document or fragment.
It does not handle browser events, network transport, or live interaction
state.  For a live web application, use panelmark-web, which builds on top
of this package.

Public API
----------
render_fragment(shell, *, include_css=False) -> str
render_document(shell, *, title="panelmark", css_href=None, extra_head="") -> str
get_base_css() -> str
HTMLRenderer
"""

from .renderer import HTMLRenderer
from .css import get_base_css


def render_fragment(shell, *, include_css: bool = False) -> str:
    """Return an HTML fragment for *shell*.

    Parameters
    ----------
    shell:
        A ``panelmark.Shell`` instance.
    include_css:
        If True, prepend a ``<style>`` block with the base CSS.
    """
    return HTMLRenderer().render_fragment(shell, include_css=include_css)


def render_document(shell, *, title: str = 'panelmark',
                    css_href: str | None = None,
                    extra_head: str = '') -> str:
    """Return a full HTML document for *shell*.

    Parameters
    ----------
    shell:
        A ``panelmark.Shell`` instance.
    title:
        Value for the ``<title>`` element.
    css_href:
        If provided, emit a ``<link>`` to this stylesheet instead of
        inlining the base CSS.
    extra_head:
        Optional raw HTML string appended inside ``<head>``.
    """
    return HTMLRenderer().render_document(
        shell, title=title, css_href=css_href, extra_head=extra_head
    )


__all__ = ['HTMLRenderer', 'render_fragment', 'render_document', 'get_base_css']
