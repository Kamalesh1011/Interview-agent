from pymongo import MongoClient
from backend.utils.embedder import get_embedding
from backend.utils.chunker import chunk_text
from backend.rag_engine import faiss_index, EMBEDDING_DIM, rag_chunks_col
import numpy as np
import json
from datetime import datetime

# ---------------------------
# Connect to existing MongoDB
# ---------------------------

client = MongoClient("mongodb+srv://i103:aishu@cluster0.zxk94yv.mongodb.net/?appName=Cluster0")
db = client["interview_system"]
interviews_col = db["interviews"]

print("📌 Connected to MongoDB interview_system")

# ---------------------------
# Fetch all interviews
# ---------------------------

all_interviews = list(interviews_col.find())
print(f"📌 Total interviews found: {len(all_interviews)}")


# ---------------------------
# Iterate and embed each interview
# ---------------------------

counter = 0
chunk_counter = 0

for interview in all_interviews:
    interview_id = interview.get("interview_id")
    student_email = interview.get("student_email")

    final_report = interview.get("final_report", {})

    if not final_report:
        print(f"⚠️ Interview {interview_id} has no final_report. Skipping...")
        continue

    # convert dict to plain text
    report_text = json.dumps(final_report)

    print(f"\n🔍 Processing Interview: {interview_id}")

    chunks = chunk_text(report_text)
    print(f"   → {len(chunks)} chunks created")

    for chunk in chunks:
        embedding = get_embedding(chunk)

        if embedding is None:
            print("   ❌ Embedding failed, skipping chunk")
            continue

        np_vec = np.array(embedding).astype("float32").reshape(1, -1)

        # Add to FAISS
        faiss_index.add(np_vec)

        # Insert chunk metadata to Mongo
        rag_chunks_col.insert_one({
            "interview_id": interview_id,
            "student_email": student_email,
            "text": chunk,
            "embedding_dim": EMBEDDING_DIM,
            "created_at": datetime.now().isoformat()
        })

        chunk_counter += 1

    counter += 1

print("\n🎉 DONE!")
print(f"📌 Interviews processed: {counter}")
print(f"📌 Chunks added to FAISS: {chunk_counter}")
