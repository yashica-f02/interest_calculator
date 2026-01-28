import streamlit as st
from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta

# -----------------------------
# Initialize session state
# -----------------------------
if 'records' not in st.session_state:
    st.session_state.records = []

# -----------------------------
# Helper Functions
# -----------------------------
def save_record(calc_type, principal, rate, duration, interest, total, frequency=None):
    record = {
        'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'type': calc_type,
        'principal': f"₹{principal:.2f}",
        'rate': f"{rate}%",
        'duration': duration,
        'interest': f"₹{interest:.2f}",
        'total': f"₹{total:.2f}",
        'frequency': frequency if frequency else "-"
    }
    st.session_state.records.insert(0, record)
    if len(st.session_state.records) > 50:
        st.session_state.records = st.session_state.records[:50]

def get_exact_ymd(start_date, end_date):
    """Calculate exact years, months, days using relativedelta"""
    delta = relativedelta(end_date, start_date)
    return delta.years, delta.months, delta.days

def display_result_table(duration, interest, total, frequency=None):
    data = {
        "Duration": [duration],
        "Frequency": [frequency if frequency else "-"],
        "Interest": [f"₹{interest:.2f}"],
        "Total Amount": [f"₹{total:.2f}"]
    }
    df = pd.DataFrame(data)
    st.table(df)

# -----------------------------
# App UI
# -----------------------------
st.set_page_config(page_title="Interest Calculator", page_icon="🪙")
st.title("🪙 Interest Calculator")
st.caption("Clean✨. Fast⏩. Accurate💹")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Simple Interest", "Compound Interest", "Records"])

# -----------------------------
# Simple Interest
# -----------------------------
with tab1:
    st.header("Simple Interest")

    col1, col2 = st.columns(2)
    with col1:
        # Changed to number_input to trigger mobile dial pad
        P = st.number_input("Principal Amount (₹)", min_value=0.0, step=100.0, value=0.0, key="si_p_num")
    with col2:
        R = st.number_input("Rate of Interest (%)", min_value=0.0, step=0.1, value=0.0, key="si_r_num")

    # Flipped: "By Dates" is now default
    duration_mode = st.radio("Duration Mode", ["By Dates", "Manual (Y/M/D)"], key="si_mode")

    total_days = 0
    duration_str = ""
    
    if duration_mode == "By Dates":
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", key="si_start")
        with col2:
            end_date = st.date_input("End Date", key="si_end")
        
        if end_date >= start_date:
            years, months, days = get_exact_ymd(start_date, end_date)
            duration_str = f"{years}Y {months}M {days}D"
            delta = end_date - start_date
            total_days = delta.days
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            years = st.number_input("Years", min_value=0, step=1, key="si_y")
        with col2:
            months = st.number_input("Months", min_value=0, step=1, key="si_m")
        with col3:
            days = st.number_input("Days", min_value=0, step=1, key="si_d")
        total_days = (years * 365) + (months * 30) + days
        duration_str = f"{years}Y {months}M {days}D"

    # Flipped: "Per Month" is now default
    per = st.radio("Rate Type", ["Per Month", "Per Year"], key="si_per_type")

    if st.button("🚀 Calculate Simple Interest"):
        if P <= 0 or R <= 0 or total_days <= 0:
            st.error("Please enter valid positive values.")
        else:
            # Calculation adjustment for accuracy
            annual_rate = R * 12 if per == "Per Month" else R
            # Using 365 for standard financial daily interest
            interest = (P * annual_rate * (total_days / 365)) / 100
            total = P + interest
            
            save_record("Simple", P, annual_rate, duration_str, interest, total)
            display_result_table(duration_str, interest, total)

# -----------------------------
# Compound Interest
# -----------------------------
with tab2:
    st.header("Compound Interest")

    col1, col2 = st.columns(2)
    with col1:
        P_ci = st.number_input("Principal Amount (₹)", min_value=0.0, step=100.0, value=0.0, key="ci_p_num")
    with col2:
        R_ci = st.number_input("Rate of Interest (%)", min_value=0.0, step=0.1, value=0.0, key="ci_r_num")

    duration_mode_ci = st.radio("Duration Mode", ["By Dates", "Manual (Y/M/D)"], key="ci_mode")

    total_days_ci = 0
    duration_str_ci = ""
    
    if duration_mode_ci == "By Dates":
        col1, col2 = st.columns(2)
        with col1:
            start_date_ci = st.date_input("Start Date", key="ci_start")
        with col2:
            end_date_ci = st.date_input("End Date", key="ci_end")
        if end_date_ci >= start_date_ci:
            y, m, d = get_exact_ymd(start_date_ci, end_date_ci)
            duration_str_ci = f"{y}Y {m}M {d}D"
            total_days_ci = (end_date_ci - start_date_ci).days
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            y_ci = st.number_input("Years", min_value=0, step=1, key="ci_y")
        with col2:
            m_ci = st.number_input("Months", min_value=0, step=1, key="ci_m")
        with col3:
            d_ci = st.number_input("Days", min_value=0, step=1, key="ci_d")
        total_days_ci = (y_ci * 365) + (m_ci * 30) + d_ci
        duration_str_ci = f"{y_ci}Y {m_ci}M {d_ci}D"

    per_ci = st.radio("Rate Type", ["Per Month", "Per Year"], key="ci_per_type")
    freq = st.selectbox("Compounding Frequency", ["Yearly","Half-Yearly","Quarterly","Monthly","Daily"], key="ci_freq")
    freq_map = {"Yearly":1, "Half-Yearly":2, "Quarterly":4, "Monthly":12, "Daily":365}
    n_val = freq_map[freq]

    if st.button("🚀 Calculate Compound Interest"):
        if P_ci <= 0 or R_ci <= 0 or total_days_ci <= 0:
            st.error("Please enter valid positive values.")
        else:
            annual_rate_ci = R_ci * 12 if per_ci == "Per Month" else R_ci
            t_years = total_days_ci / 365
            amount = P_ci * (1 + (annual_rate_ci / (100 * n_val)))**(n_val * t_years)
            interest_ci = amount - P_ci
            
            save_record("Compound", P_ci, annual_rate_ci, duration_str_ci, interest_ci, amount, frequency=freq)
            display_result_table(duration_str_ci, interest_ci, amount, frequency=freq)

# -----------------------------
# Records Tab
# -----------------------------
with tab3:
    st.header("Calculation History")
    if st.button("🗑️ Clear All Records"):
        st.session_state.records = []
        st.rerun()
    
    if not st.session_state.records:
        st.info("No calculations yet.")
    else:
        for rec in st.session_state.records[:10]:
            df_rec = pd.DataFrame([rec])
            st.table(df_rec)
  
        
         




