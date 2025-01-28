import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset yang telah di export sebelumnya
all_df = pd.read_csv('all_data.csv')

# Convert 'dteday' ke datetime format untuk memastikan tidak ada error terkait tipe data
all_df['dteday'] = pd.to_datetime(all_df['dteday'])

# Streamlit Dashboard
st.title("Bike Sharing Data Dashboard")
st.sidebar.header("Filters") # sidebar

# Sidebar filters

season_filter = st.sidebar.multiselect( # filter untuk season
    "Select Seasons:",
    options=all_df['season'].unique(),
    default=all_df['season'].unique()
)

hour_range = st.sidebar.slider( # filter untuk jam
    "Select Hour Range:",
    min_value=int(all_df['hr'].min()),
    max_value=int(all_df['hr'].max()),
    value=(int(all_df['hr'].min()), int(all_df['hr'].max())),
    step=1
)

weekday_filter = st.sidebar.multiselect( # filter untuk hari
    "Select Weekdays:",
    options=all_df['weekday'].unique(),
    default=all_df['weekday'].unique()
)

# Filter data
filtered_data = all_df[
    (all_df['season'].isin(season_filter)) &
    (all_df['hr'].between(hour_range[0], hour_range[1])) &
    (all_df['weekday'].isin(weekday_filter))
]

# Show filtered data summary pada halaman utama
st.write("### Filtered Data Summary")
st.dataframe(filtered_data.head())

# ISI KONTEN VISUALISASI
st.write("## Visualizations")

# Line chart for Recency
st.write("### Recency Distribution")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(filtered_data['Recency'], bins=30, kde=True, color='skyblue', ax=ax)
ax.set_title("Recency Distribution", fontsize=16)
ax.set_xlabel("Recency (days since last activity)", fontsize=12)
ax.set_ylabel("Frequency", fontsize=12)
st.pyplot(fig)

# Line chart for Frequency
st.write("### Frequency of Bike Rentals")
fig, ax = plt.subplots(figsize=(10, 5))
rfm_table_sorted_freq = filtered_data.groupby('registered')['cnt'].count().reset_index(name='Frequency').sort_values(by='Frequency', ascending=False)
sns.lineplot(data=rfm_table_sorted_freq, x='registered', y='Frequency', ax=ax, color='orange')
ax.set_title("Frequency of Bike Rentals", fontsize=16)
ax.set_xlabel("Registered Users", fontsize=12)
ax.set_ylabel("Frequency", fontsize=12)
st.pyplot(fig)

# Line chart for Monetary
st.write("### Monetary Value of Bike Rentals")
fig, ax = plt.subplots(figsize=(10, 5))
rfm_table_sorted_monetary = filtered_data.groupby('registered')['cnt'].sum().reset_index(name='Monetary').sort_values(by='Monetary', ascending=False)
sns.lineplot(data=rfm_table_sorted_monetary, x='registered', y='Monetary', ax=ax, color='green')
ax.set_title("Monetary Value of Bike Rentals", fontsize=16)
ax.set_xlabel("Registered Users", fontsize=12)
ax.set_ylabel("Monetary (Total Rentals)", fontsize=12)
st.pyplot(fig)


# Distribution of bike rentals by season
st.write("### Average Bike Rentals by Season")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=filtered_data, x="season", y="cnt", ci=None, palette="Blues_d", ax=ax)
ax.set_title("Average Bike Rentals by Season", fontsize=16)
ax.set_xlabel("Season (1: Spring, 2: Summer, 3: Fall, 4: Winter)", fontsize=12)
ax.set_ylabel("Average Rentals", fontsize=12)
st.pyplot(fig)

# Distribution of rentals by working day
st.write("### Bike Rentals: Working Day vs Non-Working Day")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=filtered_data, x="workingday", y="cnt", ci=None, palette="Oranges_d", ax=ax)
ax.set_title("Bike Rentals: Working Day vs Non-Working Day", fontsize=16)
ax.set_xlabel("Working Day (0: Non-Working, 1: Working)", fontsize=12)
ax.set_ylabel("Average Rentals", fontsize=12)
st.pyplot(fig)

# Impact of weather conditions on bike rentals
st.write("### Impact of Weather Conditions on Bike Rentals")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=filtered_data, x="weathersit", y="cnt", ci=None, palette="Greens_d", ax=ax)
ax.set_title("Impact of Weather Conditions on Bike Rentals", fontsize=16)
ax.set_xlabel("Weather Situation (1: Clear, 2: Mist, 3: Light Snow/Rain, 4: Heavy Rain/Snow)", fontsize=12)
ax.set_ylabel("Average Rentals", fontsize=12)
st.pyplot(fig)

# Scatter plot: Temperature vs Bike Rentals
st.write("### Scatter Plot: Temperature vs Bike Rentals")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=filtered_data, x="temp", y="cnt", alpha=0.5, color="blue", ax=ax)
ax.set_title("Temperature vs Bike Rentals", fontsize=16)
ax.set_xlabel("Normalized Temperature", fontsize=12)
ax.set_ylabel("Bike Rentals", fontsize=12)
st.pyplot(fig)

# Line chart for daily trends
st.write("### Daily Trends in Bike Rentals")
fig, ax = plt.subplots(figsize=(12, 6))
filtered_data.groupby("dteday")["cnt"].sum().plot(ax=ax, color="purple", linewidth=2)
ax.set_title("Daily Trends in Bike Rentals (Filtered)", fontsize=16)
ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Total Bike Rentals", fontsize=12)
st.pyplot(fig)
