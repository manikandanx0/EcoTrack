from fastapi import APIRouter, Depends
from firebase_config import db
from auth import verify_token

router = APIRouter()

@router.post("/add-note")
def add_note(note: dict, user=Depends(verify_token)):
    doc_ref = db.collection("notes").document()
    doc_ref.set({
        "user_id": user["uid"],
        "note": note["text"]
    })
    return {"id": doc_ref.id, "status": "created"}

@router.get("/my-notes")
def get_notes(user=Depends(verify_token)):
    notes = db.collection("notes").where("user_id", "==", user["uid"]).stream()
    return [{"id": n.id, **n.to_dict()} for n in notes]
