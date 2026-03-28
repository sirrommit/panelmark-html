"""Snapshot-like structural tests.

These tests parse the rendered HTML and assert on element ordering and
nesting rather than individual attribute substrings.  They use only the
Python standard library (html.parser) so no extra test dependency is needed.
"""
from html.parser import HTMLParser
from panelmark import Shell
from panelmark.interactions.base import Interaction
from panelmark.draw import RenderContext, DrawCommand
from panelmark_html import render_fragment


# ---------------------------------------------------------------------------
# Minimal HTML element collector
# ---------------------------------------------------------------------------

class _ElementCollector(HTMLParser):
    """Collect every start tag as (tag, attrs_dict) in document order."""

    def __init__(self):
        super().__init__()
        self.elements: list[tuple[str, dict]] = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


def collect(html: str) -> list[tuple[str, dict]]:
    p = _ElementCollector()
    p.feed(html)
    return p.elements


def tags(elements) -> list[str]:
    return [tag for tag, _ in elements]


def by_class(elements, cls: str) -> list[dict]:
    """Return attrs of all elements whose class attribute contains *cls*."""
    return [
        attrs for _, attrs in elements
        if cls in attrs.get('class', '').split()
    ]


def by_attr(elements, attr: str, value: str) -> list[dict]:
    """Return attrs of all elements where attrs[attr] == value."""
    return [attrs for _, attrs in elements if attrs.get(attr) == value]


# ---------------------------------------------------------------------------
# Stub interaction
# ---------------------------------------------------------------------------

class _Stub(Interaction):
    def render(self, context: RenderContext, focused=False) -> list[DrawCommand]:
        return []
    def handle_key(self, key): return False, None
    def get_value(self): return None
    def set_value(self, value): pass


# ---------------------------------------------------------------------------
# Single-panel shell
# ---------------------------------------------------------------------------

SINGLE = """
|=====|
|{$main$}|
|=====|
"""


class TestSinglePanelStructure:
    def setup_method(self):
        self.elems = collect(render_fragment(Shell(SINGLE)))

    def test_outer_shell_is_first_element(self):
        assert tags(self.elems)[0] == 'div'
        assert 'pm-shell' in self.elems[0][1].get('class', '')

    def test_panel_section_present(self):
        panels = by_class(self.elems, 'pm-panel')
        assert len(panels) == 1

    def test_panel_has_region_hook(self):
        panels = by_class(self.elems, 'pm-panel')
        assert panels[0].get('data-pm-region') == 'main'
        assert panels[0].get('id') == 'pm-region-main'

    def test_panel_body_follows_panel(self):
        tag_list = tags(self.elems)
        section_idx = next(
            i for i, (t, a) in enumerate(self.elems)
            if t == 'section' and 'pm-panel' in a.get('class', '')
        )
        # body div must appear after the section open tag
        body_indices = [
            i for i, (t, a) in enumerate(self.elems)
            if t == 'div' and 'pm-panel-body' in a.get('class', '')
        ]
        assert any(i > section_idx for i in body_indices)

    def test_no_vertical_split_elements(self):
        # Single-column layout — no pm-split-v expected
        assert by_class(self.elems, 'pm-split-v') == []


# ---------------------------------------------------------------------------
# VSplit shell
# ---------------------------------------------------------------------------

VSPLIT = """
|=====|
|{$left$}|{$right$}|
|=====|
"""


class TestVSplitStructure:
    def setup_method(self):
        self.elems = collect(render_fragment(Shell(VSPLIT)))

    def test_split_v_present(self):
        assert by_class(self.elems, 'pm-split-v')

    def test_two_panels(self):
        assert len(by_class(self.elems, 'pm-panel')) == 2

    def test_split_comes_before_panels(self):
        tag_list = tags(self.elems)
        split_idx = next(
            i for i, (t, a) in enumerate(self.elems)
            if 'pm-split-v' in a.get('class', '')
        )
        panel_indices = [
            i for i, (t, a) in enumerate(self.elems)
            if 'pm-panel' in a.get('class', '').split()
        ]
        assert all(i > split_idx for i in panel_indices)

    def test_both_region_hooks_present(self):
        regions = [a.get('data-pm-region') for _, a in self.elems if 'data-pm-region' in a]
        assert 'left' in regions
        assert 'right' in regions


# ---------------------------------------------------------------------------
# HSplit shell
# ---------------------------------------------------------------------------

HSPLIT = """
|=====|
|{$top$}|
|=====|
|{$bottom$}|
|=====|
"""


class TestHSplitStructure:
    def setup_method(self):
        self.elems = collect(render_fragment(Shell(HSPLIT)))

    def test_split_h_present(self):
        assert by_class(self.elems, 'pm-split-h')

    def test_two_panels(self):
        assert len(by_class(self.elems, 'pm-panel')) == 2

    def test_top_region_before_bottom(self):
        regions = [
            a['data-pm-region']
            for _, a in self.elems
            if 'data-pm-region' in a
        ]
        assert regions.index('top') < regions.index('bottom')


# ---------------------------------------------------------------------------
# Nested shell (HSplit containing a VSplit)
# ---------------------------------------------------------------------------

NESTED = """
|=====|
|{$header$}|
|=====|
|{$left$}|{$right$}|
|=====|
"""


class TestNestedStructure:
    def setup_method(self):
        self.elems = collect(render_fragment(Shell(NESTED)))

    def test_has_both_split_types(self):
        assert by_class(self.elems, 'pm-split-h')
        assert by_class(self.elems, 'pm-split-v')

    def test_three_panels(self):
        assert len(by_class(self.elems, 'pm-panel')) == 3

    def test_header_before_left_and_right(self):
        regions = [
            a['data-pm-region']
            for _, a in self.elems
            if 'data-pm-region' in a
        ]
        assert regions.index('header') < regions.index('left')
        assert regions.index('header') < regions.index('right')

    def test_split_h_before_split_v(self):
        split_classes = [
            a.get('class', '')
            for t, a in self.elems
            if t == 'div' and 'pm-split' in a.get('class', '')
        ]
        h_idx = next(i for i, c in enumerate(split_classes) if 'pm-split-h' in c)
        v_idx = next(i for i, c in enumerate(split_classes) if 'pm-split-v' in c)
        assert h_idx < v_idx


# ---------------------------------------------------------------------------
# Heading structure
# ---------------------------------------------------------------------------

HEADING = """
|=====|
|{__Panel Title__ $region$}|
|=====|
"""


class TestHeadingStructure:
    def setup_method(self):
        self.elems = collect(render_fragment(Shell(HEADING)))

    def test_header_element_present(self):
        headers = [t for t, a in self.elems if t == 'header']
        assert headers

    def test_heading_class_present(self):
        assert by_class(self.elems, 'pm-panel-heading')

    def test_heading_before_body(self):
        heading_idx = next(
            i for i, (t, a) in enumerate(self.elems)
            if 'pm-panel-heading' in a.get('class', '')
        )
        body_idx = next(
            i for i, (t, a) in enumerate(self.elems)
            if 'pm-panel-body' in a.get('class', '')
        )
        assert heading_idx < body_idx

    def test_data_pm_heading_on_panel_element(self):
        panels = by_class(self.elems, 'pm-panel')
        headed = [a for a in panels if 'data-pm-heading' in a]
        assert len(headed) == 1
        assert headed[0]['data-pm-heading'] == 'Panel Title'

    def test_data_pm_heading_absent_when_no_heading(self):
        elems = collect(render_fragment(Shell(SINGLE)))
        panels = by_class(elems, 'pm-panel')
        assert all('data-pm-heading' not in a for a in panels)


# ---------------------------------------------------------------------------
# Interaction metadata ordering in attributes
# ---------------------------------------------------------------------------

LAYOUT = """
|=====|
|{$main$}|
|=====|
"""


class TestInteractionMetadataStructure:
    def test_all_three_attrs_on_same_element(self):
        shell = Shell(LAYOUT)
        shell.assign('main', _Stub())
        elems = collect(render_fragment(shell))
        panels = by_class(elems, 'pm-panel')
        assert len(panels) == 1
        attrs = panels[0]
        assert 'data-pm-interaction' in attrs
        assert 'data-pm-focusable' in attrs
        assert 'data-pm-focused' in attrs

    def test_empty_attr_on_same_element_as_region_hook(self):
        shell = Shell(LAYOUT)
        elems = collect(render_fragment(shell))
        panels = by_class(elems, 'pm-panel')
        assert panels[0].get('data-pm-empty') == 'true'
        assert panels[0].get('data-pm-region') == 'main'
