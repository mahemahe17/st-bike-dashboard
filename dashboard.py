import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
bike_data = pd.read_csv("Bike Sharing Dataset\day.csv")

# Pastikan kolom "dteday" sudah dalam format datetime
bike_data["dteday"] = pd.to_datetime(bike_data["dteday"])

# Membuat Komponen Filter
min_date = bike_data["dteday"].min()
max_date = bike_data["dteday"].max()

# Sidebar untuk Filter Data
with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

filtered_data = bike_data[(bike_data["dteday"] >= pd.to_datetime(start_date)) & 
                          (bike_data["dteday"] <= pd.to_datetime(end_date))]

st.header("Dashboard Bike Sharing")

st.subheader("Daily Bike Sharing")

total_orders = bike_data.cnt.sum()
st.metric("Total Bike Sharing", value=total_orders)
 
fig, ax = plt.subplots(figsize=(18, 6))
ax.plot(
    filtered_data["dteday"],
    filtered_data["cnt"],
    marker='o', 
    linewidth=2,
    color="blue"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader("Bike Sharing Category")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 8))

casual_total = filtered_data["casual"].sum()
registered_total = filtered_data["registered"].sum()

sns.barplot(x=['Casual', 'Registered'], y=[casual_total, registered_total], palette=['orange', 'blue'], ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Types of Bike Sharing", fontsize=20)
ax[0].tick_params(axis='y', labelsize=15)
ax[0].tick_params(axis='x', labelsize=15)

# Kategorisasi Hari
filtered_data["day_type"] = filtered_data.apply(
    lambda row: "Holiday" if row["holiday"] == 1 else ("Weekend" if row["weekday"] in [0, 6] else "Working Day"), 
    axis=1
)
day_type_data = filtered_data.groupby("day_type").cnt.sum().reset_index()

# Visualisasi Bar Chart
sns.barplot(x="day_type", y="cnt", data=day_type_data, palette="Set2", ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Types of Day", fontsize=20)
ax[1].tick_params(axis='y', labelsize=15)
ax[1].tick_params(axis='x', labelsize=15)

st.pyplot(plt)