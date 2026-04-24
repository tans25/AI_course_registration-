import streamlit as st

# 🎨 Page config
st.set_page_config(
    page_title="AI Course Copilot",
    layout="centered"
)

# 🎨 Custom colors (UMD theme: red, gold, white)
st.markdown(
    """
    <style>
    body {
        background-color: white;
    }
    .stApp {
        background-color: white;
    }
    h1 {
        color: #E21833;  /* red */
        text-align: center;
    }
    .stButton>button {
        background-color: #FFD700;  /* gold */
        color: black;
        font-weight: bold;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🧠 Title
st.markdown("<h1>🎓 AI Course Copilot</h1>", unsafe_allow_html=True)

# 📥 Input box
user_input = st.text_input(
    "Ask your question:",
    placeholder="e.g. Easy courses for ML career"
)

# 🚀 Ask button
if st.button("Ask"):
    if user_input:
        # For now: placeholder response
        response = f"🤖 Thinking...\n\nYou asked: '{user_input}'\n\n(Soon this will return AI recommendations)"

        # 📤 Display response
        st.markdown("### 📊 Recommendations")
        st.write(response)
    else:
        st.warning("Please enter a question.")

# 📦 Optional footer
st.markdown("---")