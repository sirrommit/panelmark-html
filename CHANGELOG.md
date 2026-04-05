# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- HSplit border rendering: `|---|` and `|===|` separator lines between panels
  now emit a `<div class="pm-border pm-border-single">` or
  `<div class="pm-border pm-border-double">` element in the HTML output.
  When the border carries a title (e.g. `|--- Students ---|`), a
  `<span class="pm-border-title">` is nested inside.
- CSS rules for `.pm-border`, `.pm-border-single`, `.pm-border-double`, and
  `.pm-border-title`. The generic sibling border rule is suppressed when an
  explicit `pm-border` element is present, preventing doubled lines.
- `--pm-focused-border-color` and `--pm-focused-border-width` CSS custom
  properties controlling the focused-panel highlight.
- `[data-pm-focused="true"]` CSS rule using those custom properties.
- `data-pm-heading` attribute on panels that carry a `heading` annotation.
- `<header class="pm-panel-heading">` rendered inside panels that have a
  `__text__` heading set in the shell definition.
- `panelmark-web` handoff documentation (`docs/hook-contract.md`).
- README with quick start, API surface summary, and documentation links.
- PyPI packaging metadata (`pyproject.toml`, `LICENSE`, `AUTHORS`).

### Fixed

- `data-pm-heading` attribute was missing from panels with headings.
- Split stability: VSplit flex layout no longer collapses under certain
  content configurations.
- setuptools pinned below 77 to avoid metadata 2.4 incompatibility with twine.

---

## [0.1.0] — 2026-03-28

Initial release.

### Added

- `HTMLRenderer` class with `render_fragment()` and `render_document()` methods.
- Structural renderer: `VSplit` → `<div class="pm-split pm-split-v">`,
  `HSplit` → `<div class="pm-split pm-split-h">`, `Panel` → `<section class="pm-panel">`.
- Stable DOM hooks on every named panel: `data-pm-region`, `data-pm-kind`,
  `id="pm-region-{name}"`.
- Interaction metadata attributes: `data-pm-interaction`, `data-pm-focusable`,
  `data-pm-focused`; unnamed panels receive `data-pm-empty="true"`.
- Base CSS (`get_base_css()`) with CSS custom properties for full theming:
  `--pm-border-color`, `--pm-border-width`, `--pm-gap`, `--pm-radius`,
  `--pm-heading-font-weight`, `--pm-panel-padding`.
- Automatic single-pixel dividers between sibling panels via CSS sibling rules.
- Snapshot tests (`tests/test_snapshots.py`) and CSS tests (`tests/test_css.py`).
- Example scripts (`examples/`) with rendered output in `examples/out/`.

[Unreleased]: https://github.com/sirrommit/panelmark-html/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/sirrommit/panelmark-html/releases/tag/v0.1.0
