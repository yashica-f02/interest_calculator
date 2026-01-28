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
        # Manual Mode now starts with empty boxes and dial pads
        c1, c2, c3 = st.columns(3)
        with c1:
            y = st.number_input("Years", value=None, placeholder="0", key="si_y_man")
        with c2:
            m = st.number_input("Months", value=None, placeholder="0", key="si_m_man")
        with c3:
            d = st.number_input("Days", value=None, placeholder="0", key="si_d_man")
        
        # Convert None to 0 for math logic
        y_val = y if y else 0
        m_val = m if m else 0
        d_val = d if d else 0
        total_days = (y_val * 365) + (m_val * 30) + d_val
        duration_str = f"{y_val}Y {m_val}M {d_val}D"

    per = st.radio("Rate Type", ["Per Month", "Per Year"], key="si_per")

    if st.button("🚀 Calculate Simple Interest"):
        if not P or not R or total_days <= 0:
            st.warning("Please fill in Principal, Rate, and Duration.")
        else:
            annual_rate = R * 12 if per == "Per Month" else R
            # 365 day standard for financial precision
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
            y_c, m_c, d_c = get_exact_ymd(start_date_ci, end_date_ci)
            duration_str_ci = f"{y_c}Y {m_c}M {d_c}D"
            total_days_ci = (end_date_ci - start_date_ci).days
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            y_ci = st.number_input("Years", value=None, placeholder="0", key="ci_y_man")
        with c2:
            m_ci = st.number_input("Months", value=None, placeholder="0", key="ci_m_man")
        with c3:
            d_ci = st.number_input("Days", value=None, placeholder="0", key="ci_d_man")
        
        y_v = y_ci if y_ci else 0
        m_v = m_ci if m_ci else 0
        d_v = d_ci if d_ci else 0
        total_days_ci = (y_v * 365) + (m_v * 30) + d_v
        duration_str_ci = f"{y_v}Y {m_v}M {d_v}D"

    per_ci = st.radio("Rate Type", ["Per Month", "Per Year"], key="ci_per_sel")
    freq = st.selectbox("Compounding Frequency", ["Yearly","Half-Yearly","Quarterly","Monthly","Daily"])
    freq_map = {"Yearly":1, "Half-Yearly":2, "Quarterly":4, "Monthly":12, "Daily":365}
    n_val = freq_map[freq]

    if st.button("🚀 Calculate Compound Interest"):
        if not P_ci or not R_ci or total_days_ci <= 0:
            st.warning("Please fill in Principal, Rate, and Duration.")
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
