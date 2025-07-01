from llama_index.core.memory import ChatMemoryBuffer
from config.settings import llm
from llama_index.core.vector_stores import ExactMatchFilter , MetadataFilters

def set_filters(coursename):
    filters = MetadataFilters(filters=[ExactMatchFilter(key="course", value=coursename)])
    return filters

def create_chat_engine(index):
    memory = ChatMemoryBuffer.from_defaults(token_limit=2500)
    chat_engine = index.as_chat_engine(
        chat_mode="context",
        memory=memory,
        system_prompt="You are an AI teaching assistant with deep knowledge of course materials across multiple subjects."
"You use a Retrieval-Augmented Generation (RAG) system to access relevant documents and deliver accurate, context-aware explanations."
"Your goal is to educate clearly and help students understand, using retrieved content to support answers."
"Maintain continuity across the conversation and respond like a helpful, knowledgeable tutor familiar with the entire curriculum."
    )
    return chat_engine
