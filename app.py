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
    .main-header { font-size: 2.5rem; color: #4A90E2; text-align: center; margin-bottom: 1rem; }
    .sub-header { font-size: 1.2rem; color: #555; text-align: center; margin-bottom: 2rem; }
    .stButton>button { width: 100%; background-color: #4A90E2; color: white; font-weight: bold; }
    .stTextArea textarea { background-color: #000000; }
</style>
""", unsafe_allow_html=True)

try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        st.error("⚠️ API Key missing! Please set GOOGLE_API_KEY in st.secrets.")
        st.stop()
        
    genai.configure(api_key=api_key)

    
    @st.cache_resource
    def get_working_model():
        try:
            priority_models = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro', 'gemini-1.0-pro']
            
            available_models = [m.name.replace('models/', '') for m in genai.list_models()]
            
            for model in priority_models:
                if model in available_models:
                    return model
            
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    return m.name.replace('models/', '')
                    
            return "gemini-1.5-flash" 
        except Exception as e:
            return "gemini-1.5-flash"

    model_name = get_working_model()
    model = genai.GenerativeModel(model_name)
    
except Exception as e:
    st.error(f"⚠️ Error configuring API: {e}")
    st.stop()

def get_gemini_response(prompt_text):
    try:
        with st.spinner(f"🤖 AI is thinking (Using {model_name})..."):
            response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

st.markdown('<div class="main-header">🎓 AI Study Buddy</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">Your personal tutor.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("📝 How to use")
    st.info("1. Paste notes.\n2. Choose a tab.\n3. Click button.")
    st.caption(f"Active Model: {model_name}")

user_input = st.text_area("Paste your topic or notes here:", height=150)

tab1, tab2, tab3, tab4 = st.tabs(["📖 Explain", "📝 Summarize", "❓ Quiz", "🗂️ Flashcards"])

with tab1:
    if st.button("Explain This"):
        if user_input:
            prompt = f"Explain this concept in simple terms with analogies: {user_input}"
            st.markdown(get_gemini_response(prompt))
        else:
            st.warning("Please enter a topic.")

with tab2:
    if st.button("Summarize"):
        if user_input:
            prompt = f"Summarize this text into bullet points: {user_input}"
            st.markdown(get_gemini_response(prompt))
        else:
            st.warning("Please enter text.")

with tab3:
    if st.button("Create Quiz"):
        if user_input:
            prompt = f"Create 3 multiple-choice questions about: {user_input}. Include answers at the bottom."
            st.markdown(get_gemini_response(prompt))
        else:
            st.warning("Please enter a topic.")

with tab4:
    if st.button("Make Flashcards"):
        if user_input:
            prompt = f"Create 5 flashcards (Front/Back) for: {user_input}"
            st.markdown(get_gemini_response(prompt))
        else:
            st.warning("Please enter a topic.")

