import streamlit as st
from datetime import datetime
import pandas as pd

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

def days_to_ymd(total_days):
    years = total_days // 365
    remaining_days = total_days % 365
    months = remaining_days // 30
    days = remaining_days % 30
    return  int(days), int(months), int(years)

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
        return float(input_str.strip()) if input_str.strip() != "" else 0.0
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
        P_text = st.text_input("Principal Amount (₹)", placeholder="₹")
    with col2:
        R_text = st.text_input("Rate of Interest (%)", placeholder="%")

    P = parse_number(P_text)
    R = parse_number(R_text)

    duration_mode = st.radio("Duration Mode", ["Manual (Y/M/D)", "By Dates"], key="si_mode")

    if duration_mode == "Manual (Y/M/D)":
        col1, col2, col3 = st.columns(3)
        with col1:
            y_val = st.text_input("Years", placeholder="Y")
            y_val = int(y_val) if y_val and y_val.isdigit() else 0
        with col2:
            m_val = st.text_input("Months", placeholder="M")
            m_val = int(m_val) if m_val and m_val.isdigit() else 0
        with col3:
            d_val = st.text_input("Days", placeholder="D")
            d_val = int(d_val) if d_val and d_val.isdigit() else 0
        total_days = y_val*365 + m_val*30 + d_val

        
    else:
        # show dates in DD/MM/YYYY format
        start_date = st.date_input("Start Date", key="si_start", format="DD/MM/YYYY")
        end_date = st.date_input("End Date", key="si_end", format="DD/MM/YYYY")
        delta = end_date - start_date
        total_days = delta.days if delta.days > 0 else 0

    per = st.radio("Rate Type", ["Per Year", "Per Month"], key="si_per")

    if st.button("🚀 Calculate Simple Interest"):
        if P is None or R is None or total_days <= 0 or P <= 0 or R < 0:
            st.error("Invalid input. Check all values.")
        else:
            if per == "Per Month":
                R = R * 12
            T_decimal = total_days / 365
            interest = (P * R * T_decimal) / 100
            total = P + interest
            y, m, d = days_to_ymd(total_days)
            duration_str = f"{y}Y {m}M {d}D"
            save_record("Simple", P, R, duration_str, interest, total)
            display_result_table(duration_str, interest, total)

# -----------------------------
# Compound Interest
# -----------------------------
with tab2:
    st.header("Compound Interest")

    col1, col2 = st.columns(2)
    with col1:
        P_text = st.text_input("Principal Amount (₹)", placeholder="₹", key="ci_p")
    with col2:
        R_text = st.text_input("Rate of Interest (%)", placeholder="%", key="ci_r")

    P = parse_number(P_text)
    R = parse_number(R_text)

    duration_mode_ci = st.radio("Duration Mode", ["Manual (Y/M/D)", "By Dates"], key="ci_mode")
    if duration_mode_ci == "Manual (Y/M/D)":
        col1, col2, col3 = st.columns(3)
        with col1:
            y_val = st.text_input("Years", placeholder="Y", key="ci_y")
            y_val = int(y_val) if y_val and y_val.isdigit() else 0
        with col2:
            m_val = st.text_input("Months", placeholder="M", key="ci_m")
            m_val = int(m_val) if m_val and m_val.isdigit() else 0
        with col3:
            d_val = st.text_input("Days", placeholder="D", key="ci_d")
            d_val = int(d_val) if d_val and d_val.isdigit() else 0
        total_days = y_val*365 + m_val*30 + d_val
    else:
        # show dates in DD/MM/YYYY format
        start_date = st.date_input("Start Date", key="ci_start", format="DD/MM/YYYY")
        end_date = st.date_input("End Date", key="ci_end", format="DD/MM/YYYY")
        delta = end_date - start_date
        total_days = delta.days if delta.days > 0 else 0

    per = st.radio("Rate Type", ["Per Year", "Per Month"], key="ci_per")
    freq = st.selectbox("Compounding Frequency", ["Yearly","Half-Yearly","Quarterly","Monthly","Daily"], key="ci_freq")
    freq_map = {"Yearly":1, "Half-Yearly":2, "Quarterly":4, "Monthly":12, "Daily":365}
    n_val = freq_map[freq]

    if st.button("🚀 Calculate Compound Interest"):
        if P is None or R is None or total_days <= 0 or P <= 0 or R < 0:
            st.error("Invalid input. Check all values.")
        else:
            if per == "Per Month":
                R = R * 12
            T_decimal = total_days / 365
            amount = P * (1 + R/(100*n_val))**(n_val*T_decimal)
            interest = amount - P
            y, m, d = days_to_ymd(total_days)
            duration_str = f"{y}Y {m}M {d}D"
            save_record("Compound", P, R, duration_str, interest, amount, frequency=freq)
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
 
      
