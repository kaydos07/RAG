from datetime import datetime
from app.config.database import supabase
from app.utils.text_splitter import split_content
from app.config.llm import embedding

def save_event(title: str, description: str, date: str): 
    """Save an upcoming event with its title, detailed description, and scheduled date/time into memory"""
    parent_chunk = split_content(description, 1500)
    for parent in parent_chunk:
        try:
            parent_data_exec = (
                supabase.table("parent_chunk_memory")
                .insert({
                    "description": f"title: {title} ||  | date: {date} \n {parent} "
                })
                .execute()
            )
        except Exception as e:
            print(f"[save_event] Lỗi lưu parent chunk: {e}")
            return {"success": False, "error": f"Cannot save parent chunk: {e}"}
        parent_id = parent_data_exec.data[0]["id"]
        child_chunk = split_content(parent, 150)
        child_collection = []
        for child in child_chunk: 
            child_des = f"title: {title} | date: {date} \n {child} "
            embedded_child = embedding(child_des, "RETRIEVAL_DOCUMENT")
            child_collection.append({
                "description": child_des,
                "parent_chunk_id": parent_id,
                "embedding_vector": embedded_child
            })
        try: 
            child_data_exec = (
                supabase.table("child_chunk_memory")
                .insert(child_collection)
                .execute()
            )
        except Exception as e:
            print(f"[save_event] Lỗi xử lý/lưu child chunks: {e}")
            supabase.table("parent_chunk_memory").delete().eq("id", parent_id).execute()
            return {"success": False, "error": f"Cannot save child chunks: {e}"}
    return {"success": True, "message" : "event saved successfully to memory"}
    