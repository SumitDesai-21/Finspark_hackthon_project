import streamlit as st
import requests
import os

# Page configuration
st.set_page_config(
    page_title="BankSaathi",
    page_icon="🤖",  # Using emoji instead of image file
    layout="wide"
)

st.title("BankSaathi 🤖")

# Custom CSS for styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
}

.stMarkdown, .stText, .stMetric, .stPlotlyChart {
    font-family: 'Poppins', sans-serif !important;
}

/* Reduce gap between columns */
[data-testid="column"] {
    padding: 0 5px !important;
}

/* Align title and image closer */
[data-testid="column"]:first-child {
    padding-right: 0 !important;
}

[data-testid="column"]:last-child {
    padding-left: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# Title and icon side by side
col1, col2 = st.columns([4, 1])
with col1:
    st.title("BankSaathi")
with col2:
    # Try to load the image, if not available use an emoji
    try:
        if os.path.exists("chatbot.png"):
            st.image("chatbot.png", width=60)
        else:
            st.markdown("<h1 style='text-align: center; font-size: 60px;'>🤖</h1>", unsafe_allow_html=True)
    except:
        st.markdown("<h1 style='text-align: center; font-size: 60px;'>🤖</h1>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Take input from user
prompt = st.chat_input("Ask me about banking services...")
if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Send message to Rasa backend
    try:
        response = requests.post(
            "http://localhost:5005/webhooks/rest/webhook",
            json={"sender": "user", "message": prompt}
        )
        bot_response = ""
        for r in response.json():
            if "text" in r:
                bot_response += r["text"] + "\n"

        # Display bot response
        with st.chat_message("assistant"):
            st.markdown(bot_response)

        # Add bot response to history
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

    except Exception as e:
        error_msg = f"⚠️ Couldn't reach Rasa backend. Error: {e}"
        with st.chat_message("assistant"):
            st.markdown(error_msg)
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
