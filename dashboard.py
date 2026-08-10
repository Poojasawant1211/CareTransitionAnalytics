import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Care Transition Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("Care Transition Efficiency & Placement Outcome Analytics")

st.write(
    "Analysis of CBP custody, HHS care, transfers, discharges, "
    "backlog and placement outcomes."
)

df = pd.read_csv("data/cleaned_uac_data.csv")

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date")

st.subheader("Dataset Preview")

st.dataframe(
    df.head(),
    use_container_width=True
)

st.sidebar.header("Dashboard Filters")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

start_date = st.sidebar.date_input(
    "Start Date",
    min_date,
    min_value=min_date,
    max_value=max_date
)

end_date = st.sidebar.date_input(
    "End Date",
    max_date,
    min_value=min_date,
    max_value=max_date
)

# Check invalid date range

if start_date > end_date:
    st.error("Start Date cannot be after End Date.")
    st.stop()

# Filter dataset

filtered_df = df[
    (df["Date"].dt.date >= start_date) &
    (df["Date"].dt.date <= end_date)
].copy()

st.sidebar.write(
    f"Selected period: {start_date} to {end_date}"
)


filtered_df["Transfer_Efficiency"] = (
    filtered_df["Transfer_Efficiency"]
    .replace([float("inf"), -float("inf")], pd.NA)
)

filtered_df["Discharge_Effectiveness"] = (
    filtered_df["Discharge_Effectiveness"]
    .replace([float("inf"), -float("inf")], pd.NA)
)

filtered_df["Pipeline_Throughput"] = (
    filtered_df["Pipeline_Throughput"]
    .replace([float("inf"), -float("inf")], pd.NA)
)

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

# Transfer Efficiency

transfer_efficiency = (
    filtered_df["Transfer_Efficiency"]
    .mean()
)

# Discharge Effectiveness

discharge_effectiveness = (
    filtered_df["Discharge_Effectiveness"]
    .mean()
)

# Pipeline Throughput

total_entries = filtered_df["Apprehended"].sum()
total_exits = filtered_df["Discharged"].sum()

if total_entries > 0:
    pipeline_throughput = total_exits / total_entries
else:
    pipeline_throughput = 0

# Ending Backlog

ending_backlog = (
    filtered_df["Apprehended"].cumsum()
    -
    filtered_df["Discharged"].cumsum()
).iloc[-1]

# Display KPIs

col1.metric(
    "Transfer Efficiency",
    f"{transfer_efficiency:.2%}"
)

col2.metric(
    "Discharge Effectiveness",
    f"{discharge_effectiveness:.2%}"
)

col3.metric(
    "Pipeline Throughput",
    f"{pipeline_throughput:.2%}"
)

col4.metric(
    "Ending Backlog",
    f"{ending_backlog:,.0f}"
)

st.header("Care Pipeline Overview")

col1, col2, col3 = st.columns(3)

total_apprehended = filtered_df["Apprehended"].sum()
total_transferred = filtered_df["Transferred"].sum()
total_discharged = filtered_df["Discharged"].sum()

col1.metric(
    "Total Apprehended",
    f"{total_apprehended:,.0f}"
)

col2.metric(
    "Total Transferred",
    f"{total_transferred:,.0f}"
)

col3.metric(
    "Total Discharged",
    f"{total_discharged:,.0f}"
)

st.header("Care Pipeline Flow")

pipeline_data = pd.DataFrame({
    "Stage": [
        "Apprehended",
        "Transferred to HHS",
        "Discharged"
    ],
    "Children": [
        total_apprehended,
        total_transferred,
        total_discharged
    ]
})

st.bar_chart(
    pipeline_data.set_index("Stage")
)

st.header("Transfer & Discharge Efficiency")

efficiency_data = pd.DataFrame({
    "Metric": [
        "Transfer Efficiency",
        "Discharge Effectiveness",
        "Pipeline Throughput"
    ],
    "Percentage": [
        transfer_efficiency * 100,
        discharge_effectiveness * 100,
        pipeline_throughput * 100
    ]
})

st.bar_chart(
    efficiency_data.set_index("Metric")
)

st.header("Monthly Discharge & Placement Trend")

monthly_data = (
    filtered_df
    .set_index("Date")
    .resample("MS")["Discharged"]
    .sum()
    .reset_index()
)

monthly_data["Month"] = (
    monthly_data["Date"]
    .dt.strftime("%b %Y")
)

st.bar_chart(
    monthly_data.set_index("Month")["Discharged"]
)

st.header("Backlog Analysis")

filtered_df["Cumulative_Entries"] = (
    filtered_df["Apprehended"].cumsum()
)

filtered_df["Cumulative_Exits"] = (
    filtered_df["Discharged"].cumsum()
)

filtered_df["Calculated_Backlog"] = (
    filtered_df["Cumulative_Entries"]
    -
    filtered_df["Cumulative_Exits"]
)

st.bar_chart(
    filtered_df.set_index("Date")["Calculated_Backlog"]
)

st.header("Transfer Efficiency Trend")

st.line_chart(
    filtered_df.set_index("Date")[
        "Transfer_Efficiency"
    ]
)

st.header("Discharge Effectiveness Trend")

st.line_chart(
    filtered_df.set_index("Date")[
        "Discharge_Effectiveness"
    ]
)

st.header("Outcome Stability")

st.line_chart(
    filtered_df.set_index("Date")[
        "Outcome_Stability"
    ]
)


st.header("Bottleneck Detection")

latest_transfer = (
    filtered_df["Transfer_Efficiency"]
    .mean()
)

latest_discharge = (
    filtered_df["Discharge_Effectiveness"]
    .mean()
)


if latest_transfer < 0.50:

    st.warning(
        "⚠️ Low transfer efficiency detected. "
        "Review CBP → HHS transfer performance."
    )

else:

    st.success(
        "✅ Transfer efficiency is within the selected threshold."
    )


if latest_discharge < 0.50:

    st.warning(
        "⚠️ Low discharge effectiveness detected. "
        "Potential placement bottleneck."
    )

else:

    st.success(
        "✅ Discharge effectiveness is within the selected threshold."
    )


st.header("Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

st.header("Executive Summary")

st.write("### Key Findings")

# Highest apprehension
highest_apprehension = filtered_df["Apprehended"].max()

# Highest discharge
highest_discharge = filtered_df["Discharged"].max()

# Maximum backlog
maximum_backlog = filtered_df["Calculated_Backlog"].max()

# Average transfer efficiency
avg_transfer = filtered_df["Transfer_Efficiency"].mean()

# Average discharge effectiveness
avg_discharge = filtered_df["Discharge_Effectiveness"].mean()

col1, col2 = st.columns(2)

with col1:

    st.info(
        f"📌 **Highest Daily Apprehension:** "
        f"{highest_apprehension:,.0f} children"
    )

    st.info(
        f"📌 **Highest Daily Discharge:** "
        f"{highest_discharge:,.0f} children"
    )

    st.info(
        f"📌 **Maximum Calculated Backlog:** "
        f"{maximum_backlog:,.0f} children"
    )

with col2:

    st.info(
        f"📌 **Average Transfer Efficiency:** "
        f"{avg_transfer:.2%}"
    )

    st.info(
        f"📌 **Average Discharge Effectiveness:** "
        f"{avg_discharge:.2%}"
    )

st.header("Recommendations")

st.write("""
### Recommended Actions

1. **Improve CBP → HHS Transfer Efficiency**
   - Monitor periods with low transfer efficiency.
   - Identify delays in the transfer process.

2. **Monitor Discharge Performance**
   - Track discharge effectiveness regularly.
   - Investigate periods where discharges decline.

3. **Reduce Backlog**
   - Identify sustained periods where inflows exceed exits.
   - Prioritize cases contributing to prolonged backlog.

4. **Improve Placement Outcomes**
   - Monitor outcome stability over time.
   - Investigate sudden changes in discharge performance.

5. **Use Date-Based Monitoring**
   - Compare monthly performance.
   - Identify periods of increasing demand or declining throughput.
""")