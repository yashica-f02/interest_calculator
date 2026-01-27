import streamlit as st
from datetime import datetime
import pandas as pd

# ----------------------------
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
        'rate': f"{rate:.2f}%",
        'duration': duration,
        'interest': f"₹{interest:.2f}",
        'total': f"₹{total:.2f}",
        'frequency': frequency if frequency else "-"
    }
    st.session_state.records.insert(0, record)
    if len(st.session_state.records) > 50:
        st.session_state.records = st.session_state.records[:50]

def days_to_ymd(total_days):
    years = total_days // 365
    remaining_days = total_days % 365
    months = remaining_days // 30
    days = remaining_days % 30
    return int(days), int(months), int(years)

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
st.title("Interest Calculator")
st.caption("Clean✨. Fast⏩. Accurate💹 ")
st.caption("Financial Calculations")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Simple Interest", "Compound Interest", "Records"])

# -----------------------------
# Simple Interest
# -----------------------------
with tab1:
    st.header("Simple Interest")

    col1, col2 = st.columns(2)
    with col1:
        P = st.number_input("Principal Amount (₹)", min_value=0, step=100.0, format="%.2f")
    with col2:
        R = st.number_input("Rate of Interest (%)", min_value=0, step=0.1, format="%.2f")

    duration_mode = st.radio("Duration Mode", ["Manual (Y/M/D)", "By Dates"], key="si_mode")
    if duration_mode == "Manual (Y/M/D)":
        col1, col2, col3 = st.columns(3)
        with col1:
            y_val = st.number_input("Years", min_value=0, step=1, key="si_y")
        with col2:
            m_val = st.number_input("Months", min_value=0, max_value=11, step=1, key="si_m")
        with col3:
            d_val = st.number_input("Days", min_value=0, max_value=30, step=1, key="si_d")
        total_days = y_val*365 + m_val*30 + d_val
    else:
        start_date = st.date_input("Start Date", key="si_start")
        end_date = st.date_input("End Date", key="si_end")
        delta = end_date - start_date
        total_days = delta.days if delta.days > 0 else 0

    per = st.radio("Rate Type", ["Per Year", "Per Month"], key="si_per")

    if st.button("🚀 Calculate Simple Interest"):
        if P <= 0 or R < 0 or total_days <= 0:
            st.error("Invalid input. Check all values.")
        else:
            rate = R * 12 if per == "Per Month" else R
            T_decimal = total_days / 365
            interest = (P * rate * T_decimal) / 100
            total = P + interest
            y, m, d = days_to_ymd(total_days)
            duration_str = f"{y}Y {m}M {d}D"
            save_record("Simple", P, rate, duration_str, interest, total)
            display_result_table(duration_str, interest, total)

# -----------------------------
# Compound Interest
# -----------------------------
with tab2:
    st.header("Compound Interest")

    col1, col2 = st.columns(2)
    with col1:
        P = st.number_input("Principal Amount (₹)", min_value=0, step=100.0, format="%.2f", key="ci_p")
    with col2:
        R = st.number_input("Rate of Interest (%)", min_value=0, step=0.1, format="%.2f", key="ci_r")

    duration_mode_ci = st.radio("Duration Mode", ["Manual (Y/M/D)", "By Dates"], key="ci_mode")
    if duration_mode_ci == "Manual (Y/M/D)":
        col1, col2, col3 = st.columns(3)
        with col1:
            y_val = st.number_input("Years", min_value=0, step=1, key="ci_y")
        with col2:
            m_val = st.number_input("Months", min_value=0, max_value=11, step=1, key="ci_m")
        with col3:
            d_val = st.number_input("Days", min_value=0, max_value=30, step=1, key="ci_d")
        total_days = y_val*365 + m_val*30 + d_val
    else:
        start_date = st.date_input("Start Date", key="ci_start")
        end_date = st.date_input("End Date", key="ci_end")
        delta = end_date - start_date
        total_days = delta.days if delta.days > 0 else 0

    per = st.radio("Rate Type", ["Per Year", "Per Month"], key="ci_per")
    freq = st.selectbox("Compounding Frequency", ["Yearly","Half-Yearly","Quarterly","Monthly","Daily"], key="ci_freq")
    freq_map = {"Yearly":1, "Half-Yearly":2, "Quarterly":4, "Monthly":12, "Daily":365}
    n_val = freq_map[freq]

    if st.button("🚀 Calculate Compound Interest"):
        if P <= 0 or R < 0 or total_days <= 0:
            st.error("Invalid input. Check all values.")
        else:
            rate = R * 12 if per == "Per Month" else R
            T_decimal = total_days / 365
            amount = P * (1 + rate/(100*n_val))**(n_val*T_decimal)
            interest = amount - P
            y, m, d = days_to_ymd(total_days)
            duration_str = f"{y}Y {m}M {d}D"
            save_record("Compound", P, rate, duration_str, interest, amount, frequency=freq)
            display_result_table(duration_str, interest, amount, frequency=freq)

# -----------------------------
# Records Tab
# -----------------------------
with tab3:
    st.header("Calculation History")
    if st.button("Clear All Records"):
        st.session_state.records = []
    if not st.session_state.records:
        st.info("No calculations yet. Start calculating to see history!")
    else:
        for rec in st.session_state.records:
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
