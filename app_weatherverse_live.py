

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json
import urllib.parse
import urllib.request
from datetime import datetime

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="WeatherVerse | Weather Analytics",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- ANIMATED BACKGROUND ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

.stApp {
    background: linear-gradient(125deg, #07152e, #101d46, #28205a, #102d50);
    background-size: 300% 300%;
    animation: skyShift 18s ease infinite;
    color: #f5f7ff;
    font-family: 'Inter', sans-serif;
}

@keyframes skyShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp::before, .stApp::after {
    content: "";
    position: fixed;
    width: 340px;
    height: 340px;
    border-radius: 50%;
    filter: blur(100px);
    opacity: 0.25;
    pointer-events: none;
    z-index: 0;
}

.stApp::before {
    background: #399dff;
    top: 10%;
    left: -130px;
    animation: floatLight 15s ease-in-out infinite alternate;
}

.stApp::after {
    background: #a855f7;
    bottom: 0;
    right: -120px;
    animation: floatLight 18s ease-in-out infinite alternate-reverse;
}

@keyframes floatLight {
    from { transform: translate(0, 0); }
    to { transform: translate(90px, -70px); }
}

/* Gentle drifting clouds and tiny glowing particles */
.weather-atmosphere {
    position: fixed;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
    z-index: 0;
    isolation: isolate;
}
.weather-atmosphere .drift-cloud {
    position: absolute;
    width: 150px;
    height: 42px;
    border-radius: 999px;
    background: rgba(190, 222, 255, 0.035);
    filter: blur(1px);
    box-shadow: 0 0 26px rgba(112, 190, 255, 0.045);
    will-change: transform;
}
.weather-atmosphere .drift-cloud::before,
.weather-atmosphere .drift-cloud::after {
    content: "";
    position: absolute;
    border-radius: 50%;
    background: inherit;
}
.weather-atmosphere .drift-cloud::before {
    width: 62px;
    height: 62px;
    left: 22px;
    top: -25px;
}
.weather-atmosphere .drift-cloud::after {
    width: 82px;
    height: 78px;
    left: 62px;
    top: -39px;
}
.cloud-one {
    top: 17%;
    left: -190px;
    animation: cloudDriftOne 58s linear infinite;
}
.cloud-two {
    top: 49%;
    left: -220px;
    opacity: 0.42;
    transform: scale(0.72);
    animation: cloudDriftTwo 76s linear infinite;
    animation-delay: -23s;
}
.cloud-three {
    top: 76%;
    left: -200px;
    opacity: 0.32;
    transform: scale(0.9);
    animation: cloudDriftThree 68s linear infinite;
    animation-delay: -41s;
}
@keyframes cloudDriftOne {
    from { transform: translateX(0) scale(1); }
    to { transform: translateX(calc(100vw + 420px)) scale(1); }
}
@keyframes cloudDriftTwo {
    from { transform: translateX(0) scale(0.72); }
    to { transform: translateX(calc(100vw + 440px)) scale(0.72); }
}
@keyframes cloudDriftThree {
    from { transform: translateX(0) scale(0.9); }
    to { transform: translateX(calc(100vw + 430px)) scale(0.9); }
}
.weather-spark {
    position: absolute;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #c8f6ff;
    box-shadow: 0 0 11px 3px rgba(108, 218, 255, 0.72);
    opacity: 0;
    animation: sparkFloat 7s ease-in-out infinite;
}
.spark-one { left: 16%; top: 72%; animation-delay: 0s; }
.spark-two { left: 32%; top: 28%; animation-delay: 1.8s; }
.spark-three { left: 51%; top: 81%; animation-delay: 3.2s; }
.spark-four { left: 68%; top: 38%; animation-delay: 2.5s; }
.spark-five { left: 82%; top: 66%; animation-delay: 4.1s; }
.spark-six { left: 91%; top: 19%; animation-delay: 5.2s; }
.spark-seven { left: 24%; top: 48%; animation-delay: 2.1s; }
.spark-eight { left: 43%; top: 16%; animation-delay: 4.4s; }
.spark-nine { left: 59%; top: 61%; animation-delay: 1.1s; }
.spark-ten { left: 74%; top: 84%; animation-delay: 3.7s; }
.spark-eleven { left: 8%; top: 34%; animation-delay: 5.8s; }
.spark-twelve { left: 96%; top: 52%; animation-delay: 2.9s; }
@keyframes sparkFloat {
    0%, 100% { opacity: 0; transform: translateY(12px) scale(0.7); }
    25%, 70% { opacity: 0.9; }
    50% { opacity: 1; transform: translateY(-26px) scale(1.3); }
}
@media (prefers-reduced-motion: reduce) {
    .stApp, .stApp::before, .stApp::after,
    .weather-atmosphere .drift-cloud, .weather-spark, .hero-icon {
        animation: none !important;
    }
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: transparent;
}

[data-testid="stHeader"] {
    background: rgba(5, 12, 30, 0.3);
}

.block-container {
    position: relative;
    z-index: 1;
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

.hero {
    padding: 35px;
    border-radius: 25px;
    background: linear-gradient(115deg,
        rgba(44,105,190,0.36),
        rgba(130,76,210,0.30),
        rgba(25,184,210,0.16));
    border: 1px solid rgba(255,255,255,0.19);
    box-shadow: 0 18px 55px rgba(0,0,0,0.22);
    backdrop-filter: blur(15px);
    margin-bottom: 25px;
}

.hero h1 {
    font-size: clamp(30px, 4vw, 48px);
    font-weight: 800;
    color: white;
    line-height: 1.2;
    margin: 8px 0 12px 0;
}

.hero p {
    color: #d9e7ff;
    font-size: 16px;
    line-height: 1.7;
}

.eyebrow {
    color: #8fe8ff;
    font-weight: 700;
    letter-spacing: 3px;
    font-size: 12px;
}

.hero-icon {
    font-size: 75px;
    text-align: center;
    animation: weatherFloat 4s ease-in-out infinite;
}

@keyframes weatherFloat {
    0%, 100% { transform: translateY(0) rotate(-4deg); }
    50% { transform: translateY(-13px) rotate(4deg); }
}

h2, h3 {
    color: #f3f6ff !important;
}

.section-label {
    color: #9de9ff;
    font-size: 12px;
    letter-spacing: 2px;
    font-weight: 700;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg,
        rgba(255,255,255,0.11),
        rgba(255,255,255,0.035));
    border: 1px solid rgba(255,255,255,0.16);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.12);
    transition: transform 0.25s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: rgba(113,216,255,0.65);
}

[data-testid="stMetricLabel"] {
    color: #c2d4f4 !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
    font-weight: 800;
}

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.055);
    border: 1px dashed rgba(135,210,255,0.55);
    border-radius: 18px;
    padding: 12px;
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px;
}

.stSelectbox label {
    color: #dce8ff !important;
}

.stButton button, .stDownloadButton button {
    border-radius: 12px;
    border: 1px solid rgba(130,210,255,0.4);
    background: linear-gradient(100deg, #2678d8, #7952cf);
    color: white;
    font-weight: 700;
    transition: all 0.2s ease;
}

.stButton button:hover, .stDownloadButton button:hover {
    border-color: #a6f0ff;
    transform: translateY(-2px);
}

hr {
    border-color: rgba(255,255,255,0.15);
}

#MainMenu, footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SUBTLE WEATHER ANIMATION LAYER ----------------
# Decorative only: it sits behind the dashboard and never blocks clicks.
st.markdown("""
<div class="weather-atmosphere" aria-hidden="true">
    <div class="drift-cloud cloud-one"></div>
    <div class="drift-cloud cloud-two"></div>
    <div class="drift-cloud cloud-three"></div>
    <div class="weather-spark spark-one"></div>
    <div class="weather-spark spark-two"></div>
    <div class="weather-spark spark-three"></div>
    <div class="weather-spark spark-four"></div>
    <div class="weather-spark spark-five"></div>
    <div class="weather-spark spark-six"></div>
    <div class="weather-spark spark-seven"></div>
    <div class="weather-spark spark-eight"></div>
    <div class="weather-spark spark-nine"></div>
    <div class="weather-spark spark-ten"></div>
    <div class="weather-spark spark-eleven"></div>
    <div class="weather-spark spark-twelve"></div>
</div>
""", unsafe_allow_html=True)

# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero">
    <div class="eyebrow">✦ SMART WEATHER ANALYTICS PLATFORM</div>
    <h1>WeatherVerse 🌦️</h1>
    <p>
        Explore the atmosphere through data. Discover weather patterns,
        analyze temperature trends, and visualize the story behind your data.
    </p>
    <div style="color:#a8eaff;font-size:13px;">
        ● DATA ANALYSIS &nbsp; ● INTERACTIVE VISUALIZATION
        &nbsp; ● WEATHER INSIGHTS
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🌤️ WeatherVerse")
    st.caption("Your personal weather analytics studio")
    st.divider()

    uploaded_file = st.file_uploader(
        "📂 Upload weather CSV",
        type=["csv"]
    )

    st.markdown("### Dashboard")
    st.caption("Upload your own dataset to analyze real observations.")
    st.divider()
    st.caption("Built with Python · Pandas · Plotly · Streamlit")


# ---------------- LIVE WEATHERVERSE: LOCATION, FORECAST & MAP ----------------
# Uses the Open-Meteo public API. No API key is required for this demo.
# Network calls are cached to avoid repeatedly querying the service on reruns.
WEATHER_CODES = {
    0: ("Clear sky", "sun"), 1: ("Mainly clear", "sun"),
    2: ("Partly cloudy", "cloud"), 3: ("Overcast", "cloud"),
    45: ("Fog", "fog"), 48: ("Depositing rime fog", "fog"),
    51: ("Light drizzle", "rain"), 53: ("Drizzle", "rain"), 55: ("Dense drizzle", "rain"),
    56: ("Freezing drizzle", "rain"), 57: ("Heavy freezing drizzle", "rain"),
    61: ("Light rain", "rain"), 63: ("Rain", "rain"), 65: ("Heavy rain", "rain"),
    66: ("Freezing rain", "rain"), 67: ("Heavy freezing rain", "rain"),
    71: ("Light snow", "snow"), 73: ("Snow", "snow"), 75: ("Heavy snow", "snow"),
    77: ("Snow grains", "snow"), 80: ("Rain showers", "rain"),
    81: ("Rain showers", "rain"), 82: ("Violent rain showers", "storm"),
    85: ("Snow showers", "snow"), 86: ("Heavy snow showers", "snow"),
    95: ("Thunderstorm", "storm"), 96: ("Thunderstorm with hail", "storm"),
    99: ("Severe thunderstorm with hail", "storm")
}

@st.cache_data(ttl=1800, show_spinner=False)
def weather_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": "WeatherVerse/1.0"})
    with urllib.request.urlopen(request, timeout=12) as response:
        return json.loads(response.read().decode("utf-8"))

@st.cache_data(ttl=3600, show_spinner=False)
def geocode_city(city):
    query = urllib.parse.urlencode({"name": city, "count": 1, "language": "en", "format": "json"})
    payload = weather_json("https://geocoding-api.open-meteo.com/v1/search?" + query)
    results = payload.get("results") or []
    if not results:
        return None
    place = results[0]
    return {
        "name": place.get("name", city),
        "country": place.get("country", ""),
        "admin1": place.get("admin1", ""),
        "latitude": float(place["latitude"]),
        "longitude": float(place["longitude"]),
        "timezone": place.get("timezone", "auto")
    }

@st.cache_data(ttl=1800, show_spinner=False)
def get_live_weather(latitude, longitude, timezone="auto"):
    query = urllib.parse.urlencode({
        "latitude": latitude, "longitude": longitude, "timezone": timezone,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,weather_code,cloud_cover,pressure_msl,wind_speed_10m,wind_direction_10m,uv_index",
        "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,wind_speed_10m,weather_code",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_probability_max,precipitation_sum,wind_speed_10m_max"
    })
    return weather_json("https://api.open-meteo.com/v1/forecast?" + query)

def weather_description(code):
    return WEATHER_CODES.get(int(code), ("Changing conditions", "cloud"))

def weather_theme(kind):
    themes = {
        "sun": {"label": "Sunny", "colors": "#3b1b68, #a34d9a, #f5a742", "accent": "#ffd66b"},
        "cloud": {"label": "Cloudy", "colors": "#111d43, #354a78, #5e6790", "accent": "#c9ddff"},
        "rain": {"label": "Rainy", "colors": "#07182e, #123f69, #345e91", "accent": "#75d9ff"},
        "storm": {"label": "Stormy", "colors": "#080d25, #28204e, #503b73", "accent": "#c6a8ff"},
        "wind": {"label": "Windy", "colors": "#092c43, #166b83, #5551a1", "accent": "#9bf6ff"},
        "snow": {"label": "Snowy", "colors": "#27385c, #6589b4, #9dbbd4", "accent": "#f1f8ff"},
        "fog": {"label": "Foggy", "colors": "#30344e, #626b82, #9ba6b6", "accent": "#e0e8f2"}
    }
    return themes.get(kind, themes["cloud"])

def render_weather_animation(kind, preview=False):
    # The weather overlay is decorative and remains behind the dashboard content.
    theme = weather_theme(kind)
    effect_html = ""
    if kind == "sun":
        effect_html = '<div class="wv-sun"></div><div class="wv-sunray"></div>'
    elif kind in ("rain", "storm"):
        drops = "".join(f'<i style="left:{(i * 7) % 100}%;animation-delay:-{(i % 13) * 0.31}s;animation-duration:{0.65 + (i % 5) * 0.12}s"></i>' for i in range(52))
        effect_html = f'<div class="wv-rain">{drops}</div>'
        if kind == "storm":
            effect_html += '<div class="wv-lightning"></div>'
    elif kind == "wind":
        streaks = "".join(f'<i style="top:{(i * 11) % 100}%;animation-delay:-{(i % 9) * 0.8}s;width:{80 + (i % 5) * 35}px"></i>' for i in range(18))
        effect_html = f'<div class="wv-wind">{streaks}</div><div class="wv-vortex"></div>'
    elif kind == "snow":
        flakes = "".join(f'<i style="left:{(i * 9) % 100}%;animation-delay:-{(i % 10) * 0.6}s;animation-duration:{4 + (i % 5)}s">❄</i>' for i in range(24))
        effect_html = f'<div class="wv-snow">{flakes}</div>'
    else:
        clouds = ''.join(f'<div class="wv-cloud wvc{i}" aria-hidden="true"></div>' for i in range(1, 5))
        effect_html = clouds
    st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(125deg, {theme['colors']}); background-size: 300% 300%; animation: wvSky 18s ease infinite; }}
    @keyframes wvSky {{ 0%{{background-position:0% 50%}} 50%{{background-position:100% 50%}} 100%{{background-position:0% 50%}} }}
    .wv-weather-effects {{ position:fixed; inset:0; overflow:hidden; pointer-events:none; z-index:0; }}
    .wv-sun {{ position:absolute; width:150px;height:150px;border-radius:50%;right:9%;top:9%;background:radial-gradient(circle,#fff7b8 0%,#ffd35e 35%,rgba(255,169,64,.28) 68%,transparent 75%);box-shadow:0 0 75px 24px rgba(255,193,76,.28);animation:wvSunPulse 4s ease-in-out infinite; }}
    .wv-sunray {{ position:absolute;right:1%;top:0;width:400px;height:360px;background:radial-gradient(ellipse at 70% 25%,rgba(255,220,130,.19),transparent 68%);animation:wvRay 8s ease-in-out infinite alternate; }}
    @keyframes wvSunPulse {{50%{{transform:scale(1.07);filter:brightness(1.14)}}}}
    @keyframes wvRay {{to{{transform:translate(-28px,18px) rotate(5deg)}}}}
    .wv-cloud {{position:absolute;width:210px;height:55px;border-radius:50px;background:rgba(213,231,255,.18);filter:blur(2px);box-shadow:0 0 38px rgba(180,215,255,.12);animation:wvCloudMove 35s linear infinite}}
    .wv-cloud:before,.wv-cloud:after {{content:"";position:absolute;border-radius:50%;background:inherit}}
    .wv-cloud:before {{width:82px;height:82px;left:35px;top:-36px}} .wv-cloud:after {{width:105px;height:95px;left:90px;top:-48px}}
    .wvc1{{top:17%;left:-240px}} .wvc2{{top:42%;left:-300px;transform:scale(.7);animation-delay:-12s;animation-duration:48s;opacity:.75}} .wvc3{{top:69%;left:-260px;transform:scale(.85);animation-delay:-24s;animation-duration:42s}} .wvc4{{top:85%;left:-300px;transform:scale(.55);animation-delay:-8s;animation-duration:52s;opacity:.6}}
    @keyframes wvCloudMove {{to{{translate:calc(100vw + 420px) 0}}}}
    .wv-rain{{position:absolute;inset:-20px;opacity:.86;background:linear-gradient(115deg,transparent 0 49%,rgba(151,221,255,.08) 49.2% 49.7%,transparent 50%);background-size:14px 100%;animation:wvRainSweep 1.1s linear infinite}}
    .wv-rain i{{position:absolute;top:-30px;height:32px;width:2px;background:linear-gradient(transparent,rgba(166,226,255,.9));border-radius:2px;animation:wvDrop linear infinite}}
    @keyframes wvDrop {{to{{transform:translate(-38px,115vh)}}}} @keyframes wvRainSweep {{to{{background-position:14px 0}}}}
    .wv-lightning{{position:absolute;inset:0;background:rgba(226,235,255,.22);opacity:0;animation:wvFlash 7s linear infinite}}
    @keyframes wvFlash {{0%,91%,93%,96%,100%{{opacity:0}}92%{{opacity:.65}}94%{{opacity:.18}}}}
    .wv-wind i{{position:absolute;left:-25%;height:2px;border-radius:100%;background:linear-gradient(90deg,transparent,rgba(156,244,255,.65),transparent);animation:wvGust 5s linear infinite}}
    @keyframes wvGust {{to{{transform:translateX(150vw) skewX(-25deg)}}}}
    .wv-vortex{{position:absolute;width:260px;height:260px;right:8%;top:34%;border:2px solid rgba(180,238,255,.13);border-left-color:rgba(180,238,255,.6);border-radius:50%;box-shadow:0 0 35px rgba(130,220,255,.12);animation:wvSpin 8s linear infinite;opacity:.55}}
    @keyframes wvSpin {{to{{transform:rotate(360deg) scale(.92)}}}}
    .wv-snow i{{position:absolute;top:-30px;color:rgba(255,255,255,.9);font-style:normal;font-size:18px;text-shadow:0 0 10px white;animation:wvFlake linear infinite}}
    @keyframes wvFlake {{to{{transform:translate(60px,110vh) rotate(260deg)}}}}
    @media (prefers-reduced-motion:reduce){{.stApp,.wv-weather-effects *{{animation:none!important}}}}
    </style>
    <div class="wv-weather-effects" aria-hidden="true">{effect_html}</div>
    """, unsafe_allow_html=True)

st.markdown("## 🌍 Live Weather Explorer")
st.caption("Search a place, explore a regional weather map, and preview weather-reactive animations. Live data is fetched from Open-Meteo when the service is reachable.")
region_choice = st.radio("Map region", ["🇮🇳 India", "🌍 Whole World"], horizontal=True, key="wv_map_region")
search_col, preview_col = st.columns([1.25, 1])
with search_col:
    with st.form("wv_location_form"):
        city_query = st.text_input("Search for a city or place", value=st.session_state.get("wv_city_query", "Coimbatore"), placeholder="e.g. Chennai, Tokyo, London")
        search_submitted = st.form_submit_button("🔎 Get live weather", use_container_width=True)
with preview_col:
    animation_preview = st.selectbox("Animation preview", ["Automatic (live weather)", "☀️ Sunny", "☁️ Cloudy", "🌧️ Rainy", "⛈️ Stormy", "💨 Windy", "❄️ Snowy", "🌫️ Foggy"], key="wv_animation_preview")

if search_submitted:
    st.session_state["wv_city_query"] = city_query.strip() or "Coimbatore"
    st.session_state.pop("wv_selected_place", None)

if "wv_selected_place" not in st.session_state:
    try:
        st.session_state["wv_selected_place"] = geocode_city(st.session_state.get("wv_city_query", "Coimbatore"))
    except Exception:
        st.session_state["wv_selected_place"] = None

place = st.session_state.get("wv_selected_place")
if place:
    try:
        live = get_live_weather(place["latitude"], place["longitude"], place.get("timezone", "auto"))
        current = live.get("current", {})
        current_code = int(current.get("weather_code", 3))
        condition_text, condition_kind = weather_description(current_code)
        # Treat sustained strong wind as a windy theme unless a storm takes priority.
        if condition_kind not in ("storm", "rain") and float(current.get("wind_speed_10m", 0) or 0) >= 35:
            condition_kind = "wind"
            condition_text = "Windy conditions"
        preview_to_kind = {"☀️ Sunny":"sun", "☁️ Cloudy":"cloud", "🌧️ Rainy":"rain", "⛈️ Stormy":"storm", "💨 Windy":"wind", "❄️ Snowy":"snow", "🌫️ Foggy":"fog"}
        active_kind = condition_kind if animation_preview == "Automatic (live weather)" else preview_to_kind.get(animation_preview, condition_kind)
        render_weather_animation(active_kind, preview=(animation_preview != "Automatic (live weather)"))
        st.markdown(f"### 📍 {place['name']}, {place.get('admin1') + ', ' if place.get('admin1') else ''}{place['country']}")
        st.markdown(f"**{condition_text}** · Local observation time: {current.get('time', 'Not available')}")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🌡️ Temperature", f"{current.get('temperature_2m', '—')} °C", help="Live 2-metre air temperature")
        m2.metric("🤗 Feels like", f"{current.get('apparent_temperature', '—')} °C")
        m3.metric("💧 Humidity", f"{current.get('relative_humidity_2m', '—')}%")
        m4.metric("💨 Wind speed", f"{current.get('wind_speed_10m', '—')} km/h")
        m5, m6, m7, m8 = st.columns(4)
        m5.metric("🌧️ Precipitation", f"{current.get('precipitation', '—')} mm")
        m6.metric("☁️ Cloud cover", f"{current.get('cloud_cover', '—')}%")
        m7.metric("🔆 UV index", str(current.get('uv_index', '—')))
        m8.metric("🧭 Wind direction", f"{current.get('wind_direction_10m', '—')}°")

        daily = live.get("daily", {})
        if daily.get("time"):
            forecast_df = pd.DataFrame({
                "Date": pd.to_datetime(daily["time"]),
                "High (°C)": daily.get("temperature_2m_max", []),
                "Low (°C)": daily.get("temperature_2m_min", []),
                "Rain chance (%)": daily.get("precipitation_probability_max", [None] * len(daily["time"])),
                "Rainfall (mm)": daily.get("precipitation_sum", [None] * len(daily["time"])),
                "Wind max (km/h)": daily.get("wind_speed_10m_max", [None] * len(daily["time"]))
            })
            st.markdown("#### 📅 7-day forecast")
            fc1, fc2 = st.columns(2)
            with fc1:
                fig_forecast = px.line(forecast_df, x="Date", y=["High (°C)", "Low (°C)"], markers=True, title="Daily temperature forecast")
                fig_forecast.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,.025)", font_color="#eef4ff", margin=dict(l=8,r=8,t=55,b=8))
                st.plotly_chart(fig_forecast, use_container_width=True)
            with fc2:
                fig_rain = px.bar(forecast_df, x="Date", y="Rain chance (%)", title="Daily chance of precipitation")
                fig_rain.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,.025)", font_color="#eef4ff", margin=dict(l=8,r=8,t=55,b=8))
                st.plotly_chart(fig_rain, use_container_width=True)
            st.dataframe(forecast_df, use_container_width=True, hide_index=True)

        st.markdown("#### 🗺️ Weather map")
        st.caption("Markers show live conditions for a sample of cities in the selected region. Select a marker for its city name and current temperature.")
        india_cities = [
            ("New Delhi",28.6139,77.2090),("Mumbai",19.0760,72.8777),("Chennai",13.0827,80.2707),
            ("Bengaluru",12.9716,77.5946),("Kolkata",22.5726,88.3639),("Hyderabad",17.3850,78.4867),
            ("Coimbatore",11.0168,76.9558),("Jaipur",26.9124,75.7873),("Ahmedabad",23.0225,72.5714),
            ("Kochi",9.9312,76.2673),("Bhopal",23.2599,77.4126),("Guwahati",26.1445,91.7362)
        ]
        world_cities = [
            ("New Delhi",28.6139,77.2090),("London",51.5072,-0.1276),("Tokyo",35.6762,139.6503),
            ("New York",40.7128,-74.0060),("São Paulo",-23.5505,-46.6333),("Cairo",30.0444,31.2357),
            ("Cape Town",-33.9249,18.4241),("Sydney",-33.8688,151.2093),("Singapore",1.3521,103.8198),
            ("Dubai",25.2048,55.2708),("Paris",48.8566,2.3522),("Toronto",43.6532,-79.3832),
            ("Mexico City",19.4326,-99.1332),("Nairobi",-1.2921,36.8219),("Reykjavik",64.1466,-21.9426)
        ]
        city_list = india_cities if region_choice == "🇮🇳 India" else world_cities
        map_rows = []
        progress = st.empty()
        for idx, (city_name, lat, lon) in enumerate(city_list):
            try:
                city_live = get_live_weather(lat, lon, "auto").get("current", {})
                city_kind = weather_description(city_live.get("weather_code", 3))[1]
                if city_kind not in ("storm", "rain") and float(city_live.get("wind_speed_10m", 0) or 0) >= 35:
                    city_kind = "wind"
                map_rows.append({"City": city_name, "Latitude": lat, "Longitude": lon,
                                 "Temperature (°C)": city_live.get("temperature_2m"),
                                 "Condition": weather_description(city_live.get("weather_code", 3))[0],
                                 "Weather type": city_kind})
            except Exception:
                continue
        progress.empty()
        if map_rows:
            map_df = pd.DataFrame(map_rows)
            color_map = {"sun":"#ffcf54", "cloud":"#b9c7e7", "rain":"#65d5ff", "storm":"#bd9aff", "wind":"#79f2d5", "snow":"#ffffff", "fog":"#c6ccd5"}
            fig_map = px.scatter_geo(map_df, lat="Latitude", lon="Longitude", color="Weather type", hover_name="City",
                                     hover_data={"Temperature (°C)": True, "Condition": True, "Latitude": False, "Longitude": False, "Weather type": False},
                                     color_discrete_map=color_map, projection="natural earth" if region_choice == "🌍 Whole World" else "natural earth",
                                     title="Live weather by city", size_max=14)
            if region_choice == "🇮🇳 India":
                fig_map.update_geos(lataxis_range=[5, 36], lonaxis_range=[67, 98], showcountries=True, showland=True, landcolor="rgba(30,45,78,.8)", countrycolor="rgba(180,210,255,.35)", bgcolor="rgba(0,0,0,0)")
            else:
                fig_map.update_geos(showcountries=True, showland=True, landcolor="rgba(30,45,78,.8)", countrycolor="rgba(180,210,255,.25)", bgcolor="rgba(0,0,0,0)")
            fig_map.update_traces(marker=dict(size=12, opacity=.92, line=dict(width=1, color="white")))
            fig_map.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#eef4ff", legend_title_text="Condition", margin=dict(l=0,r=0,t=55,b=0), height=530)
            st.plotly_chart(fig_map, use_container_width=True)
            st.caption("Map coverage is a set of representative cities, not a continuous radar/satellite precipitation layer.")
            st.dataframe(map_df[["City", "Condition", "Temperature (°C)"]], use_container_width=True, hide_index=True)
        else:
            st.warning("The live city map could not load. Check your internet connection and try again.")
        st.caption("Weather data source: Open-Meteo. Forecasts are model-based and can change. The animation preview changes visuals only; it does not change the live weather readings.")
    except Exception as error:
        st.warning("Live weather could not be loaded right now. Check your internet connection, then submit the city search again.")
        st.caption("Technical detail: " + str(error)[:220])
else:
    st.warning("We couldn't find that place. Try a city name such as Coimbatore, Chennai, London, or Tokyo.")
    if animation_preview != "Automatic (live weather)":
        preview_to_kind = {"☀️ Sunny":"sun", "☁️ Cloudy":"cloud", "🌧️ Rainy":"rain", "⛈️ Stormy":"storm", "💨 Windy":"wind", "❄️ Snowy":"snow", "🌫️ Foggy":"fog"}
        render_weather_animation(preview_to_kind.get(animation_preview, "cloud"), preview=True)

st.divider()

# ---------------- SAMPLE DATA ----------------
@st.cache_data
def create_sample_data():
    rng = np.random.default_rng(42)

    dates = pd.date_range(
        end=pd.Timestamp.today().normalize(),
        periods=90,
        freq="D"
    )

    temperature = 28 + 4 * np.sin(
        np.arange(90) * 2 * np.pi / 30
    )
    temperature += rng.normal(0, 1.8, 90)

    humidity = np.clip(
        68 - (temperature - 28) * 2 + rng.normal(0, 7, 90),
        25, 100
    )

    rainfall = np.maximum(0, rng.gamma(1.4, 3, 90) - 2)

    return pd.DataFrame({
        "Date": dates,
        "Temperature": np.round(temperature, 1),
        "Humidity": np.round(humidity, 1),
        "Rainfall": np.round(rainfall, 1),
        "Wind Speed": np.round(rng.uniform(2, 22, 90), 1)
    })

# ---------------- LOAD DATA ----------------
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        if df.empty:
            st.error("The uploaded CSV has no data.")
            st.stop()

        st.success("Your CSV file was uploaded successfully.")
        data_source = "Uploaded dataset"

    except Exception as error:
        st.error(f"Could not read this CSV file: {error}")
        st.stop()
else:
    df = create_sample_data()
    data_source = "Interactive demo data"

df.columns = df.columns.astype(str).str.strip()
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

# ---------------- STATUS ----------------
st.markdown(
    f"<p class='section-label'>◉ {data_source.upper()}</p>",
    unsafe_allow_html=True
)

if uploaded_file is None:
    st.info(
        "You are viewing sample data to explore the dashboard. "
        "Upload your own weather CSV in the sidebar to analyze your data."
    )

# ---------------- SUMMARY CARDS ----------------
st.markdown("### ✨ Weather at a glance")

col1, col2, col3, col4 = st.columns(4)

col1.metric("📁 Total Records", f"{len(df):,}")
col2.metric("🧩 Total Columns", f"{len(df.columns):,}")
col3.metric("⚠️ Missing Cells", f"{int(df.isnull().sum().sum()):,}")
col4.metric("🔢 Numeric Variables", f"{len(numeric_cols):,}")

# Extra review-friendly weather insights are calculated from the displayed dataset.
def find_weather_column(words):
    for column_name in df.columns:
        name = str(column_name).lower().replace("_", " ").replace("-", " ")
        if any(word in name for word in words):
            return column_name
    return None

_temp_name = find_weather_column(["temperature", "temp"])
_humidity_name = find_weather_column(["humidity", "relative humidity"])
_rain_name = find_weather_column(["rainfall", "precipitation", "rain"])
_wind_name = find_weather_column(["wind speed", "windspeed", "wind"])

available_insights = []
for label, column_name, unit in [
    ("Average temperature", _temp_name, "°"),
    ("Average humidity", _humidity_name, "%"),
    ("Total rainfall", _rain_name, ""),
    ("Average wind speed", _wind_name, "")
]:
    if column_name is not None:
        numbers = pd.to_numeric(df[column_name], errors="coerce").dropna()
        if not numbers.empty:
            if label == "Total rainfall":
                value = f"{numbers.sum():.1f}{unit}"
            else:
                value = f"{numbers.mean():.1f}{unit}"
            available_insights.append((label, value, column_name))

if available_insights:
    st.markdown("#### 🌤️ Weather insights from your data")
    insight_cols = st.columns(len(available_insights))
    for insight_col, (label, value, original_column) in zip(insight_cols, available_insights):
        insight_col.metric(label, value, help=f"Calculated from the '{original_column}' column in the current dataset.")
    st.caption("These summaries describe the dataset you loaded; they are not live weather readings.")

st.divider()

# ---------------- DATASET PREVIEW ----------------
with st.expander("📋 Explore your dataset"):
    st.markdown("#### Dataset preview")
    st.dataframe(df.head(100), use_container_width=True)

    left, right = st.columns(2)

    with left:
        st.markdown("**Column data types**")
        types_df = pd.DataFrame({
            "Column": df.columns,
            "Data Type": [str(dtype) for dtype in df.dtypes]
        })
        st.dataframe(types_df, use_container_width=True, hide_index=True)

    with right:
        st.markdown("**Missing values per column**")
        missing_df = df.isnull().sum().rename(
            "Missing Values"
        ).to_frame()
        st.dataframe(missing_df, use_container_width=True)

# ---------------- WEATHER ANALYTICS ----------------
st.markdown("### 📈 Discover weather patterns")

if not numeric_cols:
    st.warning(
        "No numeric columns were found. Upload a CSV containing numeric "
        "weather measurements such as temperature or humidity."
    )
else:
    tab1, tab2, tab3, tab4 = st.tabs([
        "🌡️ Trends",
        "📊 Distribution",
        "🔗 Correlations",
        "🧮 Statistics"
    ])

    # TRENDS — separate variables get separate charts, never overlaid together.
    with tab1:
        st.markdown("#### Compare weather variables in separate charts")
        if len(numeric_cols) == 1:
            trend_left, trend_right = st.columns(2)
            selected_variables = [numeric_cols[0]]
        else:
            first_col, second_col = st.columns(2)
            with first_col:
                trend_one = st.selectbox(
                    "First variable",
                    numeric_cols,
                    key="trend_variable_one"
                )
            second_options = [name for name in numeric_cols if name != trend_one]
            with second_col:
                trend_two = st.selectbox(
                    "Second variable",
                    second_options,
                    key="trend_variable_two"
                )
            selected_variables = [trend_one, trend_two]
            trend_left, trend_right = st.columns(2)

        date_cols = [
            c for c in df.columns
            if str(c).lower() in ["date", "datetime", "timestamp", "time"]
        ]

        def build_trend_figure(variable_name):
            values = pd.to_numeric(df[variable_name], errors="coerce")
            chart_frame = pd.DataFrame({variable_name: values}, index=df.index).dropna()
            if date_cols:
                chart_frame["Observation Date"] = pd.to_datetime(
                    df.loc[chart_frame.index, date_cols[0]], errors="coerce"
                )
                chart_frame = chart_frame.dropna(subset=["Observation Date"])
                x_name = "Observation Date"
            else:
                chart_frame["Observation"] = np.arange(1, len(chart_frame) + 1)
                x_name = "Observation"
            if chart_frame.empty:
                return None
            chart = px.line(
                chart_frame,
                x=x_name,
                y=variable_name,
                title=f"{variable_name} trend",
                markers=True
            )
            chart.update_traces(
                line=dict(color="#56D7FF", width=3),
                marker=dict(size=5, color="#C4B5FD")
            )
            chart.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(255,255,255,0.025)",
                font=dict(color="#EAF1FF"),
                margin=dict(l=8, r=8, t=55, b=8),
                hovermode="x unified",
                showlegend=False
            )
            return chart

        for chart_column, variable_name in zip([trend_left, trend_right], selected_variables):
            with chart_column:
                st.markdown(f"**{variable_name}**")
                trend_figure = build_trend_figure(variable_name)
                if trend_figure is not None:
                    st.plotly_chart(trend_figure, use_container_width=True, key=f"trend_chart_{variable_name}")
                else:
                    st.info(f"No valid values are available for {variable_name}.")
        st.caption("Each variable is plotted separately so its scale and pattern are easier to read.")

    # DISTRIBUTION
    with tab2:
        st.markdown("#### Understand the distribution")

        dist_col = st.selectbox(
            "Select a variable to examine",
            numeric_cols,
            key="distribution_variable"
        )

        dist_values = pd.to_numeric(
            df[dist_col],
            errors="coerce"
        ).dropna()

        if not dist_values.empty:
            fig = px.histogram(
                x=dist_values,
                nbins=25,
                title=f"Distribution of {dist_col}",
                labels={"x": dist_col, "count": "Frequency"}
            )

            fig.update_traces(
                marker_color="#8B7CFF",
                marker_line_color="#B9AEFF",
                marker_line_width=1,
                opacity=0.9
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(255,255,255,0.025)",
                font=dict(color="#EAF1FF"),
                margin=dict(l=10, r=10, t=55, b=10)
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No valid numeric values are available.")

    # CORRELATION HEATMAP
    with tab3:
        st.markdown("#### Relationship between weather variables")

        if len(numeric_cols) >= 2:
            corr_data = df[numeric_cols].corr()

            fig = px.imshow(
                corr_data,
                text_auto=".2f",
                color_continuous_scale=[
                    "#233876",
                    "#56B4E9",
                    "#F4F6FF",
                    "#C084FC",
                    "#8B5CF6"
                ],
                zmin=-1,
                zmax=1,
                aspect="auto",
                title="Weather variable correlation heatmap"
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#EAF1FF"),
                margin=dict(l=10, r=10, t=55, b=10)
            )

            st.plotly_chart(fig, use_container_width=True)

            st.caption(
                "Correlation ranges from -1 to +1. Correlation indicates "
                "association, not proof of causation."
            )
        else:
            st.info(
                "At least two numeric columns are needed for correlation."
            )

    # STATISTICS
    with tab4:
        st.markdown("#### Statistical summary")

        summary = df[numeric_cols].describe().T.round(2)
        st.dataframe(summary, use_container_width=True)

        st.download_button(
            "⬇️ Download statistical summary",
            data=summary.to_csv().encode("utf-8"),
            file_name="weather_statistics.csv",
            mime="text/csv"
        )

# ---------------- TEMPERATURE FORECAST ----------------
st.divider()
st.markdown("### 🔮 Temperature Forecast")

temperature_columns = [
    col for col in numeric_cols if "temp" in col.lower()
]

if temperature_columns:
    temp_col = st.selectbox(
        "Choose temperature variable",
        temperature_columns,
        key="forecast_temperature"
    )

    values = pd.to_numeric(df[temp_col], errors="coerce").dropna()

    if len(values) >= 3:
        forecast_days = st.slider(
            "Future observations to estimate",
            min_value=3,
            max_value=30,
            value=7
        )

        x = np.arange(len(values))
        y = values.to_numpy()

        slope, intercept = np.polyfit(x, y, 1)

        future_x = np.arange(
            len(values), len(values) + forecast_days
        )
        predicted = slope * future_x + intercept

        historical = pd.DataFrame({
            "Observation": x + 1,
            "Temperature": y,
            "Type": "Historical"
        })

        future = pd.DataFrame({
            "Observation": future_x + 1,
            "Temperature": predicted,
            "Type": "Estimated trend"
        })

        chart_data = pd.concat(
            [historical, future], ignore_index=True
        )

        fig = px.line(
            chart_data,
            x="Observation",
            y="Temperature",
            color="Type",
            markers=True,
            title="Historical Temperature and Estimated Trend",
            color_discrete_map={
                "Historical": "#56D7FF",
                "Estimated trend": "#F6B84A"
            }
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.025)",
            font=dict(color="#EAF1FF"),
            margin=dict(l=10, r=10, t=55, b=10)
        )

        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "These are linear trend estimates, not live weather forecasts."
        )

        forecast_table = future[
            ["Observation", "Temperature"]
        ].round(2)

        st.dataframe(
            forecast_table,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇️ Download temperature estimates",
            data=forecast_table.to_csv(index=False).encode("utf-8"),
            file_name="temperature_estimates.csv",
            mime="text/csv"
        )
    else:
        st.info("At least three temperature observations are required.")
else:
    st.info(
        "No temperature column found. Please use a numeric column "
        "whose name contains 'temp'."
    )

# ---------------- DOWNLOAD DATA ----------------
st.divider()
st.markdown("### 📥 Export your data")

left, right = st.columns([2, 1])

with left:
    st.write(
        "Download a copy of your dataset with duplicate rows removed. "
        "The original uploaded file is not modified."
    )

with right:
    cleaned_df = df.drop_duplicates()

    st.download_button(
        "⬇️ Download cleaned CSV",
        data=cleaned_df.to_csv(index=False).encode("utf-8"),
        file_name="cleaned_weather_data.csv",
        mime="text/csv",
        use_container_width=True
    )

# ---------------- FOOTER ----------------
st.markdown("""
<div style="text-align:center;padding:28px 0 8px;color:#A9BBDD;">
    <div style="font-size:32px;">🌦️</div>
    <div style="font-weight:700;color:#E5EDFF;font-size:20px;">
        WeatherVerse
    </div>
    <div style="font-size:12px;margin-top:8px;">
        Weather Data Analysis & Forecast Visualization
    </div>
    <div style="font-size:11px;margin-top:8px;">
        An academic analytics dashboard · Powered by Python
    </div>
</div>
""", unsafe_allow_html=True)
