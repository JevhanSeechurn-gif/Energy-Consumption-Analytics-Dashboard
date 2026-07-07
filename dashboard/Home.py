import streamlit as st

st.header("UK Electricity Demand Dashboard", divider='rainbow')
st.set_page_config(
    page_title="UK Electricity Demand Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* Fade entire app */
    @keyframes fadeInPage {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    /* Apply to main app container */
    .main {
        animation: fadeInPage 1.2s ease-in;
    }

    /* Optional: smoother cards */
    div[data-testid="stMetric"] {
        animation: fadeInPage 1.2s ease-in;
    }
        .main {
            background-color: #eef6f5;
            
    }
    div[data-testid="stMetric"] {
        background-color: white;
        border-radius: 5px;
        padding: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    div[data-testid="stMetric"] div {
        color: black !important;
    }        
    </style>
""", unsafe_allow_html=True)


st.caption("Historical analysis, FES scenarios, and predictive modelling")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Latest Historical Demand", "286,780 GWh", "+1.2%")
with col2:
    st.metric("Highest FES 2050", "784,736 GWh", "+173%")
with col3:
    st.metric("Lowest FES 2050", "558,750 GWh", "+95%")
with col4:
    st.metric("Data Coverage", "2015 – 2050", "Historic + Forecast")

st.divider()


left, right = st.columns([1, 2])

with left:
    st.subheader("Project Overview")
    st.write("This dashboard explores UK electricity demand using historical data, National Grid FES scenarios, and predictive modelling.")

with right:
    st.subheader("Key Focus")
    st.write("Compare historical trends, scenario-based futures, and model-based forecasts.")

def add_footer():
    footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        z-index: 9999;
    }
    </style>
    <div class="footer">
        <p>Developed by  Jevhan Seechurn 2026</a></p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)


add_footer()