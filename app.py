import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("data/HHS_Unaccompanied_Alien_Children_Program.csv")

# Display first 5 rows
print(df.head())

print("\nDataset Information:")
print(df.info())

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Check duplicate rows
print("\nDuplicate Rows:", df.duplicated().sum())

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

# Sort by date
df = df.sort_values("Date")

print(df.head())

print("\nShape of Dataset:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)

print("\nStatistical Summary:")
print(df.describe())

# Rename columns
df.rename(columns={
    "Children apprehended and placed in CBP custody*": "Apprehended",
    "Children in CBP custody": "CBP_Custody",
    "Children transferred out of CBP custody": "Transferred",
    "Children in HHS Care": "HHS_Care",
    "Children discharged from HHS Care": "Discharged"
}, inplace=True)

print("\nUpdated Columns:")
print(df.columns)

#FIX DATA TYPES

numeric_columns = [
    "Apprehended",
    "CBP_Custody",
    "Transferred",
    "HHS_Care",
    "Discharged"
]

for col in numeric_columns:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Fill missing values with 0
df[numeric_columns] = df[numeric_columns].fillna(0)

print("\nData Types After Conversion:")
print(df.dtypes)

# KPI CALCULATIONS

df["Transfer_Efficiency"] = df["Transferred"].div(
    df["CBP_Custody"].replace(0, pd.NA)
).fillna(0)

df["Discharge_Effectiveness"] = df["Discharged"].div(
    df["HHS_Care"].replace(0, pd.NA)
).fillna(0)

df["Pipeline_Throughput"] = df["Discharged"].div(
    df["Apprehended"].replace(0, pd.NA)
).fillna(0)

df["Backlog"] = df["Apprehended"] - df["Discharged"]

df["Outcome_Stability"] = (
    df["Discharge_Effectiveness"]
    .rolling(window=7)
    .std()
)

df["Outcome_Stability"] = (
    df["Discharge_Effectiveness"]
    .rolling(window=7)
    .std()
)

print("\nKPI Columns:")
print(df[[
    "Transfer_Efficiency",
    "Discharge_Effectiveness",
    "Pipeline_Throughput",
    "Backlog",
    "Outcome_Stability"
]].head())


df.to_csv("data/cleaned_uac_data.csv", index=False)

print("\nDataset with KPIs saved successfully!")

# Daily Apprehensions Trend
plt.figure(figsize=(12,6))

plt.plot(df["Date"], df["Apprehended"])

plt.title("Daily Children Apprehended")
plt.xlabel("Date")
plt.ylabel("Number of Children")

plt.grid(True)

plt.show()

plt.figure(figsize=(12,6))

plt.plot(df["Date"], df["CBP_Custody"], label="CBP Custody")
plt.plot(df["Date"], df["HHS_Care"], label="HHS Care")

plt.title("CBP vs HHS Population")
plt.xlabel("Date")
plt.ylabel("Children")

plt.legend()
plt.grid(True)

plt.show()

# GRAPH 1

plt.figure(figsize=(12,6))
plt.plot(df["Date"], df["Apprehended"])
plt.title("Daily Children Apprehended")
plt.xlabel("Date")
plt.ylabel("Number of Children")
plt.grid(True)
plt.show()

# GRAPH 2

plt.figure(figsize=(12,6))
plt.plot(df["Date"], df["CBP_Custody"], label="CBP Custody")
plt.plot(df["Date"], df["HHS_Care"], label="HHS Care")
plt.title("Children in CBP Custody vs HHS Care")
plt.xlabel("Date")
plt.ylabel("Number of Children")
plt.legend()
plt.grid(True)
plt.show()

# GRAPH 3

plt.figure(figsize=(12,6))
plt.plot(df["Date"], df["Transfer_Efficiency"], color="green")
plt.title("Transfer Efficiency Ratio")
plt.xlabel("Date")
plt.ylabel("Transfer Efficiency")
plt.grid(True)
plt.show()

# GRAPH 4

plt.figure(figsize=(12,6))
plt.plot(df["Date"], df["Discharge_Effectiveness"], color="orange")
plt.title("Discharge Effectiveness")
plt.xlabel("Date")
plt.ylabel("Discharge Effectiveness")
plt.grid(True)
plt.show()

# GRAPH 5

plt.figure(figsize=(12,6))
plt.plot(df["Date"], df["Pipeline_Throughput"], color="purple")
plt.title("Pipeline Throughput")
plt.xlabel("Date")
plt.ylabel("Pipeline Throughput")
plt.grid(True)
plt.show()

# GRAPH 6

plt.figure(figsize=(12,6))
plt.plot(df["Date"], df["Backlog"], color="red")
plt.title("Backlog Accumulation")
plt.xlabel("Date")
plt.ylabel("Backlog")
plt.grid(True)
plt.show()

# GRAPH 7

plt.figure(figsize=(12,6))
plt.plot(df["Date"], df["Outcome_Stability"], color="brown")
plt.title("Outcome Stability")
plt.xlabel("Date")
plt.ylabel("Stability Score")
plt.grid(True)
plt.show()