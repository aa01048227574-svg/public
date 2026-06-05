import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time

# ─────────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="환승 타임라인 분석기",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# 커스텀 CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

/* 배경 */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0f172a 40%, #0a1628 100%);
    min-height: 100vh;
}

/* 상단 헤더 배너 */
.hero-banner {
    background: linear-gradient(90deg, #1e3a5f 0%, #0f2744 50%, #162035 100%);
    border: 1px solid #1e4080;
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 240px; height: 240px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(56,182,255,0.12) 0%, transparent 70%);
}
.hero-title {
    font-size: 2.0rem;
    font-weight: 900;
    color: #e2f0ff;
    letter-spacing: -0.5px;
    margin: 0 0 6px 0;
}
.hero-subtitle {
    font-size: 0.95rem;
    color: #7fa8d0;
    margin: 0;
    font-weight: 300;
}
.hero-badge {
    display: inline-block;
    background: rgba(56,182,255,0.15);
    border: 1px solid rgba(56,182,255,0.35);
    color: #38b6ff;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 4px 10px;
    border-radius: 20px;
    margin-bottom: 14px;
    font-family: 'Space Mono', monospace;
}

/* 사이드바 */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2e 0%, #0a1422 100%) !important;
    border-right: 1px solid #1a3050 !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stTextInput label,
[data-testid="stSidebar"] .stTimeInput label {
    color: #7fa8d0 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #c8dff0 !important;
}
[data-testid="stSidebarContent"] {
    padding: 1.5rem 1.2rem !important;
}

/* 메트릭 카드 */
.metric-card {
    background: linear-gradient(135deg, #111f35 0%, #0d1929 100%);
    border: 1px solid #1a3555;
    border-radius: 14px;
    padding: 22px 24px;
    text-align: center;
    transition: border-color 0.25s, transform 0.2s;
    height: 100%;
}
.metric-card:hover {
    border-color: #2a5f9f;
    transform: translateY(-2px);
}
.metric-icon {
    font-size: 1.6rem;
    margin-bottom: 8px;
}
.metric-label {
    font-size: 0.78rem;
    color: #5a85ab;
    font-weight: 500;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 900;
    color: #e2f0ff;
    font-family: 'Space Mono', monospace;
    line-height: 1.1;
}
.metric-unit {
    font-size: 0.85rem;
    color: #4a7fa5;
    font-weight: 400;
}
.metric-highlight {
    border-color: #1a6aad;
    background: linear-gradient(135deg, #0d2240 0%, #0a1a30 100%);
}
.metric-highlight .metric-value {
    color: #38b6ff;
}

/* 섹션 헤더 */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 28px 0 16px 0;
}
.section-header-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1a3555, transparent);
}
.section-title {
    color: #8ab4d4;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-family: 'Space Mono', monospace;
    white-space: nowrap;
}

/* 최적 환승 배너 */
.best-transfer-box {
    background: linear-gradient(135deg, #0a2540 0%, #0a1f38 100%);
    border: 1.5px solid #1a5080;
    border-left: 4px solid #38b6ff;
    border-radius: 12px;
    padding: 20px 26px;
    margin: 16px 0;
}
.best-transfer-title {
    color: #38b6ff;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
    font-family: 'Space Mono', monospace;
}
.best-transfer-time {
    font-size: 2.6rem;
    font-weight: 900;
    color: #e2f0ff;
    font-family: 'Space Mono', monospace;
    line-height: 1;
}
.best-transfer-sub {
    color: #5a8ab0;
    font-size: 0.88rem;
    margin-top: 6px;
}

/* 타임라인 */
.timeline-row {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 16px 0;
    border-bottom: 1px solid #1a2f4a;
}
.timeline-dot {
    width: 12px; height: 12px;
    border-radius: 50%;
    margin-top: 5px;
    flex-shrink: 0;
}
.timeline-content { flex: 1; }
.timeline-time {
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
    font-weight: 700;
    color: #38b6ff;
}
.timeline-desc {
    font-size: 0.88rem;
    color: #8ab4d4;
    margin-top: 2px;
}

/* 데이터 테이블 스타일 */
.stDataFrame {
    background: transparent !important;
}

/* 버튼 */
.stButton > button {
    background: linear-gradient(135deg, #1a4f8a 0%, #0f3a6e 100%) !important;
    color: #e2f0ff !important;
    border: 1px solid #2a6ab0 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.2s !important;
    letter-spacing: 0.5px !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2060a8 0%, #1a4f8a 100%) !important;
    border-color: #38b6ff !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(56,182,255,0.2) !important;
}

/* selectbox / input */
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stTimeInput > div > div > input {
    background: #0d1929 !important;
    border-color: #1a3555 !important;
    color: #c8dff0 !important;
    border-radius: 8px !important;
}

/* 알림 박스 */
.info-box {
    background: rgba(56,182,255,0.06);
    border: 1px solid rgba(56,182,255,0.2);
    border-radius: 10px;
    padding: 14px 18px;
    margin: 12px 0;
    color: #8ab4d4;
    font-size: 0.87rem;
    line-height: 1.6;
}

/* 탭 */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1929 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #5a85ab !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    background: #1a3d6e !important;
    color: #38b6ff !important;
}

/* 구분선 */
hr { border-color: #1a3050 !important; }

/* spinner */
.stSpinner > div { border-top-color: #38b6ff !important; }

/* progress */
.stProgress > div > div {
    background: linear-gradient(90deg, #1a4f8a, #38b6ff) !important;
    border-radius: 4px !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 핵심 로직
# ─────────────────────────────────────────────
STATION_PRESETS = {
    "강남역": {"base_add": 5, "lat": 37.498, "lon": 127.028},
    "잠실역": {"base_add": 15, "lat": 37.513, "lon": 127.100},
    "홍대입구역": {"base_add": 8, "lat": 37.557, "lon": 126.924},
    "신촌역": {"base_add": 10, "lat": 37.555, "lon": 126.937},
    "신림역": {"base_add": 12, "lat": 37.484, "lon": 126.929},
    "서울역": {"base_add": 3, "lat": 37.555, "lon": 126.972},
    "종로3가역": {"base_add": 6, "lat": 37.571, "lon": 126.992},
    "건대입구역": {"base_add": 14, "lat": 37.540, "lon": 127.070},
    "신도림역": {"base_add": 9, "lat": 37.508, "lon": 126.891},
    "직접 입력": {"base_add": 10, "lat": None, "lon": None},
}

ROUTE_PRESETS = {
    "2호선 지하철": {"type": "subway", "color": "#00a651", "icon": "🟢"},
    "1호선 지하철": {"type": "subway", "color": "#0052a4", "icon": "🔵"},
    "3호선 지하철": {"type": "subway", "color": "#ef7c1c", "icon": "🟠"},
    "4호선 지하철": {"type": "subway", "color": "#00a4e3", "icon": "🩵"},
    "9호선 지하철": {"type": "subway", "color": "#a17600", "icon": "🟡"},
    "146번 버스": {"type": "bus", "color": "#e8403a", "icon": "🔴"},
    "360번 버스": {"type": "bus", "color": "#e8403a", "icon": "🔴"},
    "740번 버스": {"type": "bus", "color": "#e8403a", "icon": "🔴"},
    "직접 입력": {"type": "bus", "color": "#888", "icon": "🚌"},
}

def calculate_travel_time(station_name: str, route_name: str, hour: int) -> int:
    base = 20
    preset = STATION_PRESETS.get(station_name, {"base_add": 10})
    base += preset["base_add"]
    if "버스" in route_name:
        # 출퇴근 시간대 정체 반영
        if 7 <= hour <= 9:
            base += 15
        elif 17 <= hour <= 20:
            base += 12
        else:
            base += 5
    return base

def get_congestion(route_name: str, hour: int) -> int:
    is_rush = 7 <= hour <= 9 or 17 <= hour <= 20
    if "2호선" in route_name or "146" in route_name:
        return 95000 if is_rush else 55000
    if "1호선" in route_name or "360" in route_name:
        return 80000 if is_rush else 45000
    if "9호선" in route_name:
        return 110000 if is_rush else 60000
    if "버스" in route_name:
        return 70000 if is_rush else 35000
    return 50000

def congestion_label(load: int) -> tuple[str, str]:
    if load >= 95000:
        return "매우 혼잡", "#ff4b4b"
    elif load >= 70000:
        return "혼잡", "#ff9f43"
    elif load >= 45000:
        return "보통", "#ffd32a"
    else:
        return "여유", "#0be881"

def run_analysis(from_station: str, from_route: str,
                 start_time_str: str, to_route: str) -> tuple[pd.DataFrame, pd.Series, int]:
    start_time = datetime.strptime(start_time_str, "%H:%M")
    travel_min = calculate_travel_time(from_station, from_route, start_time.hour)
    drop_time = start_time + timedelta(minutes=travel_min)
    drop_str = drop_time.strftime("%H:%M")

    offsets = [5, 10, 15, 20, 25, 30]
    rows = []
    for offset in offsets:
        t = drop_time + timedelta(minutes=offset)
        load = get_congestion(to_route, t.hour)
        weight = 0.65 if offset in [10, 15] else (0.85 if offset == 20 else 1.1)
        predicted = int(load * weight)
        label, color = congestion_label(predicted)
        discomfort = int((predicted * 0.002) + (offset * 1.2))
        rows.append({
            "출발지": from_station,
            "이용 수단": from_route,
            "출발 시각": start_time_str,
            "예측 하차 시각": drop_str,
            "환승 수단": to_route,
            "추천 탑승 시각": t.strftime("%H:%M"),
            "대기 시간": f"{offset}분",
            "예측 혼잡도": predicted,
            "혼잡 등급": label,
            "종합 불편 지수": discomfort,
        })

    df = pd.DataFrame(rows)
    best = df.loc[df["종합 불편 지수"].idxmin()]
    return df, best, travel_min


# ─────────────────────────────────────────────
# 사이드바 입력 UI
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 8px 0 20px 0;">
        <div style="font-size:2.2rem;">🚇</div>
        <div style="color:#38b6ff; font-weight:700; font-size:1.05rem; letter-spacing:1px;">환승 분석기</div>
        <div style="color:#3a6585; font-size:0.75rem; margin-top:4px;">Transit Timeline Optimizer</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 출발 정보")

    station_choice = st.selectbox("출발역 / 정류장", list(STATION_PRESETS.keys()), index=0)
    if station_choice == "직접 입력":
        from_station = st.text_input("역/정류장명 직접 입력", placeholder="예: 합정역")
    else:
        from_station = station_choice

    route_choice = st.selectbox("이용 교통수단", list(ROUTE_PRESETS.keys()), index=0)
    if route_choice == "직접 입력":
        from_route = st.text_input("교통수단 직접 입력", placeholder="예: 750번 버스")
    else:
        from_route = route_choice

    start_time = st.time_input("출발 시각", value=datetime.strptime("08:00", "%H:%M").time())
    start_time_str = start_time.strftime("%H:%M")

    st.markdown("### 환승 정보")
    to_choice = st.selectbox("환승할 교통수단", list(ROUTE_PRESETS.keys()), index=5)
    if to_choice == "직접 입력":
        to_route = st.text_input("환승 수단 직접 입력", placeholder="예: 472번 버스")
    else:
        to_route = to_choice

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("🔍  환승 타임라인 분석", use_container_width=True)

    st.markdown("""
    <div class="info-box" style="margin-top:20px;">
    ℹ️ 실시간 혼잡도 + 시간대별 정체 패턴을 반영하여 최적 환승 시각을 추천합니다.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 메인 영역
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">🚉 TRANSIT TIMELINE OPTIMIZER</div>
    <div class="hero-title">스마트 환승 타임라인 분석기</div>
    <div class="hero-subtitle">출발지 · 교통수단 · 시간대를 입력하면 최적 환승 시각과 혼잡도 예측을 제공합니다</div>
</div>
""", unsafe_allow_html=True)

# 분석 전 안내
if not run_btn:
    st.markdown("""
    <div style="text-align:center; padding: 60px 0 40px 0;">
        <div style="font-size:3.5rem; margin-bottom:16px;">🗺️</div>
        <div style="color:#4a7fa5; font-size:1.05rem; font-weight:500;">왼쪽 사이드바에서 출발 정보를 입력하고</div>
        <div style="color:#2a5a7a; font-size:0.9rem; margin-top:6px;">분석 버튼을 누르면 환승 타임라인이 생성됩니다</div>
    </div>
    """, unsafe_allow_html=True)

    # 사용 가이드
    col1, col2, col3 = st.columns(3)
    for col, icon, title, desc in [
        (col1, "1️⃣", "출발 정보 입력", "출발역과 이용 교통수단,\n출발 시각을 선택하세요"),
        (col2, "2️⃣", "환승 수단 선택", "갈아탈 버스 또는\n지하철 노선을 고르세요"),
        (col3, "3️⃣", "타임라인 확인", "최적 환승 시각과\n혼잡도 예측을 확인하세요"),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card" style="padding:28px 20px;">
                <div style="font-size:1.8rem; margin-bottom:10px;">{icon}</div>
                <div style="color:#c8dff0; font-weight:700; font-size:0.95rem; margin-bottom:6px;">{title}</div>
                <div style="color:#4a7fa5; font-size:0.82rem; line-height:1.6; white-space:pre-line;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

else:
    # ── 분석 실행 ──
    with st.spinner("경로 및 혼잡도 데이터 연산 중..."):
        prog = st.progress(0)
        for i in range(1, 101):
            time.sleep(0.008)
            prog.progress(i)
        df, best, travel_min = run_analysis(from_station, from_route, start_time_str, to_route)
        prog.empty()

    start_dt = datetime.strptime(start_time_str, "%H:%M")
    drop_dt = start_dt + timedelta(minutes=travel_min)
    best_dt = datetime.strptime(best["추천 탑승 시각"], "%H:%M")

    # ── 상단 메트릭 카드 ──
    st.markdown("""
    <div class="section-header">
        <span class="section-title">핵심 지표</span>
        <div class="section-header-line"></div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "🚶", "이동 소요 시간", f"{travel_min}", "분", False),
        (c2, "🕐", "예측 하차 시각", drop_dt.strftime("%H:%M"), "", False),
        (c3, "✅", "최적 환승 시각", best["추천 탑승 시각"], "", True),
        (c4, "⏳", "최소 환승 대기", best["대기 시간"], "", False),
    ]
    for col, icon, label, val, unit, highlight in cards:
        with col:
            cls = "metric-card metric-highlight" if highlight else "metric-card"
            st.markdown(f"""
            <div class="{cls}">
                <div class="metric-icon">{icon}</div>
                <div class="metric-label">{label}</div>
                <div class="metric-value">{val}<span class="metric-unit"> {unit}</span></div>
            </div>
            """, unsafe_allow_html=True)

    # ── 탭 레이아웃 ──
    tab1, tab2, tab3 = st.tabs(["📊  혼잡도 분석", "⏱  타임라인", "📋  상세 데이터"])

    # ───── TAB 1: 차트 ─────
    with tab1:
        col_l, col_r = st.columns([3, 2])

        with col_l:
            # 혼잡도 바 차트
            colors = []
            for _, row in df.iterrows():
                if row["추천 탑승 시각"] == best["추천 탑승 시각"]:
                    colors.append("#38b6ff")
                elif row["혼잡 등급"] == "매우 혼잡":
                    colors.append("#ff4b4b")
                elif row["혼잡 등급"] == "혼잡":
                    colors.append("#ff9f43")
                elif row["혼잡 등급"] == "보통":
                    colors.append("#ffd32a")
                else:
                    colors.append("#0be881")

            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=df["추천 탑승 시각"],
                y=df["예측 혼잡도"],
                marker_color=colors,
                text=[f"{v:,}" for v in df["예측 혼잡도"]],
                textposition="outside",
                textfont=dict(color="#8ab4d4", size=11, family="Space Mono"),
                hovertemplate="<b>%{x}</b><br>혼잡도: %{y:,}<br><extra></extra>",
            ))
            fig_bar.add_annotation(
                x=best["추천 탑승 시각"], y=best["예측 혼잡도"],
                text="⭐ 최적",
                showarrow=True, arrowhead=2,
                arrowcolor="#38b6ff", font=dict(color="#38b6ff", size=12, family="Noto Sans KR"),
                ay=-40, ax=0,
            )
            fig_bar.update_layout(
                title=dict(text="환승 시각별 예측 혼잡도", font=dict(color="#8ab4d4", size=14, family="Noto Sans KR")),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(13,25,41,0.6)",
                font=dict(color="#8ab4d4", family="Noto Sans KR"),
                xaxis=dict(gridcolor="#1a3050", tickfont=dict(family="Space Mono", size=11)),
                yaxis=dict(gridcolor="#1a3050", title="유동 인구 (명)"),
                margin=dict(t=50, b=30, l=10, r=10),
                height=300,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_r:
            # 불편 지수 레이더/라인
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=df["추천 탑승 시각"], y=df["종합 불편 지수"],
                mode="lines+markers",
                line=dict(color="#38b6ff", width=2.5),
                marker=dict(size=9, color=["#38b6ff" if t == best["추천 탑승 시각"] else "#1a4a7a"
                                            for t in df["추천 탑승 시각"]],
                            line=dict(color="#38b6ff", width=2)),
                fill="tozeroy",
                fillcolor="rgba(56,182,255,0.06)",
                hovertemplate="<b>%{x}</b><br>불편 지수: %{y}<extra></extra>",
            ))
            fig_line.update_layout(
                title=dict(text="종합 불편 지수", font=dict(color="#8ab4d4", size=14, family="Noto Sans KR")),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(13,25,41,0.6)",
                font=dict(color="#8ab4d4", family="Noto Sans KR"),
                xaxis=dict(gridcolor="#1a3050", tickfont=dict(family="Space Mono", size=11)),
                yaxis=dict(gridcolor="#1a3050"),
                margin=dict(t=50, b=30, l=10, r=10),
                height=300,
            )
            st.plotly_chart(fig_line, use_container_width=True)

        # 혼잡도 등급별 현황
        st.markdown("""
        <div class="section-header">
            <span class="section-title">혼잡도 범례</span>
            <div class="section-header-line"></div>
        </div>
        """, unsafe_allow_html=True)
        lg1, lg2, lg3, lg4 = st.columns(4)
        for col, label, color, desc in [
            (lg1, "여유", "#0be881", "< 45,000명"),
            (lg2, "보통", "#ffd32a", "45,000 ~ 70,000명"),
            (lg3, "혼잡", "#ff9f43", "70,000 ~ 95,000명"),
            (lg4, "매우 혼잡", "#ff4b4b", "> 95,000명"),
        ]:
            with col:
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:10px; padding:10px 14px;
                            background:#0d1929; border:1px solid #1a3050; border-radius:8px;">
                    <div style="width:12px;height:12px;border-radius:50%;background:{color};flex-shrink:0;"></div>
                    <div>
                        <div style="color:{color}; font-weight:700; font-size:0.82rem;">{label}</div>
                        <div style="color:#3a6585; font-size:0.75rem; font-family:Space Mono;">{desc}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ───── TAB 2: 타임라인 ─────
    with tab2:
        col_tl, col_best = st.columns([3, 2])

        with col_tl:
            st.markdown("""
            <div class="section-header">
                <span class="section-title">이동 타임라인</span>
                <div class="section-header-line"></div>
            </div>
            """, unsafe_allow_html=True)

            route_info = ROUTE_PRESETS.get(from_route, {"color": "#888", "icon": "🚌"})
            to_info = ROUTE_PRESETS.get(to_route, {"color": "#888", "icon": "🚌"})

            events = [
                ("#0be881", start_time_str, f"🏁 {from_station} 출발", f"{from_route} 탑승"),
                (route_info["color"], drop_dt.strftime("%H:%M"), f"🚉 환승역 도착 (이동 {travel_min}분)", f"{from_route} 하차"),
                ("#ffd32a", (drop_dt + timedelta(minutes=int(best['대기 시간'].replace('분','')))).strftime("%H:%M"),
                 f"⭐ 최적 환승 시각", f"{to_route} 탑승 — 대기 {best['대기 시간']}"),
            ]

            for color, ttime, title, desc in events:
                st.markdown(f"""
                <div class="timeline-row">
                    <div class="timeline-dot" style="background:{color};box-shadow:0 0 8px {color}55;"></div>
                    <div class="timeline-content">
                        <div class="timeline-time">{ttime}</div>
                        <div style="color:#c8dff0; font-weight:600; font-size:0.9rem; margin-top:2px;">{title}</div>
                        <div class="timeline-desc">{desc}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with col_best:
            label, lcolor = congestion_label(int(best["예측 혼잡도"]))
            st.markdown(f"""
            <div class="best-transfer-box">
                <div class="best-transfer-title">✅ 최적 환승 추천</div>
                <div class="best-transfer-time">{best["추천 탑승 시각"]}</div>
                <div class="best-transfer-sub">대기 시간 {best['대기 시간']} 후 탑승</div>
                <hr style="border-color:#1a3a5a; margin:14px 0;">
                <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                    <span style="color:#5a85ab; font-size:0.82rem;">예측 혼잡도</span>
                    <span style="color:{lcolor}; font-weight:700; font-size:0.85rem;">{label}</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                    <span style="color:#5a85ab; font-size:0.82rem;">불편 지수</span>
                    <span style="color:#e2f0ff; font-weight:700; font-family:Space Mono; font-size:0.85rem;">{int(best['종합 불편 지수'])}</span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#5a85ab; font-size:0.82rem;">환승 수단</span>
                    <span style="color:#8ab4d4; font-size:0.82rem;">{to_route}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 시간대 경고
            h = start_dt.hour
            if 7 <= h <= 9:
                st.markdown("""
                <div class="info-box" style="border-color:rgba(255,155,67,0.4); background:rgba(255,155,67,0.06);">
                ⚠️ <b>출근 피크타임</b> — 평소보다 혼잡도가 높습니다. 10~15분 일찍 출발하는 것을 권장합니다.
                </div>
                """, unsafe_allow_html=True)
            elif 17 <= h <= 20:
                st.markdown("""
                <div class="info-box" style="border-color:rgba(255,155,67,0.4); background:rgba(255,155,67,0.06);">
                ⚠️ <b>퇴근 피크타임</b> — 버스/지하철 모두 혼잡합니다. 여유 대기 시간을 확보하세요.
                </div>
                """, unsafe_allow_html=True)

    # ───── TAB 3: 데이터 테이블 ─────
    with tab3:
        st.markdown("""
        <div class="section-header">
            <span class="section-title">전체 환승 옵션 데이터</span>
            <div class="section-header-line"></div>
        </div>
        """, unsafe_allow_html=True)

        display_df = df[["추천 탑승 시각", "대기 시간", "예측 혼잡도", "혼잡 등급", "종합 불편 지수"]].copy()

        def highlight_best(row):
            if row["추천 탑승 시각"] == best["추천 탑승 시각"]:
                return ["background-color: rgba(56,182,255,0.12); color: #38b6ff; font-weight:700;"] * len(row)
            return [""] * len(row)

        def color_congestion(val):
            if val == "매우 혼잡": return "color: #ff4b4b; font-weight:700;"
            if val == "혼잡": return "color: #ff9f43; font-weight:700;"
            if val == "보통": return "color: #ffd32a;"
            if val == "여유": return "color: #0be881;"
            return ""

        styled = (display_df.style
          .apply(highlight_best, axis=1)
          .map(color_congestion, subset=["혼잡 등급"]) # 👈 .applymap을 .map으로 변경
          .format({"예측 혼잡도": "{:,}", "종합 불편 지수": "{:.0f}"}))

        st.dataframe(styled, use_container_width=True, height=300)

        # CSV 다운로드
        csv = df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="📥  분석 데이터 CSV 다운로드",
            data=csv,
            file_name=f"transit_analysis_{from_station}_{start_time_str.replace(':','')}.csv",
            mime="text/csv",
        )

# ── 푸터 ──
st.markdown("""
<hr>
<div style="text-align:center; color:#2a4a65; font-size:0.78rem; padding:10px 0 20px 0; font-family:Space Mono;">
    Transit Timeline Optimizer · Powered by Streamlit
</div>
""", unsafe_allow_html=True)
