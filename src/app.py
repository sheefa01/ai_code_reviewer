import streamlit as st
from src.ai.reviewer import CodeReviewer

st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* Premium button styling */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    /* Sleek container styling */
    .st-emotion-cache-16txtl3 {
        padding: 2rem 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI-Powered Python Code Reviewer")
st.markdown("Upload your Python files and get an instant AI code review powered by Llama 3.")

# Initialize the AI Reviewer
@st.cache_resource
def get_reviewer():
    try:
        return CodeReviewer()
    except ValueError as e:
        st.error(f"Configuration Error: {e}")
        return None

reviewer = get_reviewer()

uploaded_file = st.file_uploader("Choose a Python file (.py)", type=["py"])

if uploaded_file is not None:
    st.markdown("### Code Preview")
    code_text = uploaded_file.getvalue().decode("utf-8")
    with st.expander("Show Code"):
        st.code(code_text, language='python')
    
    if st.button("🚀 Generate AI Review", type="primary"):
        if reviewer is None:
            st.error("Please configure your .env file with the GROQ_API_KEY first.")
        else:
            with st.spinner("The AI is analyzing your code..."):
                feedback = reviewer.review_code(code_text, uploaded_file.name)
            
            st.markdown("---")
            st.markdown("## 📋 Review Report")
            st.markdown(feedback)
            st.success("Review generated successfully!")
