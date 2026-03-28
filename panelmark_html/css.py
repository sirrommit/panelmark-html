_BASE_CSS = """\
/* panelmark-html base styles
 *
 * All visual values are controlled by CSS custom properties.
 * Override any variable in your own stylesheet to theme the shell.
 *
 * Custom properties
 * -----------------
 * --pm-border-color        border / divider colour
 * --pm-border-width        thickness of all borders and dividers
 * --pm-gap                 gap between sibling panels (not used by default;
 *                          override to add spacing between panels)
 * --pm-radius              corner radius on panels
 * --pm-heading-font-weight heading font weight
 * --pm-panel-padding       padding inside panel body and heading
 */

:root {
  --pm-border-color: #888;
  --pm-border-width: 1px;
  --pm-gap: 0px;
  --pm-radius: 0px;
  --pm-heading-font-weight: bold;
  --pm-panel-padding: 0.5rem;
}

/* Shell container --------------------------------------------------------- */

.pm-shell {
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  overflow: hidden;
  font-family: monospace, monospace;
  font-size: 0.875rem;
  border: var(--pm-border-width) solid var(--pm-border-color);
  border-radius: var(--pm-radius);
}

/* Splits ------------------------------------------------------------------ */

.pm-split {
  display: flex;
  flex: 1 1 0;
  min-height: 0;
  min-width: 0;
  gap: var(--pm-gap);
}

.pm-split-h {
  flex-direction: column;
}

.pm-split-v {
  flex-direction: row;
}

/* Single-pixel dividers between sibling panels, without double borders */
.pm-split-h > * + * {
  border-top: var(--pm-border-width) solid var(--pm-border-color);
}

.pm-split-v > * + * {
  border-left: var(--pm-border-width) solid var(--pm-border-color);
}

/* Panels ------------------------------------------------------------------ */

.pm-panel {
  display: flex;
  flex-direction: column;
  flex: 1 1 0;
  min-height: 0;
  min-width: 0;
  box-sizing: border-box;
  overflow: hidden;
}

.pm-panel-heading {
  flex-shrink: 0;
  box-sizing: border-box;
  padding: 0.25rem var(--pm-panel-padding);
  font-weight: var(--pm-heading-font-weight);
  border-bottom: var(--pm-border-width) solid var(--pm-border-color);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.pm-panel-body {
  flex: 1 1 0;
  min-height: 0;
  box-sizing: border-box;
  padding: var(--pm-panel-padding);
  overflow: auto;
}
"""


def get_base_css() -> str:
    """Return the base CSS string for panelmark-html layouts.

    The returned string uses CSS custom properties (variables) for all
    visual values so that embedding applications can theme the shell
    without modifying this stylesheet.

    Suggested usage::

        # Inline in a document
        page = render_document(shell, title="My App")

        # Link an external copy
        page = render_document(shell, css_href="/static/panelmark.css")
        # then write get_base_css() to that path at build time

        # Embed in a fragment
        fragment = render_fragment(shell, include_css=True)
    """
    return _BASE_CSS
