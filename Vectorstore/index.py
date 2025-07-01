from llama_index.core import VectorStoreIndex,StorageContext
from config.settings import embed_model
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
import uuid
def buildindexandvectorstore(all_nodes):
    index = VectorStoreIndex(all_nodes,embed_model=embed_model )
    
    # db = chromadb.PersistentClient(path ="./chromadb")
    
    # chroma_collection = db.get_or_create_collection("quickstart")
    
    # vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    # Storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return index
def buildChromaDB(all_nodes):
    for node in all_nodes:
        node.id_ = str(uuid.uuid4())
    db = chromadb.PersistentClient(path ="./courseDB")
    chroma_collection = db.get_or_create_collection("Theory-of-Automata")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    Storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex(all_nodes,storage_context=Storage_context)
    return index
def get_index_from_chroma(collection_name):
    db = chromadb.PersistentClient(path ="./courseDB")
    chroma_collection = db.get_or_create_collection(collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    Storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(
    vector_store, storage_context = Storage_context
    )
    return index
