"""Example: server-side rendered fragment

Shows how to embed a ``render_fragment()`` result into a larger HTML
template.  This pattern fits naturally into Flask, Django, FastAPI, or
any other Python web framework that produces HTML responses.

Usage
-----
    python examples/fragment_ssr.py > ssr_example.html

The example simulates a page that has its own chrome (navigation bar,
footer) and embeds the panelmark shell fragment in the main content area.
The base CSS is inlined once in the page's ``<head>``; the fragment itself
carries only the structural HTML.
"""

import sys
import os
from html import escape

_here = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_here, '..', '..', 'panelmark'))
sys.path.insert(0, os.path.join(_here, '..'))

from panelmark import Shell
from panelmark_html import render_fragment, get_base_css

SHELL_LAYOUT = """
|=====|
|{$sidebar$ }|{$editor$ }|
|=====|
"""

shell = Shell(SHELL_LAYOUT)

# Render just the fragment — no wrapping <html> or <head>.
fragment = render_fragment(shell)

# Retrieve the base CSS separately so it can be placed once in <head>.
css = get_base_css()

# Simulate the surrounding page template (e.g. a Flask/Django base template).
PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My App</title>
  <style>
    /* Application styles */
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ display: flex; flex-direction: column; height: 100vh; font-family: sans-serif; }}
    .app-nav {{ flex-shrink: 0; padding: 0.5rem 1rem; background: #222; color: #fff; }}
    .app-main {{ flex: 1; min-height: 0; padding: 1rem; }}
    .app-footer {{ flex-shrink: 0; padding: 0.25rem 1rem; background: #f0f0f0; font-size: 0.75rem; }}

    /* panelmark base styles */
{panelmark_css}
  </style>
</head>
<body>
  <nav class="app-nav">My Application</nav>
  <main class="app-main">
    <!-- panelmark shell fragment injected here by the server -->
{shell_fragment}
  </main>
  <footer class="app-footer">panelmark-html fragment SSR example</footer>
</body>
</html>"""

# Indent the CSS and fragment to fit the template layout.
indented_css = '\n'.join('    ' + line for line in css.splitlines())
indented_fragment = '\n'.join('    ' + line for line in fragment.splitlines())

print(PAGE_TEMPLATE.format(
    panelmark_css=indented_css,
    shell_fragment=indented_fragment,
))
