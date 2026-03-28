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

Pre-alpha. API and DOM structure are not yet stable.
