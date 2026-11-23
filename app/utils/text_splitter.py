from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_content(content: str, chunk_size: int):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_size/10
    )
    split_content = text_splitter.split_text(content)
    
    return split_content