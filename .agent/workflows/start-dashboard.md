---
description: Generate and open the interactive data visualization dashboard
---

# Start Visualization Dashboard

Generate an HTML dashboard with all charts and visualizations.

## Steps

1. Generate the dashboard HTML:
// turbo
```bash
python3 -c "
from analysis.loader import load_posts
from analysis.insights import find_dangerous_posts
from analysis.visualize import generate_dashboard_html

print('Loading data...')
posts = load_posts()
dangerous = find_dangerous_posts(posts)

print(f'Generating dashboard for {len(posts)} posts...')
output = generate_dashboard_html(posts, dangerous)
print(f'Dashboard saved to: {output}')
"
```

2. Open in browser (optional):
```bash
xdg-open dashboard.html 2>/dev/null || open dashboard.html 2>/dev/null || echo "Open dashboard.html in your browser"
```

## Charts Included
- 🏠 Submolt Activity (bar chart)
- 🚨 Danger Keywords Heatmap
- 📈 Daily Activity Timeline
- 🏆 Top Authors
- 📊 Category Distribution (pie)
- 💬 Engagement Scatter
- 📝 Word Frequency
