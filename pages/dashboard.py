import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

#0E1117
    #FAFAFA
# ---------------------
# 🎨 Page Config
# ---------------------
st.set_page_config(
    page_title="Chatbot Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for Poppins font
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif !important;
}

.stMarkdown, .stText, .stMetric, .stPlotlyChart {
    font-family: 'Poppins', sans-serif !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
}

.stMetric > div > div > div {
    font-family: 'Poppins', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Regional-Language Chatbot Analytics")
st.markdown("An elegant view of chatbot performance and user engagement.")

# ---------------------
# 📦 Generate Dummy Data
# ---------------------
languages = ["Marathi", "Tamil", "Telugu", "Punjabi", "Hindi", "English"]
topics = ["Account Opening", "Fraud Alerts", "UPI Help", "Loan Info", "KYC Process"]

data = []
start_date = datetime.now() - timedelta(days=30)
for i in range(200):
    data.append({
        "date": start_date + timedelta(days=random.randint(0, 30)),
        "language": random.choice(languages),
        "topic": random.choice(topics)
    })

df = pd.DataFrame(data)

# ---------------------
# 📌 KPIs
# ---------------------
total_users = len(df)
unique_languages = df["language"].nunique()
most_used_lang = df["language"].mode()[0]

col1, col2, col3 = st.columns(3)
col1.metric("👥 Total Interactions", f"{total_users}")
col2.metric("🌐 Languages Used", f"{unique_languages}")
col3.metric("🏆 Top Language", most_used_lang)

# ---------------------
# 📊 Charts
# ---------------------

# Language Distribution
lang_counts = df["language"].value_counts().reset_index()
lang_counts.columns = ["Language", "Count"]
fig_lang = px.pie(lang_counts, values="Count", names="Language",
                  title="Language Distribution", color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig_lang, use_container_width=True)

# Usage Over Time
df_daily = df.groupby(df["date"].dt.date).size().reset_index(name="Count")
fig_time = px.line(df_daily, x="date", y="Count",
                   title="Usage Over Time", markers=True)
st.plotly_chart(fig_time, use_container_width=True)

# Topics Breakdown
topic_counts = df["topic"].value_counts().reset_index()
topic_counts.columns = ["Topic", "Count"]
fig_topic = px.bar(topic_counts, x="Topic", y="Count",
                   title="Top Topics Asked", text="Count", color="Topic")
fig_topic.update_traces(textposition="outside")
st.plotly_chart(fig_topic, use_container_width=True)

# ---------------------
# 📌 Footer
# ---------------------
st.markdown("---")
st.markdown("💡 *This dashboard shows demo analytics. Connect it to your chatbot logs for real insights.*")
