# Border rendering fix required

`panelmark` core now returns `(regions, borders)` from `LayoutModel.resolve()` (and
therefore from `Shell._resolve_layout()`).  The `borders` list contains
`BorderSpec` objects — one per internal HSplit separator line — with position,
style, and optional title text.

`Shell.borders` is a new read-only property that exposes this list.

## What panelmark-html must do

1. **Unpack the new tuple** everywhere `model.resolve(...)` is called directly
   (if any).  The `Shell` class already unpacks it internally, so renderer code
   that goes through `shell.borders` needs no change there.

2. **Render border lines** using the `BorderSpec` data.  Each `BorderSpec` has:
   - `row`, `col`, `width` — cell-grid coordinates
   - `style` — `'single'` (`-`) or `'double'` (`=`)
   - `title` — optional text centred in the border line

   Suggested HTML approach: emit a `<div>` positioned at `(row, col)` spanning
   `width` character cells, with a CSS border-bottom (single: `1px solid`,
   double: `3px double`) and the title text centred inside it.

3. **Read `shell.borders`** after layout resolution and include border elements
   in the rendered output.

## Context

- `BorderSpec` is importable from `panelmark.layout`.
- The change was made so that border titles like `|----Students----|` are
  actually visible at runtime.  Previously they were parsed and stored but
  never rendered.
- The `{----Students---}` syntax (with braces) is NOT a border — it is a
  content row inside a panel definition.  Only bare `|----text----|` and
  `|====text====|` lines between panel rows produce `BorderSpec` entries.
