## app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

## Laden des Beispiel-Datensatzes
url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv"
df = pd.read_csv(url)

## Streamlit-App
st.title("Airline Safety Dashboard")

## Sidebar-Eingabefelder
airline_choice = st.sidebar.multiselect("Select Airlines", df["airline"].unique())

## Datenfilterung
filtered_df = df[df["airline"].str.contains('|'.join(airline_choice), case=False)]
filtered_df = filtered_df[filtered_df["airline"].isin(airline_choice)]

# Calculate total incidents, fatal incidents, and fatalities
filtered_df["total_incidents"] = filtered_df["incidents_85_99"] + filtered_df["incidents_00_14"]
filtered_df["total_fatal_incidents"] = filtered_df["fatal_accidents_85_99"] + filtered_df["fatal_accidents_00_14"]
filtered_df["total_fatalities"] = filtered_df["fatalities_85_99"] + filtered_df["fatalities_00_14"]

# Data visualization
st.dataframe(filtered_df)

fig, ax = plt.subplots(figsize=(12, 6))
bar_width = 0.25
index = np.arange(len(filtered_df))

# Plot normal incidents
normal_incidents = ax.bar(index, filtered_df["total_incidents"], bar_width, label="Normal Incidents")
ax.bar_label(normal_incidents, padding=3)

# Plot fatal incidents
fatal_incidents = ax.bar(index + bar_width, filtered_df["total_fatal_incidents"], bar_width, label="Fatal Incidents")
ax.bar_label(fatal_incidents, padding=3)

# Plot fatalities
fatalities = ax.bar(index + 2 * bar_width, filtered_df["total_fatalities"], bar_width, label="Fatalities")
ax.bar_label(fatalities, padding=3)

ax.set_xticks(index + bar_width)
ax.set_xticklabels(filtered_df["airline"], rotation=90)
ax.set_title("Total Incidents, Fatal Incidents, and Fatalities per Airline (1985-2014)")
ax.legend()

st.pyplot(fig)