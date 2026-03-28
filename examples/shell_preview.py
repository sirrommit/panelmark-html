"""Example: shell preview page

Renders a panelmark shell definition as a standalone preview page.  Useful
during development to inspect the panel structure of a shell before wiring
up interactions or a live renderer.

Pass a shell definition string as the first argument, or run without
arguments to use the built-in example.

Usage
-----
    # Use the built-in example shell
    python examples/shell_preview.py > preview.html

    # Preview a shell stored in a file (contents piped via stdin)
    python examples/shell_preview.py "$(cat myapp.shell)" > preview.html

The output includes:
  - The rendered panel structure with all stable hooks
  - The base CSS inlined in <head>
  - A small legend block listing the named regions and their hook ids
"""

import sys
import os
from html import escape

_here = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_here, '..', '..', 'panelmark'))
sys.path.insert(0, os.path.join(_here, '..'))

from panelmark import Shell
from panelmark_html import render_fragment, get_base_css

DEFAULT_LAYOUT = """
|=== __Shell Preview__ ===|
|{25% $menu$ }|{$main$ }|
|=========================|
|{30% $inspector$ }|{$log$ }|
|=========================|
|{$status$ }|
|=========================|
"""

definition = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_LAYOUT
shell = Shell(definition)

fragment = render_fragment(shell)
css = get_base_css()

# Build a legend listing each named region and its DOM hook.
regions = shell.regions
legend_rows = ''.join(
    f'      <tr>'
    f'<td><code>{escape(name)}</code></td>'
    f'<td><code>pm-region-{escape(name)}</code></td>'
    f'<td><code>data-pm-region=&quot;{escape(name)}&quot;</code></td>'
    f'</tr>\n'
    for name in sorted(regions)
)

PREVIEW = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Shell Preview — panelmark-html</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: monospace; background: #fafafa; padding: 1rem; }}
    h1 {{ font-size: 1rem; margin-bottom: 0.75rem; color: #333; }}
    .preview-shell {{ height: 400px; margin-bottom: 1.5rem; }}
    h2 {{ font-size: 0.85rem; margin-bottom: 0.5rem; color: #555; }}
    table {{ border-collapse: collapse; font-size: 0.8rem; width: 100%; }}
    th, td {{ text-align: left; padding: 0.25rem 0.5rem;
              border: 1px solid #ddd; }}
    th {{ background: #eee; }}

    /* panelmark base styles */
{chr(10).join('    ' + line for line in css.splitlines())}
  </style>
</head>
<body>
  <h1>panelmark-html — shell preview</h1>
  <div class="preview-shell">
{chr(10).join('    ' + line for line in fragment.splitlines())}
  </div>
  <h2>Named regions</h2>
  <table>
    <thead>
      <tr><th>Region name</th><th>id</th><th>data attribute</th></tr>
    </thead>
    <tbody>
{legend_rows}    </tbody>
  </table>
</body>
</html>"""

print(PREVIEW)
