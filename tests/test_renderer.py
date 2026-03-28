"""Structural tests for the Phase 2 HTML renderer.

Tests assert on HTML substrings and attribute presence.  No external HTML
parser is used; all checks stay within the Python standard library.
"""
import pytest
from panelmark import Shell
from panelmark_html import render_fragment, render_document, HTMLRenderer


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

SINGLE_PANEL = """
|=====|
|{$main$}|
|=====|
"""

VSPLIT = """
|=====|
|{$left$}|{$right$}|
|=====|
"""

HSPLIT = """
|=====|
|{$top$}|
|=====|
|{$bottom$}|
|=====|
"""

NESTED = """
|=====|
|{$header$}|
|=====|
|{$left$}|{$right$}|
|=====|
"""

HEADING = """
|=====|
|{__My Heading__ $region$}|
|=====|
"""


# ---------------------------------------------------------------------------
# Outer shell wrapper
# ---------------------------------------------------------------------------

class TestShellWrapper:
    def test_outer_class(self):
        html = render_fragment(Shell(SINGLE_PANEL))
        assert 'class="pm-shell"' in html

    def test_outer_data_attribute(self):
        html = render_fragment(Shell(SINGLE_PANEL))
        assert 'data-pm-shell' in html

    def test_empty_layout(self):
        html = render_fragment(Shell(""))
        assert 'pm-shell' in html


# ---------------------------------------------------------------------------
# Named panel hooks
# ---------------------------------------------------------------------------

class TestPanelHooks:
    def test_id_attribute(self):
        html = render_fragment(Shell(SINGLE_PANEL))
        assert 'id="pm-region-main"' in html

    def test_data_pm_region(self):
        html = render_fragment(Shell(SINGLE_PANEL))
        assert 'data-pm-region="main"' in html

    def test_data_pm_kind(self):
        html = render_fragment(Shell(SINGLE_PANEL))
        assert 'data-pm-kind="panel"' in html

    def test_panel_body_container(self):
        html = render_fragment(Shell(SINGLE_PANEL))
        assert 'class="pm-panel-body"' in html

    def test_panel_section_element(self):
        html = render_fragment(Shell(SINGLE_PANEL))
        assert '<section' in html


# ---------------------------------------------------------------------------
# Headings
# ---------------------------------------------------------------------------

class TestHeadings:
    def test_heading_element(self):
        html = render_fragment(Shell(HEADING))
        assert 'class="pm-panel-heading"' in html

    def test_heading_text(self):
        html = render_fragment(Shell(HEADING))
        assert 'My Heading' in html

    def test_no_heading_element_when_absent(self):
        html = render_fragment(Shell(SINGLE_PANEL))
        assert 'pm-panel-heading' not in html

    def test_data_pm_heading_attribute(self):
        html = render_fragment(Shell(HEADING))
        assert 'data-pm-heading="My Heading"' in html

    def test_no_data_pm_heading_when_absent(self):
        html = render_fragment(Shell(SINGLE_PANEL))
        assert 'data-pm-heading' not in html


# ---------------------------------------------------------------------------
# Split structure
# ---------------------------------------------------------------------------

class TestVSplit:
    def test_vsplit_class(self):
        html = render_fragment(Shell(VSPLIT))
        assert 'pm-split-v' in html

    def test_vsplit_contains_both_regions(self):
        html = render_fragment(Shell(VSPLIT))
        assert 'pm-region-left' in html
        assert 'pm-region-right' in html


class TestHSplit:
    def test_hsplit_class(self):
        html = render_fragment(Shell(HSPLIT))
        assert 'pm-split-h' in html

    def test_hsplit_contains_both_regions(self):
        html = render_fragment(Shell(HSPLIT))
        assert 'pm-region-top' in html
        assert 'pm-region-bottom' in html


class TestNested:
    def test_nested_all_regions_present(self):
        html = render_fragment(Shell(NESTED))
        assert 'pm-region-header' in html
        assert 'pm-region-left' in html
        assert 'pm-region-right' in html

    def test_nested_has_both_split_types(self):
        html = render_fragment(Shell(NESTED))
        assert 'pm-split-h' in html
        assert 'pm-split-v' in html


# ---------------------------------------------------------------------------
# render_document
# ---------------------------------------------------------------------------

class TestRenderDocument:
    def test_doctype(self):
        doc = render_document(Shell(SINGLE_PANEL))
        assert doc.startswith('<!DOCTYPE html>')

    def test_default_title(self):
        doc = render_document(Shell(SINGLE_PANEL))
        assert '<title>panelmark</title>' in doc

    def test_custom_title(self):
        doc = render_document(Shell(SINGLE_PANEL), title='My App')
        assert '<title>My App</title>' in doc

    def test_title_is_escaped(self):
        doc = render_document(Shell(SINGLE_PANEL), title='<evil>')
        assert '<title>&lt;evil&gt;</title>' in doc

    def test_css_href(self):
        doc = render_document(Shell(SINGLE_PANEL), css_href='/static/pm.css')
        assert 'href="/static/pm.css"' in doc
        assert '<style>' not in doc

    def test_fragment_present_in_document(self):
        doc = render_document(Shell(SINGLE_PANEL))
        assert 'pm-region-main' in doc

    def test_extra_head(self):
        doc = render_document(Shell(SINGLE_PANEL), extra_head='<meta name="robots" content="noindex">')
        assert 'noindex' in doc
