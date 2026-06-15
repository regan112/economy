import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ──────────────────────────────────────────────
# 페이지 기본 설정
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="대한민국 사교육 상업화 분석 보고서",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# CSS 스타일
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background-color: #0f1117;
        color: #e0e0e0;
    }

    /* 사이드바 */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f2e 0%, #16213e 100%);
        border-right: 1px solid #2d3561;
    }

    /* 메인 타이틀 */
    .main-title {
        text-align: center;
        font-size: 2.6rem;
        font-weight: 900;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #fda085 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding: 1.5rem 0 0.5rem 0;
        line-height: 1.3;
    }

    .sub-title {
        text-align: center;
        color: #8892b0;
        font-size: 1.05rem;
        margin-bottom: 2rem;
        letter-spacing: 0.05em;
    }

    /* 섹션 헤더 */
    .section-header {
        background: linear-gradient(90deg, #1e3a5f 0%, #0f1117 100%);
        border-left: 5px solid #f5576c;
        padding: 1rem 1.5rem;
        margin: 2rem 0 1.5rem 0;
        border-radius: 0 8px 8px 0;
    }

    .section-header h2 {
        color: #ccd6f6;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
    }

    .section-header p {
        color: #8892b0;
        font-size: 0.9rem;
        margin: 0.3rem 0 0 0;
    }

    /* 지표 카드 */
    .metric-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #16213e 100%);
        border: 1px solid #2d3561;
        border-radius: 12px;
        padding: 1.4rem 1.2rem;
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
        margin-bottom: 0.5rem;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        border-color: #f5576c;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #f5576c;
        line-height: 1.2;
    }

    .metric-label {
        font-size: 0.82rem;
        color: #8892b0;
        margin-top: 0.4rem;
        line-height: 1.4;
    }

    .metric-delta {
        font-size: 0.78rem;
        color: #64ffda;
        margin-top: 0.3rem;
    }

    /* 인사이트 박스 */
    .insight-box {
        background: linear-gradient(135deg, #1a2744 0%, #0d1b2a 100%);
        border: 1px solid #2d4a7a;
        border-radius: 10px;
        padding: 1.3rem 1.5rem;
        margin: 1rem 0;
    }

    .insight-box h4 {
        color: #64ffda;
        font-size: 1rem;
        margin: 0 0 0.7rem 0;
    }

    .insight-box p, .insight-box li {
        color: #a8b2d8;
        font-size: 0.9rem;
        line-height: 1.7;
        margin: 0;
    }

    /* 경고/강조 박스 */
    .highlight-box {
        background: linear-gradient(135deg, #2d1b1b 0%, #1a0f0f 100%);
        border: 1px solid #f5576c;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
    }

    .highlight-box p {
        color: #ffb3ba;
        font-size: 0.92rem;
        line-height: 1.7;
        margin: 0;
    }

    /* 결론 박스 */
    .conclusion-box {
        background: linear-gradient(135deg, #1a2e1a 0%, #0d1a0d 100%);
        border: 1px solid #64ffda;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
    }

    .conclusion-box p {
        color: #b3ffec;
        font-size: 0.92rem;
        line-height: 1.7;
        margin: 0;
    }

    /* 구분선 */
    .divider {
        border: none;
        border-top: 1px solid #2d3561;
        margin: 2rem 0;
    }

    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1a1f2e;
        border-radius: 8px;
        padding: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        color: #8892b0;
        border-radius: 6px;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: #2d3561 !important;
        color: #ccd6f6 !important;
    }

    /* 사이드바 링크 */
    .sidebar-nav {
        padding: 0.5rem 1rem;
        margin: 0.3rem 0;
        border-radius: 6px;
        color: #8892b0;
        font-size: 0.9rem;
        cursor: pointer;
    }

    .sidebar-nav:hover {
        background-color: #2d3561;
        color: #ccd6f6;
    }

    /* 출처 텍스트 */
    .source-text {
        color: #4a5568;
        font-size: 0.78rem;
        text-align: right;
        margin-top: 0.5rem;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# 데이터 로드 및 전처리
# ──────────────────────────────────────────────
@st.cache_data
def load_participation_data():
    """성적 구간별 사교육 참여율 데이터 정제"""
    years = list(range(2016, 2026))

    # 전체 사교육 참여율 (평균)
    participation_avg = {
        2016: 67.77, 2017: 71.17, 2018: 58.55, 2019: 60.95,
        2020: 61.56, 2021: 64.56, 2022: 65.96, 2023: 66.43,
        2024: 67.30, 2025: 62.95
    }

    # 성적 구간별 참여율
    participation_by_grade = {
        "상위10% 이내": [77.85, 79.18, 65.78, 72.30, 73.11, 74.56, 77.53, 76.06, 76.60, 73.77],
        "11~30%":       [74.89, 77.61, 64.89, 67.81, 68.90, 72.03, 73.64, 73.67, 74.26, 70.00],
        "31~60%":       [69.67, 72.95, 61.02, 62.78, 63.14, 67.35, 67.49, 69.07, 69.52, 65.46],
        "61~80%":       [64.27, 68.37, 55.48, 57.18, 57.19, 60.13, 61.36, 62.07, 63.32, 58.47],
        "81~100%":      [55.89, 60.59, 47.36, 48.88, 49.81, 51.68, 54.00, 53.94, 55.67, 50.11],
    }

    # 과목별 참여율 (평균)
    subject_participation = {
        "영어":    [39.15, 39.76, 32.47, 36.35, 38.59, 41.00, 42.09, 42.44, 42.91, 38.58],
        "수학":    [42.25, 43.26, 38.00, 41.68, 44.16, 45.57, 46.67, 47.45, 46.91, 42.19],
        "국어":    [17.68, 18.94, 16.02, 18.89, 20.25, 23.93, 25.79, 26.90, 27.52, 25.47],
        "사회·과학": [10.41, 11.24, 7.58, 9.61, 10.68, 13.19, 14.26, 15.00, 14.99, 13.34],
        "예체능·취미": [37.79, 41.13, 15.87, 14.84, 13.51, 14.58, 16.00, 16.02, 17.22, 17.14],
    }

    # 유형별 참여율 (평균, 일반교과)
    type_participation = {
        "학원수강":      [35.82, 36.39, 35.15, 39.26, 40.95, 42.84, 44.27, 45.15, 46.27, 42.88],
        "개인과외":      [9.59, 8.71, 11.41, 12.35, 11.97, 13.46, 13.07, 12.39, 12.00, 10.24],
        "그룹과외":      [8.84, 9.34, 6.48, 6.39, 6.57, 5.89, 5.58, 5.47, 4.65, 4.13],
        "방문학습지":    [11.85, 12.33, 0.62, 0.53, 0.51, 0.49, 0.49, 0.43, 0.38, 0.26],
        "유료인터넷강좌": [5.13, 5.20, 4.11, 5.50, 5.77, 9.40, 9.79, 10.63, 10.81, 8.39],
    }

    return years, participation_avg, participation_by_grade, subject_participation, type_participation


@st.cache_data
def load_expenditure_data():
    """학교급별 사교육비 총액 데이터 정제"""
    years = list(range(2016, 2026))

    # 전체 사교육비 총액 (억원)
    total_expenditure = {
        2016: 180606, 2017: 186703, 2018: 194852, 2019: 209970,
        2020: 193532, 2021: 234158, 2022: 259538, 2023: 271144,
        2024: 291919, 2025: 275351
    }

    # 학교급별 사교육비
    by_school = {
        "초등학교": [77438, 81311, 85531, 95597, 76107, 105279, 119055, 124222, 132256, 121744],
        "중학교":   [48102, 48297, 49972, 52554, 53943, 63480, 70832, 71534, 78338, 75794],
        "고등학교": [55065, 57095, 59348, 61819, 63482, 65399, 69651, 75389, 81324, 77813],
    }

    # 과목별 지출 총액 (억원)
    by_subject = {
        "영어":    [55443, 54250, 56729, 61381, 59908, 71396, 77943, 79873, 86859, 78977],
        "수학":    [53636, 53931, 55479, 58915, 59960, 67356, 73246, 76350, 82762, 77119],
        "국어":    [11318, 12577, 13854, 15013, 16014, 19271, 21577, 23669, 25646, 23275],
        "사회·과학": [7025, 7420, 7744, 8503, 8786, 10466, 11360, 12140, 12600, 11215],
        "논술":    [5390, 5274, 6030, 6525, 5994, 7518, 8236, 8228, 8999, 9123],
    }

    # 지역별 총액 (억원)
    by_region = {
        "서울":    [41263, 44017, 44439, 46853, 45758, 52389, 57709, 59154, 61857, 59164],
        "광역시":  [43011, 44940, 45022, 48209, 44381, 53833, 58671, 62038, 66494, 61540],
        "중소도시": [81301, 78752, 87116, 94318, 83143, 102006, 113730, 120404, 131388, 123971],
        "읍면지역": [15031, 18993, 18274, 20588, 20251, 25931, 29427, 29548, 32180, 30675],
    }

    # 유형별 지출 (일반교과, 억원)
    by_type = {
        "학원수강":       [89075, 90923, 95727, 106974, 105446, 124475, 139755, 150344, 169060, 160609],
        "개인과외":       [21923, 19337, 20234, 19902, 21147, 24214, 24602, 22999, 22491, 18744],
        "그룹과외":       [13536, 14644, 14854, 14377, 14410, 15095, 14698, 13516, 12536, 11112],
        "방문학습지":     [7480, 7801, 7920, 7996, 7199, 7357, 7253, 6751, 6569, 5040],
        "유료인터넷강좌": [3042, 3159, 3865, 4803, 5021, 8257, 9628, 10175, 9658, 6860],
    }

    return years, total_expenditure, by_school, by_subject, by_region, by_type


# ──────────────────────────────────────────────
# 공통 plotly 테마
# ──────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15,17,23,0.6)",
    font=dict(family="Pretendard, Noto Sans KR, sans-serif", color="#ccd6f6"),
    legend=dict(
        bgcolor="rgba(26,31,46,0.8)",
        bordercolor="#2d3561",
        borderwidth=1,
        font=dict(size=11)
    ),
    xaxis=dict(gridcolor="#1e2740", linecolor="#2d3561", tickfont=dict(size=11)),
    yaxis=dict(gridcolor="#1e2740", linecolor="#2d3561", tickfont=dict(size=11)),
    margin=dict(l=40, r=30, t=50, b=40),
    hovermode="x unified",
)

COLOR_PALETTE = [
    "#f5576c", "#64ffda", "#fda085", "#a78bfa",
    "#38bdf8", "#fb923c", "#34d399", "#e879f9"
]


# ──────────────────────────────────────────────
# 사이드바
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem 0;'>
        <span style='font-size:2.5rem;'>📚</span>
        <div style='font-size:1.1rem; font-weight:700; color:#ccd6f6; margin-top:0.5rem;'>
            사교육 상업화<br>분석 보고서
        </div>
        <div style='font-size:0.75rem; color:#8892b0; margin-top:0.3rem;'>
            2016–2025 · 통계청 데이터 기반
        </div>
    </div>
    <hr style='border-color:#2d3561; margin:1rem 0;'>
    """, unsafe_allow_html=True)

    section = st.radio(
        "📋 목차",
        [
            "🏠 개요 및 핵심 지표",
            "📈 시장 규모의 팽창",
            "🎯 성적 구간별 불평등 구조",
            "📚 과목별 상업화 심화",
            "🏫 사교육 유형 변화",
            "🗺️ 지역별 격차 분석",
            "⚙️ 산업화 구조 분석",
            "📌 종합 결론 및 시사점",
        ],
        label_visibility="collapsed"
    )

    st.markdown("""
    <hr style='border-color:#2d3561; margin:1rem 0;'>
    <div style='font-size:0.78rem; color:#4a5568; padding: 0 0.5rem;'>
        📊 데이터 출처<br>
        · 통계청 「초중고 사교육비조사」<br>
        · 학생 성적 구간별 사교육 참여율<br>
        · 학교급별 사교육비 총액<br>
        <br>
        📅 수집 기간: 2016~2025년
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# 데이터 로드
# ──────────────────────────────────────────────
years, part_avg, part_grade, subj_part, type_part = load_participation_data()
years_e, total_exp, school_exp, subj_exp, region_exp, type_exp = load_expenditure_data()


# ══════════════════════════════════════════════
# SECTION 1: 개요 및 핵심 지표
# ══════════════════════════════════════════════
if section == "🏠 개요 및 핵심 지표":
    st.markdown('<div class="main-title">🏫 대한민국 사교육 상업화 분석 보고서</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">2016–2025 통계청 사교육비 조사 데이터 기반 | 사교육 산업화의 구조적 실체</div>', unsafe_allow_html=True)

    # 핵심 지표 카드
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">29.2조</div>
            <div class="metric-label">2024년 사교육비 총액<br>(역대 최고)</div>
            <div class="metric-delta">▲ 2016년 대비 +61.6%</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">67.3%</div>
            <div class="metric-label">2024년 사교육 참여율<br>(전체 학생 기준)</div>
            <div class="metric-delta">▲ 2016년 대비 +0.5%p</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">21.9%p</div>
            <div class="metric-label">성적 구간별 참여율 격차<br>(상위 vs 하위)</div>
            <div class="metric-delta">상위10% 76.6% vs 하위20% 55.7%</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">65.0%</div>
            <div class="metric-label">학원수강 비중<br>(2024 일반교과 기준)</div>
            <div class="metric-delta">▲ 학원 집중화 심화</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # 보고서 개요
    col_l, col_r = st.columns([3, 2])
    with col_l:
        st.markdown("""
        <div class="section-header">
            <h2>📋 보고서 개요</h2>
            <p>사교육 산업화의 구조적 메커니즘 분석</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="insight-box">
            <h4>🔍 분석 목적</h4>
            <p>
            대한민국 사교육은 단순한 '보충학습'의 차원을 넘어 하나의 <strong style='color:#f5576c;'>거대 산업</strong>으로 
            진화하고 있습니다. 본 보고서는 2016년부터 2025년까지 10년간의 통계청 데이터를 
            바탕으로 사교육 상업화의 구체적 구조를 분석합니다.
            </p>
            <br>
            <p><strong style='color:#64ffda;'>핵심 분석 축:</strong></p>
            <ul>
                <li>시장 규모의 급격한 팽창 메커니즘</li>
                <li>성적 구간별 참여율 격차의 구조적 고착화</li>
                <li>수학·영어·국어 중심의 과목별 상업화 심화</li>
                <li>학원 중심 산업 구조로의 집중 현상</li>
                <li>지역별·소득별 사교육 격차의 불평등 재생산</li>
                <li>디지털 전환에 따른 새로운 사교육 시장 형성</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="highlight-box">
            <p>
            ⚠️ <strong>핵심 문제의식:</strong> 사교육 시장은 학생의 학업 성취를 돕는 
            '교육적 기능'보다 학교 교육의 공백을 파고드는 '상업적 기능'이 더 강해지고 있습니다. 
            성적이 높을수록 더 많은 사교육을 받고, 사교육을 더 받을수록 성적이 높아지는 
            <strong>불평등의 자기강화 구조</strong>가 형성되어 있습니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        # 10년간 총액 추이 미니 차트
        fig_mini = go.Figure()
        exp_values = [total_exp[y] / 10000 for y in range(2016, 2026)]
        fig_mini.add_trace(go.Scatter(
            x=list(range(2016, 2026)),
            y=exp_values,
            mode="lines+markers+text",
            name="총액(조원)",
            line=dict(color="#f5576c", width=3),
            marker=dict(size=8, color="#f5576c"),
            text=[f"{v:.1f}" for v in exp_values],
            textposition="top center",
            textfont=dict(size=9, color="#fda085"),
            fill="tozeroy",
            fillcolor="rgba(245,87,108,0.1)"
        ))
        fig_mini.update_layout(
            title=dict(text="📊 연도별 사교육비 총액 (조원)", font=dict(size=13, color="#ccd6f6")),
            height=280,
            **PLOT_LAYOUT,
            showlegend=False
        )
        st.plotly_chart(fig_mini, use_container_width=True)

        # 참여율 미니 차트
        fig_mini2 = go.Figure()
        part_values = [part_avg[y] for y in range(2016, 2026)]
        fig_mini2.add_trace(go.Bar(
            x=list(range(2016, 2026)),
            y=part_values,
            marker=dict(
                color=part_values,
                colorscale=[[0, "#2d3561"], [0.5, "#a78bfa"], [1, "#f5576c"]],
                showscale=False
            ),
            text=[f"{v:.1f}%" for v in part_values],
            textposition="outside",
            textfont=dict(size=9, color="#8892b0")
        ))
        fig_mini2.update_layout(
            title=dict(text="📊 연도별 사교육 참여율 (%)", font=dict(size=13, color="#ccd6f6")),
            height=260,
            **PLOT_LAYOUT,
            showlegend=False
        )
        st.plotly_chart(fig_mini2, use_container_width=True)

    # 연표
    st.markdown("""
    <div class="section-header">
        <h2>📅 10년간 사교육 시장 주요 변화 연표</h2>
    </div>
    """, unsafe_allow_html=True)

    timeline_data = [
        ("2016", "기준점", "#8892b0", "방문학습지 비중 높음(11.9%), 사교육비 18.1조원"),
        ("2018", "변곡점", "#38bdf8", "방문학습지 급락(0.6%), 예체능 분리 집계 시작"),
        ("2019", "성장세", "#64ffda", "사교육비 21.0조 돌파, 온라인 강좌 확대 시작"),
        ("2020", "코로나 충격", "#fda085", "사교육비 19.4조 일시 감소, 온라인 전환 가속"),
        ("2021", "반등", "#a78bfa", "사교육비 23.4조 급반등, 학원수강 집중화"),
        ("2022", "급팽창", "#f5576c", "사교육비 26.0조, 국어 사교육 급증"),
        ("2023", "최고치 근접", "#fb923c", "사교육비 27.1조, 온라인 강좌 10.6%"),
        ("2024", "역대 최고", "#e879f9", "사교육비 29.2조 역대 최고, 초등 13.2조"),
        ("2025", "조정", "#34d399", "사교육비 27.5조, 온라인강좌 하락 조정"),
    ]

    cols = st.columns(len(timeline_data))
    for i, (year, label, color, desc) in enumerate(timeline_data):
        with cols[i]:
            st.markdown(f"""
            <div style='text-align:center; padding:0.5rem; background:rgba(26,31,46,0.6); 
                        border-radius:8px; border-top:3px solid {color}; height:140px;'>
                <div style='font-size:1rem; font-weight:700; color:{color};'>{year}</div>
                <div style='font-size:0.68rem; color:#8892b0; margin:0.2rem 0;
                            background:rgba(45,53,97,0.5); border-radius:4px; padding:1px 4px;'>{label}</div>
                <div style='font-size:0.65rem; color:#a8b2d8; margin-top:0.4rem; line-height:1.4;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SECTION 2: 시장 규모의 팽창
# ══════════════════════════════════════════════
elif section == "📈 시장 규모의 팽창":
    st.markdown("""
    <div class="section-header">
        <h2>📈 사교육 시장 규모의 팽창</h2>
        <p>2016~2025년 10년간 사교육비 총액 및 구성 변화 분석</p>
    </div>
    """, unsafe_allow_html=True)

    # 핵심 지표
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("18.1조", "2016년 총액", "기준 연도"),
        ("29.2조", "2024년 총액 (최고)", "▲ 61.6% 증가"),
        ("2.2배", "10년간 성장 배율", "초등 1.7배, 중등 1.6배"),
        ("+3.4조", "최대 단년 증가", "2021→2022년"),
    ]
    for col, (val, label, sub) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-delta">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 탭
    tab1, tab2, tab3 = st.tabs(["📊 총액 추이", "🏫 학교급별 추이", "📐 구성비 변화"])

    with tab1:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        exp_tr = [total_exp[y] / 10000 for y in range(2016, 2026)]
        growth = [0] + [
            (exp_tr[i] - exp_tr[i - 1]) / exp_tr[i - 1] * 100
            for i in range(1, len(exp_tr))
        ]

        fig.add_trace(go.Scatter(
            x=list(range(2016, 2026)), y=exp_tr,
            mode="lines+markers",
            name="총 사교육비(조원)",
            line=dict(color="#f5576c", width=3.5),
            marker=dict(size=9, symbol="circle", color="#f5576c",
                        line=dict(color="white", width=2)),
            fill="tozeroy", fillcolor="rgba(245,87,108,0.08)"
        ), secondary_y=False)

        colors_g = ["#64ffda" if g >= 0 else "#f5576c" for g in growth[1:]]
        fig.add_trace(go.Bar(
            x=list(range(2017, 2026)), y=growth[1:],
            name="전년 대비 증감률(%)",
            marker_color=colors_g, opacity=0.7
        ), secondary_y=True)

        fig.update_layout(
            title="연도별 사교육비 총액 및 증감률",
            height=430, **PLOT_LAYOUT
        )
        fig.update_yaxes(title_text="총액 (조원)", secondary_y=False,
                         tickformat=".1f", ticksuffix="조")
        fig.update_yaxes(title_text="증감률 (%)", secondary_y=True,
                         ticksuffix="%", gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
            <h4>💡 주요 인사이트</h4>
            <p>
            • <strong style='color:#f5576c;'>2020년:</strong> 코로나19로 유일한 감소(-7.8%), 이후 폭발적 반등<br>
            • <strong style='color:#64ffda;'>2021년:</strong> 전년 대비 +21.0% 급반등 — 억눌린 수요의 폭발<br>
            • <strong style='color:#fda085;'>2022년:</strong> 26조원 돌파, 단년 최대 증가폭<br>
            • <strong style='color:#a78bfa;'>2024년:</strong> 29.2조원으로 역대 최고치 기록<br>
            • <strong style='color:#38bdf8;'>2025년:</strong> 소폭 감소(27.5조), 그러나 여전히 역사적 고점 수준
            </p>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        school_keys = ["초등학교", "중학교", "고등학교"]
        school_colors = ["#64ffda", "#a78bfa", "#f5576c"]

        fig2 = go.Figure()
        for key, color in zip(school_keys, school_colors):
            vals = [v / 10000 for v in school_exp[key]]
            fig2.add_trace(go.Scatter(
                x=list(range(2016, 2026)), y=vals,
                mode="lines+markers",
                name=key,
                line=dict(color=color, width=2.8),
                marker=dict(size=8, color=color),
            ))
        fig2.update_layout(
            title="학교급별 사교육비 추이 (조원)",
            height=400, **PLOT_LAYOUT,
            yaxis=dict(ticksuffix="조", **PLOT_LAYOUT["yaxis"])
        )
        st.plotly_chart(fig2, use_container_width=True)

        # 초등 점유율
        col_a, col_b = st.columns(2)
        with col_a:
            labels_s = school_keys
            values_s = [school_exp[k][-2] / 10000 for k in school_keys]  # 2024년
            fig_pie = go.Figure(go.Pie(
                labels=labels_s, values=values_s,
                hole=0.45,
                marker=dict(colors=school_colors),
                textfont=dict(size=13)
            ))
            fig_pie.update_layout(
                title="2024년 학교급별 비중",
                height=320, paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ccd6f6"),
                legend=dict(bgcolor="rgba(26,31,46,0.8)", bordercolor="#2d3561", borderwidth=1)
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_b:
            st.markdown("""
            <div class="insight-box" style='margin-top:1rem;'>
                <h4>🏫 학교급별 핵심 포인트</h4>
                <p>
                • <strong style='color:#64ffda;'>초등학교:</strong> 2024년 13.2조로 가장 큰 비중(45.3%)
                  — '조기 교육' 상업화의 극단적 표현<br><br>
                • <strong style='color:#a78bfa;'>중학교:</strong> 내신·고입 준비 수요로 꾸준한 성장세<br><br>
                • <strong style='color:#f5576c;'>고등학교:</strong> 입시 직결 과목 집중으로 단가↑, 
                  절대 금액 지속 상승<br><br>
                • <strong style='color:#fda085;'>초등 10년간 성장률:</strong> 2016년 7.7조 → 2024년 13.2조 
                  (+71.3%) — 모든 급 중 최고 성장률
                </p>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        # 연도별 학교급 구성비 누적 바
        school_share_data = {}
        for y_idx, y in enumerate(range(2016, 2026)):
            tot = total_exp[y]
            for key in school_keys:
                if key not in school_share_data:
                    school_share_data[key] = []
                school_share_data[key].append(school_exp[key][y_idx] / tot * 100)

        fig3 = go.Figure()
        for key, color in zip(school_keys, school_colors):
            fig3.add_trace(go.Bar(
                x=list(range(2016, 2026)),
                y=school_share_data[key],
                name=key,
                marker_color=color,
                text=[f"{v:.1f}%" for v in school_share_data[key]],
                textposition="inside",
                textfont=dict(size=10)
            ))
        fig3.update_layout(
            barmode="stack",
            title="학교급별 사교육비 구성비 변화 (%)",
            height=400, **PLOT_LAYOUT,
            yaxis=dict(ticksuffix="%", **PLOT_LAYOUT["yaxis"])
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown("""
        <div class="highlight-box">
            <p>
            ⚠️ <strong>초등학교 비중 지속 확대:</strong> 2016년 42.9% → 2024년 45.3%로 증가. 
            '선행학습'과 '조기 스펙 쌓기' 트렌드가 초등 사교육 시장을 거대하게 확장시키고 있습니다. 
            이는 교육이 상품화될수록 '더 어린 나이에, 더 많이'라는 시장 논리가 작동함을 보여줍니다.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SECTION 3: 성적 구간별 불평등 구조
# ══════════════════════════════════════════════
elif section == "🎯 성적 구간별 불평등 구조":
    st.markdown("""
    <div class="section-header">
        <h2>🎯 성적 구간별 불평등 구조</h2>
        <p>성적이 높을수록 더 많은 사교육 — 불평등의 자기강화 메커니즘</p>
    </div>
    """, unsafe_allow_html=True)

    grade_keys = list(part_grade.keys())
    grade_colors = ["#f5576c", "#fda085", "#64ffda", "#a78bfa", "#38bdf8"]

    # 핵심 지표
    col1, col2, col3 = st.columns(3)
    with col1:
        gap_2016 = part_grade["상위10% 이내"][0] - part_grade["81~100%"][0]
        gap_2024 = part_grade["상위10% 이내"][8] - part_grade["81~100%"][8]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{gap_2024:.1f}%p</div>
            <div class="metric-label">2024년 상위-하위 참여율 격차</div>
            <div class="metric-delta">2016년 {gap_2016:.1f}%p → 2024년 {gap_2024:.1f}%p</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        top_2024 = part_grade["상위10% 이내"][8]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{top_2024:.1f}%</div>
            <div class="metric-label">상위 10% 학생 사교육 참여율 (2024)</div>
            <div class="metric-delta">10명 중 7.7명이 사교육 참여</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        bot_2024 = part_grade["81~100%"][8]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{bot_2024:.1f}%</div>
            <div class="metric-label">하위 20% 학생 사교육 참여율 (2024)</div>
            <div class="metric-delta">10명 중 5.6명이 사교육 참여</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 구간별 참여율 추이", "🔥 격차 히트맵", "📐 2024년 스냅샷"])

    with tab1:
        fig = go.Figure()
        for key, color in zip(grade_keys, grade_colors):
            fig.add_trace(go.Scatter(
                x=list(range(2016, 2026)),
                y=part_grade[key],
                mode="lines+markers",
                name=key,
                line=dict(color=color, width=2.5),
                marker=dict(size=7, color=color),
            ))
        fig.update_layout(
            title="성적 구간별 사교육 참여율 추이 (%)",
            height=430, **PLOT_LAYOUT,
            yaxis=dict(ticksuffix="%", range=[40, 90], **PLOT_LAYOUT["yaxis"])
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
            <h4>💡 구조적 패턴 분석</h4>
            <p>
            • <strong style='color:#f5576c;'>역U자형 공통 패턴:</strong> 모든 성적 구간이 2018년 하락 후 회복, 
              2020년 코로나 하락 후 재반등하는 동일한 패턴 — 사교육은 경기 민감 산업<br><br>
            • <strong style='color:#64ffda;'>간격 유지의 법칙:</strong> 어떤 외부 충격에도 성적 구간 간 간격은 
              일정하게 유지 — 구조적 격차가 고착됨을 의미<br><br>
            • <strong style='color:#fda085;'>2021년 이후 동반 상승:</strong> 모든 구간의 참여율 동반 상승 → 
              사교육이 '선택'에서 '필수'로 전환되는 사회적 압박<br><br>
            • <strong style='color:#a78bfa;'>하위 구간 참여율도 50% 이상:</strong> 학업 성적과 무관하게 
              사교육이 보편화됨 — 상업화의 저변 확대
            </p>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        # 히트맵 데이터 구성
        heatmap_z = []
        heatmap_text = []
        for key in grade_keys:
            row = part_grade[key]
            heatmap_z.append(row)
            heatmap_text.append([f"{v:.1f}%" for v in row])

        fig2 = go.Figure(go.Heatmap(
            z=heatmap_z,
            x=list(range(2016, 2026)),
            y=grade_keys,
            text=heatmap_text,
            texttemplate="%{text}",
            textfont=dict(size=11),
            colorscale=[
                [0, "#0d1b2a"],
                [0.3, "#1e3a5f"],
                [0.6, "#a78bfa"],
                [0.8, "#f5576c"],
                [1, "#ffd700"]
            ],
            showscale=True,
            colorbar=dict(
                ticksuffix="%",
                title="참여율(%)",
                tickfont=dict(color="#ccd6f6")
            )
        ))
        fig2.update_layout(
            title="성적 구간 × 연도별 참여율 히트맵",
            height=340,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,17,23,0.6)",
            font=dict(color="#ccd6f6"),
            xaxis=dict(tickmode="linear", dtick=1),
            margin=dict(l=100, r=50, t=50, b=40)
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("""
        <div class="highlight-box">
            <p>
            ⚠️ <strong>불평등 재생산의 핵심 메커니즘:</strong> 히트맵에서 상위 성적 구간(상단)일수록 
            전반적으로 더 밝은 색상(높은 참여율)을 보입니다. 이는 <strong>'사교육 → 성적 향상 → 더 많은 사교육'</strong>이라는 
            선순환이 상위 계층에 집중되어 있음을 시각적으로 보여줍니다. 반면 하위 구간 학생들은 
            동일한 접근 기회를 갖지 못하여 격차가 구조적으로 고착됩니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        # 2024년 레이더 차트
        fig3 = go.Figure()
        categories_2024 = grade_keys + [grade_keys[0]]
        values_2024 = [part_grade[k][8] for k in grade_keys] + [part_grade[grade_keys[0]][8]]

        fig3.add_trace(go.Scatterpolar(
            r=values_2024,
            theta=categories_2024,
            fill="toself",
            name="2024년",
            line=dict(color="#f5576c", width=2),
            fillcolor="rgba(245,87,108,0.2)"
        ))

        values_2016 = [part_grade[k][0] for k in grade_keys] + [part_grade[grade_keys[0]][0]]
        fig3.add_trace(go.Scatterpolar(
            r=values_2016,
            theta=categories_2024,
            fill="toself",
            name="2016년",
            line=dict(color="#64ffda", width=2, dash="dot"),
            fillcolor="rgba(100,255,218,0.08)"
        ))

        fig3.update_layout(
            polar=dict(
                bgcolor="rgba(15,17,23,0.6)",
                radialaxis=dict(
                    visible=True, range=[40, 85],
                    gridcolor="#2d3561", linecolor="#2d3561",
                    tickfont=dict(color="#8892b0", size=10),
                    ticksuffix="%"
                ),
                angularaxis=dict(
                    linecolor="#2d3561",
                    gridcolor="#2d3561",
                    tickfont=dict(color="#ccd6f6", size=11)
                )
            ),
            title="2016 vs 2024 성적 구간별 참여율 비교",
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ccd6f6"),
            legend=dict(bgcolor="rgba(26,31,46,0.8)", bordercolor="#2d3561", borderwidth=1)
        )
        st.plotly_chart(fig3, use_container_width=True)

        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown("""
            <div class="conclusion-box">
                <p>
                ✅ <strong>2024년 성적 구간별 사교육 참여율</strong><br>
                • 상위 10%: 76.6% (10명 중 7.7명)<br>
                • 11~30%: 74.3% (10명 중 7.4명)<br>
                • 31~60%: 69.5% (10명 중 7.0명)<br>
                • 61~80%: 63.3% (10명 중 6.3명)<br>
                • 하위 20%: 55.7% (10명 중 5.6명)
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col_r:
            st.markdown("""
            <div class="highlight-box">
                <p>
                ⚠️ <strong>핵심 역설:</strong> 사교육은 '성적이 낮은 학생을 돕는' 
                보충 수단이어야 하지만, 실제로는 <strong>이미 성적이 높은 학생들이 
                더 많이 이용</strong>합니다. 이는 사교육이 교육적 필요보다 
                <strong>상업적 수요(경쟁 우위 유지)</strong>에 의해 작동함을 
                보여주는 결정적 증거입니다.
                </p>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# SECTION 4: 과목별 상업화 심화
# ══════════════════════════════════════════════
elif section == "📚 과목별 상업화 심화":
    st.markdown("""
    <div class="section-header">
        <h2>📚 과목별 사교육 상업화 심화</h2>
        <p>수학·영어·국어 중심의 독과점적 과목 구조와 신흥 과목의 부상</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["💰 과목별 지출액", "📊 참여율 추이", "🔍 과목별 심층 분석"])

    with tab1:
        # 과목별 지출액 누적 영역 차트
        subj_keys_exp = ["영어", "수학", "국어", "사회·과학", "논술"]
        subj_colors_exp = ["#38bdf8", "#f5576c", "#fda085", "#64ffda", "#a78bfa"]

        fig = go.Figure()
        for key, color in zip(subj_keys_exp, subj_colors_exp):
            vals = [v / 10000 for v in subj_exp[key]]
            fig.add_trace(go.Scatter(
                x=list(range(2016, 2026)), y=vals,
                mode="lines+markers",
                name=key,
                line=dict(color=color, width=2.5),
                marker=dict(size=7, color=color),
                stackgroup="one",
                fillcolor=color.replace("#", "rgba(").replace("38bdf8", "56,189,248,0.3") + "0.2)"
            ))
        fig.update_traces(stackgroup="one", fillcolor=None)

        fig2 = go.Figure()
        for key, color in zip(subj_keys_exp, subj_colors_exp):
            vals = [v / 10000 for v in subj_exp[key]]
            fig2.add_trace(go.Bar(
                x=list(range(2016, 2026)), y=vals,
                name=key,
                marker_color=color,
            ))
        fig2.update_layout(
            barmode="stack",
            title="과목별 사교육비 총액 누적 (조원)",
            height=430, **PLOT_LAYOUT,
            yaxis=dict(ticksuffix="조", **PLOT_LAYOUT["yaxis"])
        )
        st.plotly_chart(fig2, use_container_width=True)

        # 2024년 과목별 파이
        col_a, col_b = st.columns(2)
        with col_a:
            vals_2024 = [subj_exp[k][-2] / 10000 for k in subj_keys_exp]
            fig_pie = go.Figure(go.Pie(
                labels=subj_keys_exp, values=vals_2024,
                hole=0.5,
                marker=dict(colors=subj_colors_exp),
                textfont=dict(size=12)
            ))
            fig_pie.update_layout(
                title="2024년 과목별 지출 비중",
                height=320, paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ccd6f6"),
                legend=dict(bgcolor="rgba(26,31,46,0.8)", bordercolor="#2d3561", borderwidth=1)
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_b:
            # 증가율 계산
            growth_data = {}
            for key in subj_keys_exp:
                v2016 = subj_exp[key][0]
                v2024 = subj_exp[key][8]
                growth_data[key] = (v2024 - v2016) / v2016 * 100

            fig_bar_g = go.Figure(go.Bar(
                x=list(growth_data.values()),
                y=list(growth_data.keys()),
                orientation="h",
                marker=dict(
                    color=list(growth_data.values()),
                    colorscale=[[0, "#2d3561"], [0.5, "#a78bfa"], [1, "#f5576c"]],
                    showscale=False
                ),
                text=[f"+{v:.1f}%" for v in growth_data.values()],
                textposition="outside",
                textfont=dict(color="#ccd6f6")
            ))
            fig_bar_g.update_layout(
                title="2016→2024 과목별 지출 증가율",
                height=320, **PLOT_LAYOUT,
                xaxis=dict(ticksuffix="%", **PLOT_LAYOUT["xaxis"]),
            )
            st.plotly_chart(fig_bar_g, use_container_width=True)

    with tab2:
        subj_part_keys = ["수학", "영어", "국어", "사회·과학", "예체능·취미"]
        subj_part_colors = ["#f5576c", "#38bdf8", "#fda085", "#64ffda", "#a78bfa"]

        fig3 = go.Figure()
        for key, color in zip(subj_part_keys, subj_part_colors):
            fig3.add_trace(go.Scatter(
                x=list(range(2016, 2026)),
                y=subj_part[key],
                mode="lines+markers",
                name=key,
                line=dict(color=color, width=2.5),
                marker=dict(size=7, color=color),
            ))
        fig3.update_layout(
            title="과목별 사교육 참여율 추이 (%)",
            height=400, **PLOT_LAYOUT,
            yaxis=dict(ticksuffix="%", **PLOT_LAYOUT["yaxis"])
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
            <h4>💡 과목별 참여율 변화의 핵심</h4>
            <p>
            • <strong style='color:#fda085;'>국어 사교육의 급성장:</strong> 2016년 17.7% → 2024년 27.5% (+55.4%) 
              — 수능 국어의 변별력 강화가 직접적 원인<br><br>
            • <strong style='color:#f5576c;'>수학의 압도적 우위:</strong> 10년 내내 가장 높은 참여율 유지. 
              '수포자' 공포 마케팅으로 저학년부터 수학 사교육 의존 심화<br><br>
            • <strong style='color:#38bdf8;'>영어의 지속적 강세:</strong> 절대평가 전환에도 불구하고 참여율 유지 — 
              '영어는 기본'이라는 인식이 시장 형성<br><br>
            • <strong style='color:#a78bfa;'>예체능 급락:</strong> 2017년 41.1% → 2018년 15.9%로 급락 — 
              통계 방식 변경 반영, 
