"""Tests for Phase 3: base CSS content and integration with the renderer."""
from panelmark import Shell
from panelmark_html import get_base_css, render_fragment, render_document


SINGLE_PANEL = """
|=====|
|{$main$}|
|=====|
"""


class TestGetBaseCss:
    def test_returns_nonempty_string(self):
        css = get_base_css()
        assert isinstance(css, str)
        assert len(css) > 0

    # Required selectors
    def test_contains_pm_shell(self):
        assert '.pm-shell' in get_base_css()

    def test_contains_pm_split(self):
        assert '.pm-split' in get_base_css()

    def test_contains_pm_split_h(self):
        assert '.pm-split-h' in get_base_css()

    def test_contains_pm_split_v(self):
        assert '.pm-split-v' in get_base_css()

    def test_contains_pm_panel(self):
        assert '.pm-panel' in get_base_css()

    def test_contains_pm_panel_heading(self):
        assert '.pm-panel-heading' in get_base_css()

    def test_contains_pm_panel_body(self):
        assert '.pm-panel-body' in get_base_css()

    # Required CSS custom properties
    def test_variable_border_color(self):
        assert '--pm-border-color' in get_base_css()

    def test_variable_border_width(self):
        assert '--pm-border-width' in get_base_css()

    def test_variable_gap(self):
        assert '--pm-gap' in get_base_css()

    def test_variable_radius(self):
        assert '--pm-radius' in get_base_css()

    def test_variable_heading_font_weight(self):
        assert '--pm-heading-font-weight' in get_base_css()

    def test_variable_panel_padding(self):
        assert '--pm-panel-padding' in get_base_css()

    # Flexbox layout
    def test_shell_uses_flexbox(self):
        assert 'display: flex' in get_base_css()

    def test_split_h_is_column(self):
        assert 'flex-direction: column' in get_base_css()

    def test_split_v_is_row(self):
        assert 'flex-direction: row' in get_base_css()

    # Dividers use sibling combinator (no double borders)
    def test_hsplit_divider_rule(self):
        assert '.pm-split-h > * + *' in get_base_css()

    def test_vsplit_divider_rule(self):
        assert '.pm-split-v > * + *' in get_base_css()


class TestCssIntegration:
    def test_render_fragment_include_css_adds_style_block(self):
        html = render_fragment(Shell(SINGLE_PANEL), include_css=True)
        assert '<style>' in html
        assert '.pm-shell' in html

    def test_render_fragment_no_css_by_default(self):
        html = render_fragment(Shell(SINGLE_PANEL))
        assert '<style>' not in html

    def test_render_document_inlines_css_by_default(self):
        doc = render_document(Shell(SINGLE_PANEL))
        assert '<style>' in doc
        assert '.pm-shell' in doc

    def test_render_document_css_href_skips_inline(self):
        doc = render_document(Shell(SINGLE_PANEL), css_href='/static/pm.css')
        assert 'href="/static/pm.css"' in doc
        assert '<style>' not in doc
