# panelmark-html Hook Contract

This document defines the stable interface between `panelmark-html` and
`panelmark-web`.  It specifies which parts of the rendered HTML are stable
API that `panelmark-web` may depend on, and which parts are presentation
details subject to change.

---

## Stability classes

| Label | Meaning |
|-------|---------|
| **Stable** | Will not change without a major version bump.  `panelmark-web` may hard-depend on these. |
| **Stable / additive** | New values may be added in minor versions; existing values will not change. |
| **Presentation** | Internal rendering detail.  May change in any release.  Do not depend on these. |

---

## Shell root element

Every rendered shell is wrapped in a single root element.

```html
<div class="pm-shell" data-pm-shell>
  ...
</div>
```

| Part | Stability |
|------|-----------|
| `class="pm-shell"` | **Stable** |
| `data-pm-shell` (boolean attribute, no value) | **Stable** |
| Element tag (`div`) | Presentation |

`panelmark-web` should locate the shell root via `[data-pm-shell]` or
`.pm-shell`, not by tag name.

---

## Split containers

Horizontal and vertical splits are rendered as `div` elements with two
CSS classes.

```html
<div class="pm-split pm-split-h"> ... </div>  <!-- stacked / column -->
<div class="pm-split pm-split-v"> ... </div>  <!-- side-by-side / row -->
```

| Part | Stability |
|------|-----------|
| `class="pm-split"` | **Stable** |
| `class="pm-split-h"` | **Stable** — column (stacked) layout |
| `class="pm-split-v"` | **Stable** — row (side-by-side) layout |
| Element tag (`div`) | Presentation |
| Exact nesting depth and order | Presentation — may be optimised in future releases |

Split containers are structural scaffolding.  `panelmark-web` should not
attach behavior to them directly; use panel-level hooks instead.  The class
semantics (`.pm-split-h` = column, `.pm-split-v` = row) are stable, but the
exact tree of nested split elements is not part of the API contract.

---

## Panel elements

Each named region in the shell definition is rendered as a `section`
element.

```html
<section
  class="pm-panel"
  data-pm-region="sidebar"
  data-pm-kind="panel"
  id="pm-region-sidebar"
  data-pm-heading="Sidebar"    <!-- when a heading is defined -->
  data-pm-empty="true"         <!-- when no interaction is assigned -->
>
  <header class="pm-panel-heading">Sidebar</header>   <!-- if heading defined -->
  <div class="pm-panel-body"></div>
</section>
```

### Panel-level hooks

| Attribute / class | When present | Stability |
|---|---|---|
| `class="pm-panel"` | Always | **Stable** |
| `data-pm-region="<name>"` | Named panels only | **Stable** |
| `id="pm-region-<name>"` | Named panels only | **Stable** |
| `data-pm-kind="panel"` | Named panels only | **Stable** |
| `data-pm-heading="<text>"` | Named panel with a heading defined | **Stable** |
| `data-pm-empty="true"` | Named panel, no interaction assigned | **Stable** |
| Element tag (`section`) | — | Presentation |

Unnamed panels (structural layout nodes with no shell region name) carry
only `class="pm-panel"` and no hooks.  `panelmark-web` should ignore them.

### Locating a panel

Prefer `data-pm-region` over `id` for programmatic targeting — it
unambiguously identifies a panelmark region regardless of page context:

```js
document.querySelector('[data-pm-region="sidebar"]')
// or, for direct access:
document.getElementById('pm-region-sidebar')
```

---

## Interaction metadata attributes

When a `panelmark.Shell` has interactions assigned to regions,
`panelmark-html` emits three additional attributes on the panel element.

```html
<section
  class="pm-panel"
  data-pm-region="menu"
  data-pm-kind="panel"
  id="pm-region-menu"
  data-pm-interaction="panelmark_tui.interactions.menu.MenuReturn"
  data-pm-focusable="true"
  data-pm-focused="false"
>
```

| Attribute | Value | Stability |
|---|---|---|
| `data-pm-interaction` | Fully qualified Python class name (`module.qualname`) | **Stable** |
| `data-pm-focusable` | `"true"` or `"false"` | **Stable** |
| `data-pm-focused` | `"true"` or `"false"` | **Stable** |

These three attributes are mutually exclusive with `data-pm-empty`: a panel
has either all three interaction attributes or `data-pm-empty`, never both.

`data-pm-focused` reflects the shell's focus state at render time.  It is a
static snapshot; live focus updates are the responsibility of `panelmark-web`.

---

## Panel heading element

If the shell definition includes a heading for a region (`__text__` syntax),
a `header` element is emitted as the first child of the panel.

```html
<header class="pm-panel-heading">Settings</header>
```

| Part | Stability |
|------|-----------|
| `class="pm-panel-heading"` | **Stable** |
| Element tag (`header`) | Presentation |
| Heading text content | **Stable** — equals the heading declared in the shell definition |

`panelmark-web` must not remove or replace the heading element; it should
only modify the panel body.

---

## Panel body element

The panel body is the **hydration and update boundary** for `panelmark-web`.

```html
<div class="pm-panel-body"></div>
```

| Part | Stability |
|------|-----------|
| `class="pm-panel-body"` | **Stable** |
| Element tag (`div`) | Presentation |
| Inner content | **Intentionally empty** in `panelmark-html`; owned by `panelmark-web` |

### Update boundary contract

`panelmark-web` is responsible for populating and updating the panel body.
The expected update pattern is:

1. Locate the panel: `[data-pm-region="<name>"] .pm-panel-body`
2. Replace or patch the body's inner HTML with rendered interaction content
3. Re-run on dirty regions after each key or mouse event

`panelmark-web` must not replace the `.pm-panel-body` element itself — only
its contents.  This preserves the structural CSS that depends on the element's
presence in the flex layout.

---

## CSS classes

The following CSS classes are stable API.  `panelmark-web` and embedding
applications may use them as selectors.

| Class | Element | Stability |
|-------|---------|-----------|
| `.pm-shell` | Shell root | **Stable** |
| `.pm-split` | Split container | **Stable** |
| `.pm-split-h` | Horizontal split (column layout) | **Stable** |
| `.pm-split-v` | Vertical split (row layout) | **Stable** |
| `.pm-panel` | Panel element | **Stable** |
| `.pm-panel-heading` | Panel heading | **Stable** |
| `.pm-panel-body` | Panel body / update boundary | **Stable** |

---

## CSS custom properties

The following CSS custom properties are stable theming hooks.  Override
them in your own stylesheet to theme the shell without modifying
`panelmark-html` output.

| Property | Default | Controls |
|----------|---------|----------|
| `--pm-border-color` | `#888` | Border and divider colour |
| `--pm-border-width` | `1px` | Thickness of all borders |
| `--pm-gap` | `0px` | Gap between sibling panels |
| `--pm-radius` | `0px` | Corner radius on panels |
| `--pm-heading-font-weight` | `bold` | Heading font weight |
| `--pm-panel-padding` | `0.5rem` | Padding inside body and heading |
| `--pm-focused-border-color` | `#4a9eff` | Outline colour on the focused panel |
| `--pm-focused-border-width` | `2px` | Outline thickness on the focused panel |

All properties are defined on `:root` in the base stylesheet and inherit
into panels automatically.

The `--pm-focused-*` properties control the `[data-pm-focused="true"]` rule.
`panelmark-html` emits `data-pm-focused` as a static snapshot; live updates
are the responsibility of `panelmark-web`.

---

## Presentation details — do not depend on these

The following are internal rendering choices that may change in any release:

- The specific HTML element tags used (`div`, `section`, `header`) — use
  class or data attribute selectors instead of tag selectors
- Attribute ordering within a single element
- Whitespace and indentation in the rendered HTML
- The exact default values of CSS custom properties
- The order of CSS rules within the base stylesheet
- The exact nesting depth and order of split containers (the class semantics
  are stable; the specific tree of `pm-split` elements is not)

---

## Compatibility summary

`panelmark-web` should rely on this pattern to locate and update a region:

```js
// 1. Find the panel
const panel = document.querySelector('[data-pm-region="sidebar"]');

// 2. Read metadata
const interactionClass = panel.dataset.pmInteraction;  // e.g. "...MenuReturn"
const isFocusable      = panel.dataset.pmFocusable === 'true';
const isEmpty          = 'pmEmpty' in panel.dataset;
const heading          = panel.dataset.pmHeading;      // undefined if no heading

// 3. Update the body only
const body = panel.querySelector('.pm-panel-body');
body.innerHTML = renderInteractionHTML(interactionClass, state);
```

This pattern is stable across all `panelmark-html` releases that follow this
contract.
