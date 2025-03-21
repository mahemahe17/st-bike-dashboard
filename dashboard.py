import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
df_day = pd.read_csv("data1.csv")
df_hour = pd.read_csv("data2.csv")

# Pastikan kolom "dteday" sudah dalam format datetime
df_day["dteday"] = pd.to_datetime(df_day["dteday"])
df_hour["dteday"] = pd.to_datetime(df_hour["dteday"])

# Membuat Komponen Filter
min_date = df_day["dteday"].min()
max_date = df_day["dteday"].max()

# Sidebar untuk Filter Data
with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

filtered_data = df_day[(df_day["dteday"] >= pd.to_datetime(start_date)) & 
                          (df_day["dteday"] <= pd.to_datetime(end_date))]

st.title("Bike Sharing Dashboard")

col1, col2 = st.columns([3,1])

with col1:
    st.subheader("Daily Bike Sharing")

with col2:
    total_orders = filtered_data.cnt.sum()
    st.metric("Total Daily Bike Sharing", value=total_orders)
 
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

# Membuat kolom baru untuk menyimpan tipe cuaca
df_day["weather_type"] = df_day["weathersit"].map({
    1: "Clear",
    2: "Cloudy",
    3: "Light Rain",
    4: "Heavy Rain"
})

# Membuat kolom baru "temp_actual" untuk menyimpan nilai "temp" sebelum dinormalisasi
df_day["temp_actual"] = df_day["temp"] * 41

st.subheader("Hubungan Suhu dan Tipe Cuaca Terhadap Jumlah Peminjaman")
plt.figure(figsize=(10, 6))
sns.scatterplot(x='temp_actual', y='cnt', hue='weather_type', data=df_day, alpha=0.7)
plt.title("Hubungan Suhu dan Tipe Cuaca Terhadap Jumlah Peminjaman")
plt.xlabel("Suhu (Celsius)")
plt.ylabel("Jumlah Penyewaan (cnt)")
plt.legend(title="Weather Type")
st.pyplot(plt)

st.subheader("Tren Rata-Rata Jumlah Peminjaman Sepeda per Jam dalam Sehari")

# Hitung rata-rata jumlah peminjaman sepeda per jam
hourly_avg = df_hour.groupby('hr')['cnt'].mean().reset_index()

# Visualisasi Line Plot
plt.figure(figsize=(12, 6))
sns.lineplot(x='hr', y='cnt', data=hourly_avg, marker='o', color='blue')
plt.title("Tren Rata-Rata Jumlah Peminjaman Sepeda per Jam dalam Sehari")
plt.xlabel("Jam (0-23)")
plt.ylabel("Rata-Rata Jumlah Peminjaman Sepeda")
plt.xticks(range(0, 24))
plt.grid(True)
st.pyplot(plt)