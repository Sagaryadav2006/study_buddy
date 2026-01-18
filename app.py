import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4A90E2;
        color: white;
        font-weight: bold;
    }
    .stTextArea textarea {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        st.error("⚠️ API Key missing! Please set GOOGLE_API_KEY in st.secrets for deployment.")
        st.stop()
        
    genai.configure(api_key=api_key)
    
except Exception as e:
    st.error(f"⚠️ Error configuring API: {e}")
    st.stop()

def get_gemini_response(prompt_text):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        with st.spinner("🤖 AI is thinking..."):
            response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

st.markdown('<div class="main-header">🎓 AI Study Buddy</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your personal tutor for explanations, summaries, and quizzes.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("📝 How to use")
    st.info(
        "1. Paste your study notes or a topic name.\n"
        "2. Choose a tab (Explain, Summarize, etc.).\n"
        "3. Click the button to generate magic!"
    )
    st.divider()
    st.caption("Powered by Google Gemini 1.5 Flash")

user_input = st.text_area("Paste your topic, question, or notes here:", height=150, placeholder="E.g., Explain Quantum Entanglement or paste a paragraph about History...")

tab1, tab2, tab3, tab4 = st.tabs(["📖 Explain Concept", "📝 Summarize Notes", "❓ Generate Quiz", "🗂️ Flashcards"])

with tab1:
    st.markdown("### Simplify Complex Topics")
    st.caption("Get a simple, easy-to-understand explanation with examples.")
    
    if st.button("Explain This"):
        if user_input:
            prompt = f"""
            Act as an expert tutor. Explain the following concept or text to a student in simple terms. 
            Use analogies where possible.
            
            Topic/Text: {user_input}
            """
            response = get_gemini_response(prompt)
            st.markdown("---")
            st.markdown(response)
        else:
            st.warning("Please enter a topic first.")

with tab2:
    st.markdown("### Quick Summary")
    st.caption("Turn long notes into bullet points.")
    
    if st.button("Summarize Notes"):
        if user_input:
            prompt = f"""
            Summarize the following text into concise bullet points. 
            Capture the key dates, definitions, and main ideas.
            
            Text: {user_input}
            """
            response = get_gemini_response(prompt)
            st.success("Summary generated!")
            st.markdown(response)
        else:
            st.warning("Please enter some text to summarize.")

with tab3:
    st.markdown("### Test Your Knowledge")
    st.caption("Generate 3 multiple-choice questions based on the input.")
    
    if st.button("Create Quiz"):
        if user_input:
            prompt = f"""
            Create a mini-quiz with 3 multiple-choice questions based on the topic below.
            Format it clearly with the question, options (A, B, C, D), and show the correct answer at the very bottom hidden by a spoiler tag or separated clearly.
            
            Topic: {user_input}
            """
            response = get_gemini_response(prompt)
            st.markdown("---")
            st.markdown(response)
        else:
            st.warning("Please enter a topic for the quiz.")

with tab4:
    st.markdown("### Study Flashcards")
    st.caption("Generate front/back flashcard content.")
    
    if st.button("Make Flashcards"):
        if user_input:
            prompt = f"""
            Create 5 study flashcards based on the text below.
            Format them exactly like this:
            
            **Front:** [Concept/Question]
            **Back:** [Answer/Definition]
            ---
            
            Text: {user_input}
            """
            response = get_gemini_response(prompt)
            st.markdown("---")
            st.markdown(response)
        else:
            st.warning("Please enter a topic.")

st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>Built with Streamlit & Gemini API</div>", unsafe_allow_html=True)