from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core  import Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from google.api_core.exceptions import ServiceUnavailable

import os
import time
llm = None
# 2️⃣ Initialize Google LLM (Gemini)
def add_api_key(gemini_api_key):
    os.environ['GOOGLE_API_KEY'] = gemini_api_key
    for attempt in range(5):
        try:
            print(f"🔁 Attempt {attempt+1}: Initializing Gemini Flash...")
            llm=  GoogleGenAI(model="gemini-2.0-flash")
        except ServiceUnavailable as e:
            print(f"⚠️ Gemini Flash overloaded: {e}")
            time.sleep(5 * (2 ** attempt))
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            break
    Settings.llm = llm
# 3️⃣ Initialize Google GenAI-based embedding model
# embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5", device="cpu")
embed_model = OllamaEmbedding(model_name="nomic-embed-text:v1.5",base_url="http://localhost:11434")

# 4️⃣ Apply global Settings (optional)
Settings.llm = llm
Settings.embed_model = embed_model
