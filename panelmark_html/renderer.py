from html import escape

from panelmark.layout import HSplit, VSplit, Panel

from .css import get_base_css


class HTMLRenderer:
    """Converts a panelmark Shell into an HTML fragment or full document.

    Phase 2 scope: structural rendering only — splits, panels, headings, and
    stable DOM hooks.  Interaction metadata hooks are added in Phase 4.
    CSS rules are provided by get_base_css() (Phase 3).
    """

    def render_fragment(self, shell, *, include_css: bool = False) -> str:
        """Return an HTML fragment for *shell*.

        Parameters
        ----------
        shell:
            A ``panelmark.Shell`` instance.
        include_css:
            If True, prepend a ``<style>`` block with the base CSS.
        """
        parts = []
        if include_css:
            css = get_base_css()
            if css:
                parts.append(f'<style>\n{css}\n</style>\n')
        parts.append(self._render_shell(shell))
        return ''.join(parts)

    def render_document(self, shell, *, title: str = 'panelmark',
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
            Optional raw HTML string appended inside ``<head>`` before
            ``</head>``.
        """
        head_lines = [
            '    <meta charset="UTF-8">',
            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f'    <title>{escape(title)}</title>',
        ]
        if css_href:
            head_lines.append(
                f'    <link rel="stylesheet" href="{escape(css_href, quote=True)}">'
            )
        else:
            css = get_base_css()
            if css:
                head_lines.append(f'    <style>\n{css}\n    </style>')
        if extra_head:
            head_lines.append(f'    {extra_head}')

        head = '\n'.join(head_lines)
        fragment = self._render_shell(shell)

        return (
            '<!DOCTYPE html>\n'
            '<html lang="en">\n'
            '<head>\n'
            f'{head}\n'
            '</head>\n'
            '<body>\n'
            f'{fragment}'
            '</body>\n'
            '</html>\n'
        )

    # ------------------------------------------------------------------
    # Internal rendering
    # ------------------------------------------------------------------

    def _render_shell(self, shell) -> str:
        node = shell.layout.root
        if node is None:
            return '<div class="pm-shell" data-pm-shell></div>\n'
        inner = self._render_node(node, indent=2)
        return f'<div class="pm-shell" data-pm-shell>\n{inner}</div>\n'

    def _render_node(self, node, indent: int = 0) -> str:
        if node is None:
            return ''
        pad = ' ' * indent

        if isinstance(node, Panel):
            return self._render_panel(node, indent)

        if isinstance(node, VSplit):
            left = self._render_node(node.left, indent + 2)
            right = self._render_node(node.right, indent + 2)
            return (
                f'{pad}<div class="pm-split pm-split-v">\n'
                f'{left}'
                f'{right}'
                f'{pad}</div>\n'
            )

        if isinstance(node, HSplit):
            top = self._render_node(node.top, indent + 2)
            bottom = self._render_node(node.bottom, indent + 2)
            return (
                f'{pad}<div class="pm-split pm-split-h">\n'
                f'{top}'
                f'{bottom}'
                f'{pad}</div>\n'
            )

        return ''

    def _render_panel(self, node: Panel, indent: int = 0) -> str:
        pad = ' ' * indent
        inner = ' ' * (indent + 2)

        attrs = ['class="pm-panel"']
        if node.name:
            attrs.append(f'data-pm-region="{escape(node.name, quote=True)}"')
            attrs.append('data-pm-kind="panel"')
            attrs.append(f'id="pm-region-{escape(node.name, quote=True)}"')

        lines = [f'{pad}<section {" ".join(attrs)}>\n']

        if node.heading:
            lines.append(
                f'{inner}<header class="pm-panel-heading">'
                f'{escape(node.heading)}'
                f'</header>\n'
            )

        lines.append(f'{inner}<div class="pm-panel-body"></div>\n')
        lines.append(f'{pad}</section>\n')

        return ''.join(lines)
