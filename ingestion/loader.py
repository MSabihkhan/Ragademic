from llama_index.core.readers import SimpleDirectoryReader
import tempfile
import os


def save_uploaded_files(uploaded_files):
    """Save uploaded files to temporary directory"""
    temp_dir = tempfile.mkdtemp()
    saved_files = []
    
    for uploaded_file in uploaded_files:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_files.append(file_path)
    
    return temp_dir, saved_files

def load_user_docs(file_paths):
    # Create directory path from first file
    temp_dir = os.path.dirname(file_paths[0])
    
    # Load documents
    docs = SimpleDirectoryReader(temp_dir).load_data()
    
    # Configure document metadata
    for doc in docs:
        doc.text_template = "Metadata:\n{metadata_str}\n---\nContent:\n{content}"
        if "page_label" not in doc.excluded_embed_metadata_keys:
            doc.excluded_embed_metadata_keys.append("page_label")
        if "file_path" not in doc.excluded_embed_metadata_keys:
            doc.excluded_embed_metadata_keys.append("file_path")
    return docs

def load_documents_to_chroma():
    all_docs = []
    for course in os.listdir("data"):
        course_path = os.path.join("data", course)
        if os.path.isdir(course_path):
            print(f"\nProcessing course: {course}")
            raw_docs = SimpleDirectoryReader(course_path).load_data()
            for doc in raw_docs:
                filename = os.path.basename(doc.metadata.get('file_path', ''))
                topic = os.path.splitext(filename)[0]
                doc.metadata.update( {
                    "course": course,
                    "topic": topic
                })
                all_docs.append(doc)
    return all_docs