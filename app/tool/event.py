from datetime import datetime
from ..function.database import supabase
from ..function.agent import embedding, split_content

def save_event(title: str, description: str, date: datetime): 
    date_iso = date.isoformat()
    parent_chunk = split_content(description, 1500)
    for parent in parent_chunk:
        try:
            parent_data_exec = (
                supabase.table("parent_chunk_memory")
                .insert({
                    "title": title, 
                    "des": parent,
                    "date": date_iso})
                .execute()
            )
        except Exception as e:
            print(f"[save_event] Lỗi lưu parent chunk: {e}")
            return {"success": False, "error": f"Cannot save parent chunk: {e}"}
        parent_id = parent_data_exec.data[0].id
        child_chunk = split_content(parent, 150)
        child_collection = []
        for child in child_chunk: 
            child = f"title: {title} | date: {date_iso} \n {child} "
            embedded_child = embedding(child, "RETRIEVAL_DOCUMENT")
            child_collection.append({
                "description": child,
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
    return {"success": True}
