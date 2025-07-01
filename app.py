import sys
import sqlite3
sys.modules["sqlite3"] = sqlite3
import streamlit as st
from Vectorstore.index import get_index_from_chroma
from chat.engine import create_chat_engine
from config.settings import add_api_key
from google.genai.errors import ServerError
import nest_asyncio

nest_asyncio.apply()

# ---------------------------- SETUP ----------------------------------

def setup_chat_engine(course_name, gemini_api_key):
    try:
        if gemini_api_key:
            add_api_key(gemini_api_key)

        index = get_index_from_chroma(course_name)
        chat_engine = create_chat_engine(index)

        st.session_state.chat_engine = chat_engine
        st.session_state.index_loaded = True
        st.success(f"✅ Loaded course: {course_name}")
    except Exception as e:
        st.session_state.index_loaded = False
        st.error(f"❌ Failed to load index: {e}")

# -------------------------- PAGE CONFIG ------------------------------

st.set_page_config(
    page_title="Modular RAG Chat",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------- SESSION STATE INIT -----------------------

if "chat_engine" not in st.session_state:
    st.session_state.chat_engine = None
if "index_loaded" not in st.session_state:
    st.session_state.index_loaded = False
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = ""
if "selected_course" not in st.session_state:
    st.session_state.selected_course = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}  # Stores messages per course
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# --------------------------- HEADER ----------------------------------

st.title("🧠 Ragademic")
st.markdown("Select a course → Activate the knowledge engine → Let the dialogue begin.")

# -------------------------- SIDEBAR ----------------------------------

with st.sidebar:
    st.header("🔑 API Configuration")

    # Gemini API Key
    api_key = st.text_input(
        "Enter Gemini API Key:",
        type="password",
        value=st.session_state.gemini_api_key,
        help="Get your API key from: https://aistudio.google.com/app/apikey"
    )

    if api_key and api_key != st.session_state.gemini_api_key:
        st.session_state.gemini_api_key = api_key
        st.rerun()

    # Gate rest of app
    if not st.session_state.gemini_api_key:
        st.warning("🚫 Please enter your Gemini API key to begin.")
        st.stop()

    st.divider()
    st.header("📚 Select Course")

    course_options = ["Select course","Algorithms", "Computer-Networks", "Theory-of-Automata"]

    # Ensure selected course is in course_options
    if st.session_state.selected_course not in course_options:
        st.session_state.selected_course = course_options[0]

    current_index = course_options.index(st.session_state.selected_course)
    selected_course = st.selectbox(
        "Select Course Collection:",
        course_options,
        index=current_index,
        key="course_selector"
    )

    # Handle course switch
    if selected_course != st.session_state.selected_course:
        # Save current chat to history
        if st.session_state.selected_course and st.session_state.messages:
            st.session_state.chat_history[st.session_state.selected_course] = st.session_state.messages

        # Restore previous messages or start fresh
        st.session_state.messages = st.session_state.chat_history.get(selected_course, [])
        st.session_state.selected_course = selected_course
        setup_chat_engine(selected_course, st.session_state.gemini_api_key)
        st.rerun()

    # Show previous course chats (if any)
    if st.session_state.chat_history:
        st.subheader("🧾 Previous Chats")
        for course, messages in st.session_state.chat_history.items():
            if course != st.session_state.selected_course:
                if st.button(f"💬 Continue: {course}", key=f"continue_{course}"):
                    st.session_state.chat_history[st.session_state.selected_course] = st.session_state.messages
                    st.session_state.messages = messages
                    st.session_state.selected_course = course
                    setup_chat_engine(course, st.session_state.gemini_api_key)
                    st.rerun()

    st.divider()
    st.header("📄 Upload Documents (Disabled for Now)")

    uploaded_files = st.file_uploader(
        "Upload Documents",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True,
        help="Upload your files (processing not enabled yet)"
    )

    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
        st.success(f"✅ {len(uploaded_files)} files uploaded")
        with st.expander("📋 Uploaded Files"):
            for file in uploaded_files:
                st.write(f"• **{file.name}** ({file.size:,} bytes)")

    st.button("🚀 Process Uploads (Disabled)", disabled=True)

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.chat_history[st.session_state.selected_course] = []

# ------------------------ CHAT INTERFACE -----------------------------

if st.session_state.index_loaded:
    for msg in st.session_state.messages:
        role = "🤖 Assistant: \n" if msg["role"] == "assistant" else "👤 You:\n"
        st.markdown(f"**{role}** {msg['content']}")

    if prompt := st.chat_input("Ask something from the selected course..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat_engine.chat(prompt)
                response_text = str(response.response) if hasattr(response, "response") else str(response)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                st.markdown(f"**🤖 Assistant:** {response_text}")
            except ServerError:
                error_msg = "❌ Gemini LLM is overloaded (503). Please try again later."
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.error(error_msg)
            except Exception as e:
                error_msg = f"❌ Unexpected error: {e}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.error(error_msg)
else:
    st.info("⚠️ Select a course to initialize the chat engine.")

# ---------------------------- FOOTER ---------------------------------

st.markdown("---")
st.markdown("Made with ❤️ using LlamaIndex and ChromaDB 🔍🧠")
