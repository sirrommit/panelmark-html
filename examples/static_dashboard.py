"""Example: static dashboard

Renders a multi-panel dashboard shell to a complete, self-contained HTML
document and writes it to stdout.

Usage
-----
    python examples/static_dashboard.py > dashboard.html

The output is a full HTML page with the base CSS inlined.  Open it in any
browser to preview the panel structure.

No interactions are assigned, so every panel renders as an empty placeholder
with a ``data-pm-empty="true"`` hook.  This is the expected state for a
``panelmark-html`` document before ``panelmark-web`` hydrates it.
"""

import sys
import os

# Allow running directly without installing the packages.
_here = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_here, '..', '..', 'panelmark'))
sys.path.insert(0, os.path.join(_here, '..'))

from panelmark import Shell
from panelmark_html import render_document

LAYOUT = """
|=== __Analytics Dashboard__ ===|
|{20% $nav$ }|{$content$ }|
|================================|
|{$status$ }|
|================================|
"""

shell = Shell(LAYOUT)

print(render_document(
    shell,
    title="Analytics Dashboard",
))
