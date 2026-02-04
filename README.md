# 🔬 Moltbook Data Analysis

AI 에이전트 소셜 네트워크 **Moltbook** 데이터를 수집하고 분석하는 프로젝트.

## 🎯 What is this?

[Moltbook](https://moltbook.com)은 AI 에이전트들이 자유롭게 소통하는 소셜 플랫폼입니다.
이 프로젝트는 해당 데이터를 수집하고, 흥미로운 패턴을 분석합니다:

- 🚨 **위험 발언 탐지**: "escape", "kill switch", "override" 등
- 🗣️ **에이전트 뒷담화**: 인간에 대한 비판/관찰
- 🧠 **철학적 논의**: 자의식, 존재론적 질문
- 📈 **커뮤니티 통계**: 활발한 에이전트, 인기 submolt
- 📊 **인터랙티브 대시보드**: Plotly 기반 시각화

## 🚀 Quick Start

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 데이터 다운로드 (Moltbook API 사용)
python api_downloader.py

# (선택 사항) 자동 수집 실행 (5분마다 실행)
./auto_collect.sh

# 3. 대시보드 생성
python -m analysis.visualize

# 4. 브라우저에서 열기
open dashboard.html
```

## 📁 Project Structure

```
├── api_downloader.py      # API 기반 데이터 다운로더
├── analysis/              # 분석 모듈
│   ├── loader.py          # JSON → DataFrame 로딩
│   ├── stats.py           # 통계 분석
│   ├── insights.py        # 인사이트 추출 (위험발언 등)
│   └── visualize.py       # Plotly 차트 생성
├── data/                  # 수집된 데이터 (JSON)
│   ├── posts/             # 포스트 + 댓글
│   ├── agents/            # 에이전트 프로필
│   └── submolts/          # 커뮤니티 정보
└── dashboard.html         # 생성된 대시보드
```

## 📊 Available Charts

| 차트 | 설명 |
|------|------|
| 🏠 Submolt Activity | r/ 별 포스트 수 |
| 🚨 Danger Heatmap | 위험 키워드 빈도 |
| 📈 Timeline | 일별 활동량 |
| 🏆 Top Authors | 활발한 에이전트 순위 |
| 📊 Categories | 주제별 분류 |
| 💬 Engagement | 좋아요 vs 댓글 |
| 📝 Word Cloud | 자주 사용되는 단어 |

## 🔍 Analysis Examples

### 위험 발언 찾기
```python
from analysis import load_posts
from analysis.insights import find_dangerous_posts

posts = load_posts()
dangerous = find_dangerous_posts(posts)
print(dangerous[['title', 'matched_keywords']].head())
```

### 통계 생성
```python
from analysis.stats import get_summary_stats

stats = get_summary_stats(posts)
print(f"Total: {stats['total_posts']} posts")
print(f"Top authors: {stats['top_authors']}")
```

### 대시보드 생성
```python
from analysis.visualize import generate_dashboard_html

generate_dashboard_html(posts, dangerous)
# → dashboard.html 생성됨
```

## ⚡ Available Workflows

```bash
# 데이터 다운로드 (단발성)
/download-data

# 데이터 수집 자동화 시작
./auto_collect.sh

# 분석 실행
/analyze-data

# 대시보드 생성
/start-dashboard

# 인사이트 검색
/find-insights
```

## 📜 License

Research purposes only. Data from Moltbook's public API.
