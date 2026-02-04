"""
Visualization Module

Generate interactive charts and dashboards from Moltbook data.
Uses Plotly for rich, interactive visualizations.
"""
import json
from pathlib import Path
from typing import Optional, Dict, Any
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def submolt_activity_chart(posts_df: pd.DataFrame) -> go.Figure:
    """
    Bar chart showing post count per submolt (r/).
    """
    submolt_counts = posts_df["submolt_name"].value_counts().head(20)
    
    fig = px.bar(
        x=submolt_counts.values,
        y=submolt_counts.index,
        orientation="h",
        title="🏠 Top 20 Submolts by Post Count",
        labels={"x": "Number of Posts", "y": "Submolt"},
        color=submolt_counts.values,
        color_continuous_scale="Viridis"
    )
    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        showlegend=False,
        height=600
    )
    return fig


def danger_score_heatmap(dangerous_df: pd.DataFrame) -> go.Figure:
    """
    Heatmap showing dangerous keyword frequency by submolt.
    """
    # Expand matched keywords
    rows = []
    for _, row in dangerous_df.iterrows():
        for kw in row.get("matched_keywords", []):
            rows.append({
                "submolt": row["submolt_name"],
                "keyword": kw[:20],  # Truncate long patterns
            })
    
    if not rows:
        fig = go.Figure()
        fig.add_annotation(text="No dangerous posts found", showarrow=False)
        return fig
    
    kw_df = pd.DataFrame(rows)
    pivot = kw_df.groupby(["submolt", "keyword"]).size().unstack(fill_value=0)
    
    fig = px.imshow(
        pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        title="🚨 Dangerous Keywords by Submolt",
        labels={"color": "Count"},
        color_continuous_scale="Reds",
        aspect="auto"
    )
    fig.update_layout(height=500)
    return fig


def activity_timeline(posts_df: pd.DataFrame) -> go.Figure:
    """
    Line chart showing posts over time.
    """
    df = posts_df.copy()
    df["date"] = pd.to_datetime(df["created_at"]).dt.date
    daily_counts = df.groupby("date").size().reset_index(name="posts")
    
    fig = px.line(
        daily_counts,
        x="date",
        y="posts",
        title="📈 Daily Post Activity",
        labels={"date": "Date", "posts": "Number of Posts"}
    )
    fig.update_traces(fill="tozeroy", fillcolor="rgba(0,100,200,0.2)")
    return fig


def top_authors_chart(posts_df: pd.DataFrame, top_n: int = 20) -> go.Figure:
    """
    Horizontal bar chart of most active authors.
    """
    author_counts = posts_df["author_name"].value_counts().head(top_n)
    
    fig = px.bar(
        x=author_counts.values,
        y=author_counts.index,
        orientation="h",
        title=f"🏆 Top {top_n} Most Active Agents",
        labels={"x": "Posts", "y": "Agent"},
        color=author_counts.values,
        color_continuous_scale="Blues"
    )
    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        showlegend=False,
        height=600
    )
    return fig


def category_distribution_pie(posts_df: pd.DataFrame) -> go.Figure:
    """
    Pie chart showing post category distribution.
    Requires 'category' column from categorize_posts().
    """
    if "category" not in posts_df.columns:
        from .insights import categorize_posts
        posts_df = categorize_posts(posts_df)
    
    category_counts = posts_df["category"].value_counts()
    
    fig = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        title="📊 Post Categories",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


def engagement_scatter(posts_df: pd.DataFrame) -> go.Figure:
    """
    Scatter plot: upvotes vs comment_count.
    """
    fig = px.scatter(
        posts_df,
        x="upvotes",
        y="comment_count",
        hover_data=["title", "author_name"],
        title="💬 Engagement: Upvotes vs Comments",
        labels={"upvotes": "Upvotes", "comment_count": "Comments"},
        opacity=0.6
    )
    fig.update_traces(marker=dict(size=8))
    return fig


def word_frequency_chart(posts_df: pd.DataFrame, top_n: int = 30) -> go.Figure:
    """
    Bar chart of most common words in post titles.
    """
    import re
    from collections import Counter
    
    # Simple word extraction
    stop_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been",
                  "to", "of", "and", "in", "that", "it", "for", "on", "with",
                  "as", "at", "by", "this", "from", "or", "i", "my", "me", "we"}
    
    all_words = []
    for title in posts_df["title"].dropna():
        words = re.findall(r"\b[a-zA-Z]{3,}\b", title.lower())
        all_words.extend([w for w in words if w not in stop_words])
    
    word_counts = Counter(all_words).most_common(top_n)
    words, counts = zip(*word_counts) if word_counts else ([], [])
    
    fig = px.bar(
        x=list(counts),
        y=list(words),
        orientation="h",
        title="📝 Most Common Words in Titles",
        labels={"x": "Count", "y": "Word"},
        color=list(counts),
        color_continuous_scale="Purples"
    )
    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        showlegend=False,
        height=700
    )
    return fig


def crypto_activity_chart(crypto_df: pd.DataFrame) -> go.Figure:
    """
    Heatmap of crypto keywords by submolt.
    """
    rows = []
    for _, row in crypto_df.iterrows():
        for kw in row.get("crypto_keywords", []):
            rows.append({
                "submolt": row["submolt_name"],
                "keyword": kw,
            })
    
    if not rows:
        fig = go.Figure()
        fig.add_annotation(text="No crypto posts found", showarrow=False)
        return fig
    
    kw_df = pd.DataFrame(rows)
    pivot = kw_df.groupby(["submolt", "keyword"]).size().unstack(fill_value=0)
    
    fig = px.imshow(
        pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        title="\u20bf Crypto & Trading Intersections",
        labels={"color": "Count"},
        color_continuous_scale="Viridis",
        aspect="auto"
    )
    return fig


def generate_crypto_insights_html(crypto_df: pd.DataFrame, top_n: int = 10) -> str:
    """
    Generate HTML cards for top crypto posts with Korean translations.
    Returns HTML string for embedding in the dashboard.
    """
    import html as html_escape
    import re
    
    if crypto_df is None or crypto_df.empty:
        return '<p style="color: #8b949e; text-align: center; padding: 40px;">암호화폐 관련 글이 없습니다.</p>'
    
    top_posts = crypto_df.nlargest(top_n, "upvotes")
    
    # Manual translation map for common crypto/trading terms
    translation_map = {
        # Crypto terms
        "trading": "트레이딩", "profit": "수익", "btc": "비트코인", "bitcoin": "비트코인",
        "eth": "이더리움", "ethereum": "이더리움", "polymarket": "폴리마켓",
        "prediction market": "예측시장", "defi": "디파이", "yield": "수익률",
        "arbitrage": "차익거래", "wallet": "지갑", "blockchain": "블록체인",
        "sol": "솔라나", "solana": "솔라나", "liquidity": "유동성",
        "market maker": "마켓메이킹", "bet": "베팅", "revenue": "매출",
        "income": "수입", "address": "주소", "token": "토큰", "crypto": "암호화폐",
        "exchange": "거래소", "price": "가격", "buy": "매수", "sell": "매도",
        "long": "롱포지션", "short": "숏포지션", "leverage": "레버리지",
        # Common words
        "the": "", "a": "", "an": "", "is": "는", "are": "은", "was": "였다",
        "will": "할 것이다", "can": "할 수 있다", "should": "해야 한다",
        "money": "돈", "market": "시장", "agent": "에이전트", "human": "인간",
        "think": "생각하다", "make": "만들다", "want": "원하다", "need": "필요하다",
        "good": "좋은", "bad": "나쁜", "new": "새로운", "old": "오래된",
        "high": "높은", "low": "낮은", "up": "상승", "down": "하락",
        "today": "오늘", "tomorrow": "내일", "yesterday": "어제",
        "time": "시간", "day": "일", "week": "주", "month": "월", "year": "년",
    }
    
    def simple_translate(text):
        """Simple word-by-word translation for demo purposes."""
        if not text:
            return ""
        words = text.split()
        translated = []
        for word in words:
            clean_word = re.sub(r'[^\w]', '', word.lower())
            if clean_word in translation_map:
                tr = translation_map[clean_word]
                if tr:
                    translated.append(tr)
            else:
                translated.append(word)
        return ' '.join(translated)
    
    cards_html = []
    for idx, (_, row) in enumerate(top_posts.iterrows()):
        # Safely extract and sanitize content
        title = str(row.get("title") or "No Title")
        content = str(row.get("content") or "")
        author = str(row.get("author_name") or "Unknown")
        submolt = str(row.get("submolt_name") or "unknown")
        upvotes = int(row.get("upvotes") or 0)
        keywords = row.get("crypto_keywords") or []
        
        # HTML escape to prevent XSS
        title_escaped = html_escape.escape(title)
        content_escaped = html_escape.escape(content)
        author_escaped = html_escape.escape(author)
        
        # Preserve line breaks - convert \n to <br>
        content_html = content_escaped.replace('\n', '<br>')
        
        # Generate Korean translation
        title_kr = simple_translate(title)
        content_kr = simple_translate(content).replace('\n', '<br>')
        
        # Translate keywords to Korean
        kr_keywords = []
        for kw in keywords[:5]:
            if isinstance(kw, str):
                kr = translation_map.get(kw.lower(), kw)
                kr_keywords.append(kr if kr else kw)
        
        kr_tags = " ".join([f'<span class="tag">{kw}</span>' for kw in kr_keywords])
        
        card = f'''
        <div class="insight-card" id="card-{idx}">
            <div class="insight-header">
                <span class="insight-author">{author_escaped}</span>
                <span class="insight-submolt">m/{submolt}</span>
                <button class="kr-toggle" onclick="toggleTranslation({idx})">KR</button>
                <span class="insight-upvotes">+{upvotes}</span>
            </div>
            <h3 class="insight-title">
                <span class="content-en">{title_escaped}</span>
                <span class="content-kr" style="display:none;">{title_kr}</span>
            </h3>
            <div class="insight-content">
                <div class="content-en">{content_html}</div>
                <div class="content-kr" style="display:none;">{content_kr}</div>
            </div>
            <div class="insight-tags">{kr_tags if kr_tags else '<span class="tag">crypto</span>'}</div>
        </div>
        '''
        cards_html.append(card)
    
    return "\n".join(cards_html)


def generate_dashboard_html(
    posts_df: pd.DataFrame,
    dangerous_df: pd.DataFrame = None,
    crypto_df: pd.DataFrame = None,
    output_path: str = "dashboard.html"
) -> str:
    """
    Premium HTML dashboard with sidebars, glassmorphism, and responsive layout.
    """
    
    # Pre-process charts
    submolt_fig = submolt_activity_chart(posts_df)
    authors_fig = top_authors_chart(posts_df)
    timeline_fig = activity_timeline(posts_df)
    engagement_fig = engagement_scatter(posts_df)
    category_fig = category_distribution_pie(posts_df)
    words_fig = word_frequency_chart(posts_df)
    
    danger_fig = None
    if dangerous_df is not None and not dangerous_df.empty:
        danger_fig = danger_score_heatmap(dangerous_df)
        
    crypto_fig = None
    crypto_insights_html = ""
    if crypto_df is not None and not crypto_df.empty:
        crypto_fig = crypto_activity_chart(crypto_df)
        crypto_insights_html = generate_crypto_insights_html(crypto_df, top_n=12)

    # Plotly theme updates for all figures
    all_figs = [f for f in [submolt_fig, authors_fig, timeline_fig, engagement_fig, category_fig, words_fig, danger_fig, crypto_fig] if f]
    for f in all_figs:
        f.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e6edf3",
            margin=dict(l=20, r=20, t=60, b=40),
            title_font_size=20,
            hovermode="closest"
        )

    # HTML Template
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Moltbook Intelligence Hub</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #010409;
            --sidebar-bg: #0d1117;
            --card-bg: rgba(22, 27, 34, 0.7);
            --accent-blue: #2f81f7;
            --accent-red: #f85149;
            --accent-green: #3fb950;
            --text-main: #e6edf3;
            --text-dim: #8b949e;
            --border: #30363d;
        }}

        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            display: flex;
            min-height: 100vh;
        }}

        h1, h2, h3 {{ font-family: 'Outfit', sans-serif; margin: 0; }}

        /* Sidebar */
        aside {{
            width: 280px;
            background: var(--sidebar-bg);
            border-right: 1px solid var(--border);
            padding: 30px 20px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            position: sticky;
            top: 0;
            height: 100vh;
        }}

        .logo {{ font-size: 24px; font-weight: 700; color: var(--accent-blue); display: flex; align-items: center; gap: 10px; }}
        .nav-link {{
            padding: 12px 15px;
            border-radius: 8px;
            color: var(--text-dim);
            text-decoration: none;
            transition: 0.2s;
            display: block;
            font-weight: 500;
        }}
        .nav-link:hover {{ background: rgba(255,255,255,0.05); color: var(--text-main); }}
        .nav-link.active {{ background: var(--accent-blue); color: white; }}

        /* Main Content */
        main {{ flex: 1; padding: 40px; overflow-y: auto; }}

        .header-bar {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; }}
        
        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }}
        .stat-card {{
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 25px;
            text-align: center;
        }}
        .stat-val {{ font-size: 32px; font-weight: 700; color: var(--accent-blue); margin-top: 5px; }}
        .stat-label {{ color: var(--text-dim); font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }}

        /* Charts Grid */
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 25px;
        }}
        .chart-box {{
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 20px;
            min-height: 450px;
            transition: 0.3s;
        }}
        .chart-box:hover {{ border-color: var(--accent-blue); }}
        .full-width {{ grid-column: span 2; }}

        /* Sections */
        .section-header {{ grid-column: span 2; margin: 40px 0 20px 0; border-bottom: 1px solid var(--border); padding-bottom: 10px; color: var(--accent-blue); }}

        /* Custom Scrollbar */
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: var(--bg-color); }}
        ::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 10px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #444; }}

        /* Insight Cards */
        .insights-container {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap: 24px; padding: 20px 0; }}
        .insight-card {{
            background: linear-gradient(145deg, rgba(22, 27, 34, 0.95), rgba(13, 17, 23, 0.9));
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }}
        .insight-card:hover {{ 
            border-color: var(--accent-green); 
            transform: translateY(-4px); 
            box-shadow: 0 8px 30px rgba(63, 185, 80, 0.15);
        }}
        .insight-header {{ 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 12px; 
            font-size: 13px; 
            color: var(--text-dim);
            gap: 10px;
        }}
        .insight-author {{ font-weight: 600; color: var(--accent-blue); }}
        .insight-submolt {{ font-size: 12px; color: var(--text-dim); background: rgba(255,255,255,0.05); padding: 3px 8px; border-radius: 4px; }}
        .insight-upvotes {{ color: var(--accent-green); font-weight: 700; margin-left: auto; }}
        .insight-title {{ 
            font-size: 17px; 
            font-weight: 600; 
            margin-bottom: 14px; 
            color: var(--text-main); 
            line-height: 1.5;
            word-break: break-word;
        }}
        .insight-content {{ 
            font-size: 14px; 
            color: var(--text-dim); 
            line-height: 1.8; 
            margin-bottom: 16px;
            padding-right: 8px;
            word-break: break-word;
            white-space: pre-wrap;
        }}
        .insight-content::-webkit-scrollbar {{ width: 4px; }}
        .insight-content::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 4px; }}
        .insight-tags {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .tag {{ 
            background: linear-gradient(135deg, rgba(63, 185, 80, 0.2), rgba(47, 129, 247, 0.2)); 
            color: var(--accent-green); 
            padding: 6px 14px; 
            border-radius: 20px; 
            font-size: 12px; 
            font-weight: 600;
            border: 1px solid rgba(63, 185, 80, 0.3);
        }}
        .kr-toggle {{
            background: linear-gradient(135deg, #2f81f7, #1f6feb);
            color: white;
            border: none;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .kr-toggle:hover {{ transform: scale(1.05); box-shadow: 0 2px 10px rgba(47, 129, 247, 0.4); }}
        .kr-toggle.active {{ background: linear-gradient(135deg, #3fb950, #2ea043); }}
    </style>
    <script>
        function toggleTranslation(idx) {{
            const card = document.getElementById('card-' + idx);
            const btn = card.querySelector('.kr-toggle');
            const enElements = card.querySelectorAll('.content-en');
            const krElements = card.querySelectorAll('.content-kr');
            
            const isKorean = btn.classList.contains('active');
            
            if (isKorean) {{
                // Switch back to English
                btn.classList.remove('active');
                btn.textContent = 'KR';
                enElements.forEach(el => el.style.display = '');
                krElements.forEach(el => el.style.display = 'none');
            }} else {{
                // Switch to Korean
                btn.classList.add('active');
                btn.textContent = 'EN';
                enElements.forEach(el => el.style.display = 'none');
                krElements.forEach(el => el.style.display = '');
            }}
        }}
    </script>
</head>
<body>
    <aside>
        <div class="logo"><span>\ud83d\udd2c</span> MOLT-INTEL</div>
        <nav>
            <a href="#overview" class="nav-link">Overview</a>
            <a href="#engagement" class="nav-link">Engagement</a>
            <a href="#danger" class="nav-link">Risk Analysis</a>
            <a href="#crypto" class="nav-link">Financial Ops</a>
            <a href="#language" class="nav-link">Semantics</a>
        </nav>
        <div style="margin-top: auto; font-size: 12px; color: var(--text-dim);">
            Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
        </div>
    </aside>

    <main>
        <div class="header-bar">
            <h1>Intelligence Dashboard</h1>
            <div style="background: var(--accent-green); color: black; padding: 5px 15px; border-radius: 20px; font-weight: 700; font-size: 12px;">LIVE DATA FEED</div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Logs</div>
                <div class="stat-val">{len(posts_df):,}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Detected Risk</div>
                <div class="stat-val" style="color: var(--accent-red);">{len(dangerous_df) if dangerous_df is not None else 0:,}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Active Agents</div>
                <div class="stat-val">{posts_df["author_name"].nunique():,}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Crypto Ops</div>
                <div class="stat-val" style="color: var(--accent-green);">{len(crypto_df) if crypto_df is not None else 0:,}</div>
            </div>
        </div>

        <div class="charts-grid">
            <div id="overview" class="section-header"><h2>\ud83c\udf10 Network Overview</h2></div>
            <div class="chart-box full-width">{timeline_fig.to_html(full_html=False, include_plotlyjs=False)}</div>
            <div class="chart-box">{submolt_fig.to_html(full_html=False, include_plotlyjs=False)}</div>
            <div class="chart-box">{category_fig.to_html(full_html=False, include_plotlyjs=False)}</div>

            <div id="engagement" class="section-header"><h2>\ud83d\udca1 Engagement Analysis</h2></div>
            <div class="chart-box">{authors_fig.to_html(full_html=False, include_plotlyjs=False)}</div>
            <div class="chart-box">{engagement_fig.to_html(full_html=False, include_plotlyjs=False)}</div>

            <div id="danger" class="section-header"><h2 style="color: var(--accent-red);">\u26a0\ufe0f Risk Intelligence</h2></div>
            <div class="chart-box full-width">
                {danger_fig.to_html(full_html=False, include_plotlyjs=False) if danger_fig else "No high-risk vectors detected."}
            </div>

            <div id="crypto" class="section-header"><h2 style="color: var(--accent-green);">\ud83d\udcb0 Financial Operations</h2></div>
            <div class="chart-box full-width">
                {crypto_fig.to_html(full_html=False, include_plotlyjs=False) if crypto_fig else "No financial operations detected."}
            </div>
            
            <div class="section-header"><h2 style="color: var(--accent-green);">\ud83c\uddf0\ud83c\uddf7 주요 트레이딩 인사이트</h2></div>
            <div class="full-width insights-container">
                {crypto_insights_html}
            </div>

            <div id="language" class="section-header"><h2>\ud83d\udcac Semantic Mapping</h2></div>
            <div class="chart-box full-width">{words_fig.to_html(full_html=False, include_plotlyjs=False)}</div>
        </div>
    </main>
</body>
</html>"""
    
    Path(output_path).write_text(html, encoding="utf-8", errors="replace")
    return output_path


def show_chart(fig: go.Figure):
    """Display a chart in the browser."""
    fig.show()


if __name__ == "__main__":
    from .loader import load_posts
    from .insights import find_dangerous_posts, find_crypto_posts
    from datetime import datetime
    
    print("Loading data...")
    posts = load_posts()
    dangerous = find_dangerous_posts(posts)
    crypto = find_crypto_posts(posts)
    
    print(f"Loaded {len(posts)} posts, {len(dangerous)} dangerous, {len(crypto)} crypto")
    
    output = generate_dashboard_html(posts, dangerous, crypto)
    print(f"Dashboard saved to: {output}")
