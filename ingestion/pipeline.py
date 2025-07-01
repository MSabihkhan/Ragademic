from llama_index.core.ingestion import IngestionPipeline
from ingestion.transformers import text_slitter
import time

pipeline = IngestionPipeline(
    transformations=[
        text_slitter
        ]
    )

def run_pipeline(docs):
    all_nodes = []
    for i, doc in enumerate(docs):
        print(f"📄 Processing document {i + 1}/{len(docs)}")
        nodes = pipeline.run(documents=[doc], in_place=True, show_progress=True)
        all_nodes.extend(nodes) 
    print("Document Processing done")
    time.sleep(2)
    return all_nodes
