import streamlit as st
from textblob import TextBlob
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Set wide layout and light theme
st.set_page_config(layout="wide", page_title="Sentiment Analyzer")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Sentiment Analysis", "Sentiment Summary"])

# Initialize session state
if "feedback_list" not in st.session_state:
    st.session_state.feedback_list = []

if page == "Sentiment Analysis":
    st.markdown("<h1 style='text-align: center;'>📊 Real-Time Sentiment Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size: 28px; font-family: Arial;'>📝 Enter your review or feedback:</h3>", unsafe_allow_html=True)
    user_input = st.text_input("", key="user_input")

    def get_sentiment(text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.3:
            sentiment = "😊 Positive"
        elif polarity < -0.3:
            sentiment = "😠 Negative"
        else:
            sentiment = "😐 Neutral"
        return polarity, sentiment

    if user_input:
        polarity, sentiment_label = get_sentiment(user_input)
        st.session_state.feedback_list.append({
            "Text": user_input,
            "Polarity": polarity,
            "Sentiment": sentiment_label,
            "Time": datetime.now()
        })

        # Gauge Chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=polarity,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Polarity Score"},
            gauge={
                'axis': {'range': [-1, 1]},
                'bar': {'color': "black"},
                'steps': [
                    {'range': [-1, -0.3], 'color': "red"},
                    {'range': [-0.3, 0.3], 'color': "yellow"},
                    {'range': [0.3, 1], 'color': "green"},
                ],
            }
        ))

        # Display Gauge and Giphy side by side with equal ratio
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            if "Positive" in sentiment_label:
                gif_url = "https://media.giphy.com/media/l0MYvV7rbVYm2e1Y4/giphy.gif"
            elif "Negative" in sentiment_label:
                gif_url = "https://media.giphy.com/media/QvBgZiA6uDmCEaAFru/giphy.gif"
            else:
                gif_url = "https://media.giphy.com/media/v5WZ2uwiW4VcVay8Sw/giphy.gif"
            st.image(gif_url, use_column_width=True)

        st.markdown(f"<h3 style='text-align:center;'>Sentiment: {sentiment_label}</h3>", unsafe_allow_html=True)
        

elif page == "Sentiment Summary":
    st.markdown("<h1 style='text-align: center;'>📚 Sentiment Summary</h1>", unsafe_allow_html=True)

    if st.session_state.feedback_list:
        df_summary = pd.DataFrame(st.session_state.feedback_list)

        # Show data
        st.markdown("### 🧾 All Feedbacks")
        st.dataframe(df_summary)

        # Sentiment Trend Line
        df_summary['Entry #'] = range(1, len(df_summary) + 1)
        st.markdown("### 📈 Sentiment Polarity Trend:")
        st.line_chart(df_summary.set_index('Entry #')['Polarity'])

        # Summary count
        st.markdown("### 📊 Sentiment Count:")
        st.write(df_summary['Sentiment'].value_counts())

        # Download Button
        csv = df_summary.to_csv(index=False).encode('utf-8')
        st.download_button("Download Summary Report", csv, "summary_report.csv", "text/csv")
    else:
        st.info("No feedbacks to show yet.")
