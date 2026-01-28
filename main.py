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
    years = delta.years
    months = delta.months
    days = delta.days
    return years, months, days

def display_result_table(duration, interest, total, frequency=None):
    data = {
        "Duration": [duration],
        "Frequency": [frequency if frequency else "-"],
        "Interest": [f"₹{interest:.2f}"],
        "Total Amount": [f"₹{total:.2f}"]
    }
    df = pd.DataFrame(data)
    st.table(df)

def parse_number(input_str):
    try:
        return float(input_str.strip().replace(',', '')) if input_str.strip() != "" else 0.0
    except ValueError:
        return None

# -----------------------------
# App UI
# -----------------------------
st.title("🪙Interest Calculator")
st.caption("Clean✨. Fast⏩. Accurate💹")
st.caption("FINANCIAL CALCULATIONS")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Simple Interest", "Compound Interest", "Records"])

# -----------------------------
# Simple Interest
# -----------------------------
with tab1:
    st.header("Simple Interest")

    col1, col2 = st.columns(2)
    with col1:
        P_text = st.text_input("Principal Amount (₹)", placeholder="₹10000", help="Enter amount (dial pad keyboard)")
    with col2:
        R_text = st.text_input("Rate of Interest (%)", placeholder="7.5", help="Enter rate (dial pad keyboard)")

    P = parse_number(P_text)
    R = parse_number(R_text)

    # By Dates FIRST (default)
    duration_mode = st.radio("Duration Mode", ["By Dates", "Manual (Y/M/D)"], index=0)

    total_days = 0
    duration_str = ""
    
    if duration_mode == "Manual (Y/M/D)":
        col1, col2, col3 = st.columns(3)
        with col1:
            years = st.number_input("Years", min_value=0, format="%d", step=1, key="si_y")
        with col2:
            months = st.number_input("Months", min_value=0, format="%d", step=1, key="si_m")
        with col3:
            days = st.number_input("Days", min_value=0, format="%d", step=1, key="si_d")
        total_days = years * 365.25 + months * 30.4375 + days  # More accurate
        duration_str = f"{years}Y {months}M {days}D"
    else:
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

    # Per Month FIRST (default)
    per = st.radio("Rate Type", ["Per Month", "Per Year"], index=0)

    if st.button("🚀 Calculate Simple Interest"):
        if P is None or R is None or total_days <= 0 or P <= 0 or R < 0:
            st.error("Invalid input. Check all values.")
        elif duration_mode == "By Dates" and end_date < start_date:
            st.error("End date must be after start date.")
        else:
            rate = R if per == "Per Month" else R
            # FIXED: More accurate interest calculation matching bank standards
            T_decimal = total_days / 365.25
            interest = (P * rate * T_decimal) / 100
            total = P + interest
            save_record("Simple", P, rate, duration_str, interest, total)
            st.success(f"✅ Interest: ₹{interest:.2f} | Total: ₹{total:.2f}")
            display_result_table(duration_str, interest, total)

# -----------------------------
# Compound Interest
# -----------------------------
with tab2:
    st.header("Compound Interest")

    col1, col2 = st.columns(2)
    with col1:
        P_text = st.text_input("Principal Amount (₹)", placeholder="₹10000", key="ci_p", help="Enter amount (dial pad keyboard)")
    with col2:
        R_text = st.text_input("Rate of Interest (%)", placeholder="7.5", key="ci_r", help="Enter rate (dial pad keyboard)")

    P = parse_number(P_text)
    R = parse_number(R_text)

    # By Dates FIRST (default)
    duration_mode_ci = st.radio("Duration Mode", ["By Dates", "Manual (Y/M/D)"], index=0, key="ci_mode")

    total_days = 0
    duration_str = ""
    
    if duration_mode_ci == "Manual (Y/M/D)":
        col1, col2, col3 = st.columns(3)
        with col1:
            years = st.number_input("Years", min_value=0, format="%d", step=1, key="ci_y")
        with col2:
            months = st.number_input("Months", min_value=0, format="%d", step=1, key="ci_m")
        with col3:
            days = st.number_input("Days", min_value=0, format="%d", step=1, key="ci_d")
        total_days = years * 365.25 + months * 30.4375 + days
        duration_str = f"{years}Y {months}M {days}D"
    else:
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", key="ci_start")
        with col2:
            end_date = st.date_input("End Date", key="ci_end")
        if end_date >= start_date:
            years, months, days = get_exact_ymd(start_date, end_date)
            duration_str = f"{years}Y {months}M {days}D"
            delta = end_date - start_date
            total_days = delta.days

    # Per Month FIRST (default)
    per = st.radio("Rate Type", ["Per Month", "Per Year"], index=0, key="ci_per")
    freq = st.selectbox("Compounding Frequency", ["Yearly","Half-Yearly","Quarterly","Monthly","Daily"], index=3, key="ci_freq")  # Monthly default
    freq_map = {"Yearly":1, "Half-Yearly":2, "Quarterly":4, "Monthly":12, "Daily":365}
    n_val = freq_map[freq]

    if st.button("🚀 Calculate Compound Interest"):
        if P is None or R is None or total_days <= 0 or P <= 0 or R < 0:
            st.error("Invalid input. Check all values.")
        elif duration_mode_ci == "By Dates" and end_date < start_date:
            st.error("End date must be after start date.")
        else:
            rate = R if per == "Per Month" else R
            T_decimal = total_days / 365.25
            amount = P * (1 + rate/(100*n_val))**(n_val*T_decimal)
            interest = amount - P
            save_record("Compound", P, rate, duration_str, interest, amount, frequency=freq)
            st.success(f"✅ Interest: ₹{interest:.2f} | Total: ₹{amount:.2f}")
            display_result_table(duration_str, interest, amount, frequency=freq)

# -----------------------------
# Records Tab
# -----------------------------
with tab3:
    st.header("Calculation History")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear All Records"):
            st.session_state.records = []
            st.rerun()
    
    if not st.session_state.records:
        st.info("No calculations yet. Start calculating to see history!")
    else:
        recent_records = st.session_state.records[:10]
        for rec in recent_records:
            data = {
                "Timestamp": [rec['timestamp']],
                "Type": [rec['type']],
                "Principal": [rec['principal']],
                "Rate": [rec['rate']],
                "Duration": [rec['duration']],
                "Frequency": [rec['frequency']],
                "Interest": [rec['interest']],
                "Total Amount": [rec['total']]
            }
            df = pd.DataFrame(data)
            st.table(df)

 
  




