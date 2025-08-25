import streamlit as st
import pandas as pd
import plotly.express as px

# Load the cleaned Excel file
excel_file = "Cleaned_MF_Tracker.xlsx"
fund_schedule_df = pd.read_excel(excel_file, sheet_name="Fund Schedule", engine="openpyxl")
mf_confos_df = pd.read_excel(excel_file, sheet_name="MF confos", engine="openpyxl")

# Set page config
st.set_page_config(page_title="Managed Fund Tracker", layout="wide")

# Title and description
st.title("📊 Managed Fund Tracker Dashboard")
st.markdown("""
This dashboard provides an overview of managed fund lodgements and confirmations.
Use the filters and charts below to explore fund statuses and transaction details.
""")

# Section 1: Bar chart of fund status counts
st.subheader("Fund Status Overview")
if "STATUS" in fund_schedule_df.columns:
    status_counts = fund_schedule_df["STATUS"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    fig = px.bar(status_counts, x="Status", y="Count", color="Status", title="Fund Status Counts")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("STATUS column not found in Fund Schedule sheet.")

# Section 2: Table of pending lodgements
st.subheader("Pending Lodgements")
if "STATUS" in fund_schedule_df.columns:
    pending_df = fund_schedule_df[fund_schedule_df["STATUS"].str.lower() == "pending"]
    st.dataframe(pending_df)
else:
    st.warning("STATUS column not found for filtering pending lodgements.")

# Section 3: Searchable and filterable MF confos table
st.subheader("MF Confos Transactions")
if not mf_confos_df.empty:
    search_term = st.text_input("🔍 Search transactions by Case Number or Transaction Type")
    filtered_df = mf_confos_df.copy()
    if search_term:
        filtered_df = filtered_df[
            filtered_df["Case Number"].astype(str).str.contains(search_term, case=False, na=False) |
            filtered_df["Transaction Type"].astype(str).str.contains(search_term, case=False, na=False)
        ]
    st.dataframe(filtered_df)
else:
    st.info("No transaction data available in MF confos sheet.")

# Section 4: Placeholders for PDF export and email alerts
st.subheader("📤 Export & Alerts")
st.markdown("""
- **PDF Export**: [Coming Soon] Export summary or full table to PDF.
- **Email Alerts**: [Coming Soon] Notify when a fund is pending too long or rejected.
""")
