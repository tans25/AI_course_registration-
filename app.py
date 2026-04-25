import streamlit as st
import json
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 🎨 Page config
st.set_page_config(
    page_title="AI Course Copilot",
    layout="centered"
)

# 🎨 Custom colors (UMD theme: red, gold)
st.markdown(
    """
    <style>
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

# 📚 Load course dataset from data.json
@st.cache_data
def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except Exception as e:
        return []

COURSE_DATA = load_data()

def get_recommendations(user_query):
    if not COURSE_DATA:
        return "⚠️ Error: Could not load course data from `data.json`."

    # Retrieve Hugging Face API key
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        return "⚠️ Error: `HF_TOKEN` is missing. Please create a free token at huggingface.co and set it in your `.env` file."
    
    # Initialize the client with Qwen open source model (no approval needed)
    client = InferenceClient("Qwen/Qwen2.5-72B-Instruct", token=hf_token)
    
    system_prompt = """You are a campus academic advisor for MSDS/MSAI students at UMD.
Your job:
- Recommend 2–3 courses from the provided list based on the user's goal.
- Explain why they fit the student’s goal.
- Mention difficulty (easy/medium/hard).
- Include career relevance.
- Keep answers short, structured, and friendly."""

    user_prompt = f"Course data:\n{json.dumps(COURSE_DATA, indent=2)}\n\nUser question: {user_query}"

    try:
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1024,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error calling Hugging Face API: {e}\n\n*Note: If the error persists, please check your HF_TOKEN.*"

def handle_query(query):
    with st.spinner("🤖 Thinking like your advisor..."):
        response = get_recommendations(query)
        st.markdown("### 📊 Recommendations")
        st.write(response)

# 📥 Input box
user_input = st.text_input(
    "Ask your question:",
    placeholder="e.g. Easy courses for ML career"
)

# 🚀 Suggested queries
st.markdown("### 💡 Suggested Queries")
col1, col2, col3 = st.columns(3)

# Render all buttons first so they don't disappear
btn_gpa = col1.button("GPA boost")
btn_ml = col2.button("ML career path")
btn_easy = col3.button("Easy electives")
btn_ask = st.button("Ask")

# Determine the query
query_to_run = None
if btn_gpa:
    query_to_run = "Easy courses for GPA boost"
elif btn_ml:
    query_to_run = "Best courses for ML career"
elif btn_easy:
    query_to_run = "Easy electives"
elif btn_ask:
    if user_input:
        query_to_run = user_input
    else:
        st.warning("Please enter a question.")

# Execute if a query was selected
if query_to_run:
    handle_query(query_to_run)

# 📦 Optional footer
st.markdown("---")