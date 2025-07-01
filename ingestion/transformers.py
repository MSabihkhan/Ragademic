from llama_index.core.node_parser import SentenceSplitter



text_slitter = SentenceSplitter(separator=" ", chunk_size=1024 , chunk_overlap=128)

