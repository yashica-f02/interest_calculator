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
    # Standardizing for display
    record = {
        'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'type': calc_type,
        'principal': f"₹{principal:,.2f}",
        'rate': f"{rate}%",
        'duration': duration,
        'interest': f"₹{interest:,.2f}",
        'total': f"₹{total:,.2f}",
        'frequency': frequency if frequency else "-"
    }
    st.session_state.records.insert(0, record)
    if len(st.session_state.records) > 50:
        st.session_state.records = st.session_state.records[:50]

def get_exact_ymd(start_date, end_date):
    delta = relativedelta(end_date, start_date)
    return delta.years, delta.months, delta.days

def display_result_table(duration, interest, total, frequency=None):
    data = {
        "Duration": [duration],
        "Frequency": [frequency if frequency else "-"],
        "Interest": [f"₹{interest:,.2f}"],
        "Total Amount": [f"₹{total:,.2f}"]
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
        # value=None makes the box empty on start
        P = st.number_input("Principal Amount (₹)", value=None, placeholder="Enter Amount", key="si_p")
    with col2:
        R = st.number_input("Rate (%)", value=None, placeholder="Enter Rate", key="si_r")

    # Default to "By Dates"
    duration_mode = st.radio("Duration Mode", ["By Dates", "Manual (Y/M/D)"], key="si_mode")

    total_days = 0
    duration_str = ""
    
    if duration_mode == "By Dates":
        c1, c2 = st.columns(2)
        with c1:
            start_date = st.date_input("Start Date", key="si_start")
        with c2:
            end_date = st.date_input("End Date", key="si_end")
        
        if end_date >= start_date:
            years, months, days = get_exact_ymd(start_date, end_date)
            duration_str = f"{years}Y {months}M {days}D"
            total_days = (end_date - start_date).days
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            y = st.number_input("Years", min_value=0, step=1, value=0)
        with c2:
            m = st.number_input("Months", min_value=0, step=1, value=0)
        with c3:
            d = st.number_input("Days", min_value=0, step=1, value=0)
        total_days = (y * 365) + (m * 30) + d
        duration_str = f"{y}Y {m}M {d}D"

    # Default to "Per Month"
    per = st.radio("Rate Type", ["Per Month", "Per Year"], key="si_per")

    if st.button("🚀 Calculate Simple Interest"):
        if not P or not R or total_days <= 0:
            st.warning("Please fill in all fields with values greater than zero.")
        else:
            annual_rate = R * 12 if per == "Per Month" else R
            # Exact 365 day calculation for precision
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
        P_ci = st.number_input("Principal Amount (₹)", value=None, placeholder="Enter Amount", key="ci_p")
    with col2:
        R_ci = st.number_input("Rate (%)", value=None, placeholder="Enter Rate", key="ci_r")

    duration_mode_ci = st.radio("Duration Mode", ["By Dates", "Manual (Y/M/D)"], key="ci_mode_sel")

    total_days_ci = 0
    duration_str_ci = ""
    
    if duration_mode_ci == "By Dates":
        c1, c2 = st.columns(2)
        with c1:
            start_date_ci = st.date_input("Start Date", key="ci_start")
        with c2:
            end_date_ci = st.date_input("End Date", key="ci_end")
        if end_date_ci >= start_date_ci:
            y, m, d = get_exact_ymd(start_date_ci, end_date_ci)
            duration_str_ci = f"{y}Y {m}M {d}D"
            total_days_ci = (end_date_ci - start_date_ci).days
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            y_ci = st.number_input("Years", min_value=0, step=1, value=0, key="ci_y_manual")
        with c2:
            m_ci = st.number_input("Months", min_value=0, step=1, value=0, key="ci_m_manual")
        with c3:
            d_ci = st.number_input("Days", min_value=0, step=1, value=0, key="ci_d_manual")
        total_days_ci = (y_ci * 365) + (m_ci * 30) + d_ci
        duration_str_ci = f"{y_ci}Y {m_ci}M {d_ci}D"

    per_ci = st.radio("Rate Type", ["Per Month", "Per Year"], key="ci_per_sel")
    freq = st.selectbox("Compounding Frequency", ["Yearly","Half-Yearly","Quarterly","Monthly","Daily"])
    freq_map = {"Yearly":1, "Half-Yearly":2, "Quarterly":4, "Monthly":12, "Daily":365}
    n_val = freq_map[freq]

    if st.button("🚀 Calculate Compound Interest"):
        if not P_ci or not R_ci or total_days_ci <= 0:
            st.warning("Please fill in all fields with values greater than zero.")
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
        st.info("No history yet.")
    else:
        for rec in st.session_state.records[:10]:
            st.table(pd.DataFrame([rec]))
     




