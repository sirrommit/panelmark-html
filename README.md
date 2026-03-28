# panelmark-html

**panelmark-html** is the static HTML/CSS renderer for the
[panelmark](https://github.com/sirrommit/panelmark) ecosystem. Given a
`panelmark` shell and its assigned interactions, it produces an HTML document
or fragment representing the shell's panel structure.

---

## What this package is

- A static renderer: layout model in, HTML string out.
- Useful for server-side rendering into Flask/Django templates, generating
  reports or dashboards, and automated snapshot tests.
- The structural foundation that `panelmark-web` will build live interactivity
  on top of.

## What this package is not

- It does not handle browser events, keyboard or mouse input, or focus
  transitions.
- It does not open sockets, HTTP routes, or sessions.
- It does not render interaction-internal state (item lists, form fields,
  text content). Panel bodies are empty placeholders with stable DOM hooks;
  filling them in with live content is the job of `panelmark-web`.
- It does not require JavaScript for its output to be valid HTML.

## Relationship to panelmark-web

`panelmark-html` and `panelmark-web` are separate packages with distinct scopes.

| Package | Role |
|---------|------|
| **panelmark-html** | Static structure: panel layout, borders, headings, stable DOM hooks |
| **panelmark-web** | Live layer: browser events, interaction rendering, server sessions |

`panelmark-web` depends on `panelmark-html` for its rendered structure. The
DOM hooks and CSS classes defined here are the stable contract between the two
packages.

## Installation

```
pip install panelmark-html
```

## Dependencies

- `panelmark` — core layout model and shell state machine
- No web framework dependency
- No JavaScript build step

## Status

**Package maturity:** Pre-alpha. The public Python API (`render_fragment`,
`render_document`, `get_base_css`, `HTMLRenderer`) and higher-level rendering
features may still evolve.

**Hook contract:** The region-level DOM hooks (`data-pm-region`, `id`,
`data-pm-*` attributes) and CSS classes (`.pm-shell`, `.pm-split-*`,
`.pm-panel`, `.pm-panel-body`) are the intended stable substrate for
`panelmark-web` and are documented as such in
[docs/hook-contract.md](docs/hook-contract.md).  These will not change
without a major version bump.
