import html
import os
from pathlib import Path

skills = [
    ("Java / Spring Boot", 90, "#f89820"),
    ("Angular", 80, "#dd0031"),
    ("MySQL", 85, "#4479a1"),
    ("Git / GitHub", 90, "#f05032"),
    ("Docker", 70, "#2496ed"),
    ("Design Patterns", 60, "#8b5cf6"),
    ("Architecture", 60, "#00add8"),
    ("CI/CD", 45, "#22c55e"),
]

width = 760
height = 80 + len(skills) * 58
bar_x = 250
bar_width = 400

rows = []

for index, (name, percent, color) in enumerate(skills):
    y = 55 + index * 58
    completed = int(bar_width * percent / 100)

    rows.append(
        f'''
        <text x="28" y="{y}" class="label">{html.escape(name)}</text>
        <rect x="{bar_x}" y="{y - 21}" width="{bar_width}" height="18" rx="9" fill="#30363d"/>
        <rect x="{bar_x}" y="{y - 21}" width="{completed}" height="18" rx="9" fill="{color}"/>
        <text x="680" y="{y}" class="value">{percent}%</text>
        '''
    )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>
    .title {{ fill: #c9d1d9; font: 700 24px "Segoe UI", Arial, sans-serif; }}
    .label {{ fill: #c9d1d9; font: 600 16px "Segoe UI", Arial, sans-serif; }}
    .value {{ fill: #c9d1d9; font: 700 15px "Segoe UI", Arial, sans-serif; }}
    .subtitle {{ fill: #8b949e; font: 14px "Segoe UI", Arial, sans-serif; }}
  </style>

  <rect width="100%" height="100%" rx="14" fill="#0d1117"/>
  <text x="28" y="38" class="title">Progression technique</text>
  <text x="28" y="62" class="subtitle">Auto-évaluation — mise à jour via GitHub Actions</text>

  {''.join(rows)}
</svg>
'''

output = Path("profile/skills.svg")
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(svg, encoding="utf-8")
