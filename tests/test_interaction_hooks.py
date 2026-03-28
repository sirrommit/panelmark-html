"""Tests for Phase 4: interaction metadata hooks.

A minimal stub Interaction is defined here so the tests have no dependency
on panelmark-tui or any other renderer package.
"""
import pytest
from panelmark import Shell
from panelmark.interactions.base import Interaction
from panelmark.draw import RenderContext, DrawCommand
from panelmark_html import render_fragment


# ---------------------------------------------------------------------------
# Minimal stub interactions
# ---------------------------------------------------------------------------

class FocusableInteraction(Interaction):
    """Focusable stub — is_focusable returns True (the default)."""

    def render(self, context: RenderContext, focused: bool = False) -> list[DrawCommand]:
        return []

    def handle_key(self, key) -> tuple:
        return False, None

    def get_value(self):
        return None

    def set_value(self, value) -> None:
        pass


class NonFocusableInteraction(Interaction):
    """Non-focusable stub — is_focusable returns False."""

    @property
    def is_focusable(self) -> bool:
        return False

    def render(self, context: RenderContext, focused: bool = False) -> list[DrawCommand]:
        return []

    def handle_key(self, key) -> tuple:
        return False, None

    def get_value(self):
        return None

    def set_value(self, value) -> None:
        pass


LAYOUT = """
|=====|
|{$main$}|
|=====|
"""

TWO_PANEL = """
|=====|
|{$left$}|{$right$}|
|=====|
"""

THREE_PANEL = """
|=====|
|{$top$}|
|=====|
|{$left$}|{$right$}|
|=====|
"""


# ---------------------------------------------------------------------------
# data-pm-empty on panels with no interaction
# ---------------------------------------------------------------------------

class TestEmptyPanel:
    def test_unassigned_named_panel_gets_empty_attr(self):
        html = render_fragment(Shell(LAYOUT))
        assert 'data-pm-empty="true"' in html

    def test_assigned_panel_does_not_get_empty_attr(self):
        shell = Shell(LAYOUT)
        shell.assign('main', FocusableInteraction())
        html = render_fragment(shell)
        assert 'data-pm-empty' not in html

    def test_one_assigned_one_unassigned(self):
        shell = Shell(TWO_PANEL)
        shell.assign('left', FocusableInteraction())
        html = render_fragment(shell)
        # right is unassigned → empty
        assert 'data-pm-empty="true"' in html
        # left is assigned → no empty attr on that section
        # both regions present
        assert 'pm-region-left' in html
        assert 'pm-region-right' in html


TWO_PANEL = """
|=====|
|{$left$}|{$right$}|
|=====|
"""


# ---------------------------------------------------------------------------
# data-pm-interaction
# ---------------------------------------------------------------------------

class TestInteractionAttr:
    def test_class_name_present(self):
        shell = Shell(LAYOUT)
        shell.assign('main', FocusableInteraction())
        html = render_fragment(shell)
        assert 'data-pm-interaction=' in html

    def test_qualified_class_name(self):
        shell = Shell(LAYOUT)
        interaction = FocusableInteraction()
        shell.assign('main', interaction)
        html = render_fragment(shell)
        cls = type(interaction)
        expected = f'{cls.__module__}.{cls.__qualname__}'
        assert f'data-pm-interaction="{expected}"' in html

    def test_no_interaction_attr_when_unassigned(self):
        html = render_fragment(Shell(LAYOUT))
        assert 'data-pm-interaction' not in html


# ---------------------------------------------------------------------------
# data-pm-focusable
# ---------------------------------------------------------------------------

class TestFocusableAttr:
    def test_focusable_true(self):
        shell = Shell(LAYOUT)
        shell.assign('main', FocusableInteraction())
        html = render_fragment(shell)
        assert 'data-pm-focusable="true"' in html

    def test_focusable_false(self):
        shell = Shell(LAYOUT)
        shell.assign('main', NonFocusableInteraction())
        html = render_fragment(shell)
        assert 'data-pm-focusable="false"' in html


# ---------------------------------------------------------------------------
# data-pm-focused
# ---------------------------------------------------------------------------

class TestFocusedAttr:
    def test_focused_false_when_no_focus_set(self):
        shell = Shell(LAYOUT)
        shell.assign('main', FocusableInteraction())
        html = render_fragment(shell)
        assert 'data-pm-focused="false"' in html

    def test_focused_true_when_focus_set(self):
        shell = Shell(LAYOUT)
        shell.assign('main', FocusableInteraction())
        shell.set_focus('main')
        html = render_fragment(shell)
        assert 'data-pm-focused="true"' in html

    def test_only_focused_panel_is_true(self):
        shell = Shell(TWO_PANEL)
        shell.assign('left', FocusableInteraction())
        shell.assign('right', FocusableInteraction())
        shell.set_focus('left')
        html = render_fragment(shell)
        # Count occurrences
        assert html.count('data-pm-focused="true"') == 1
        assert html.count('data-pm-focused="false"') == 1

    def test_focused_false_for_non_focusable(self):
        shell = Shell(LAYOUT)
        shell.assign('main', NonFocusableInteraction())
        # Non-focusable interaction can't receive focus via set_focus
        html = render_fragment(shell)
        assert 'data-pm-focused="false"' in html


# ---------------------------------------------------------------------------
# Panel body is always empty
# ---------------------------------------------------------------------------

class TestEmptyBody:
    def test_body_empty_when_no_interaction(self):
        html = render_fragment(Shell(LAYOUT))
        assert '<div class="pm-panel-body"></div>' in html

    def test_body_empty_when_interaction_assigned(self):
        shell = Shell(LAYOUT)
        shell.assign('main', FocusableInteraction())
        html = render_fragment(shell)
        assert '<div class="pm-panel-body"></div>' in html
