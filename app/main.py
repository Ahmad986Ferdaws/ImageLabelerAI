# app/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app import vision, db
import os
import shutil
import uuid

app = FastAPI()

# Ensure dirs exist
IMAGE_DIR = \"images/\"
os.makedirs(IMAGE_DIR, exist_ok=True)

# Init SQLite DB
db.init_db()

class LabelResponse(BaseModel):
    image_id: str
    labels: list[str]
    description: str

@app.post(\"/upload_image\", response_model=LabelResponse)
async def upload_image(file: UploadFile = File(...)):
    ext = file.filename.split(\".\")[-1].lower()
    if ext not in [\"jpg\", \"jpeg\", \"png\"]:
        raise HTTPException(status_code=400, detail=\"Unsupported file type.\")
    
    image_id = str(uuid.uuid4())[:8]
    image_path = os.path.join(IMAGE_DIR, f\"{image_id}.{ext}\")

    with open(image_path, \"wb\") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run Vision labeling
    labels, description = vision.label_image(image_path)

    # Save to DB
    db.insert_label(image_id, image_path, labels, description)

    return LabelResponse(
        image_id=image_id,
        labels=labels,
        description=description
    )

@app.get(\"/image_labels/{image_id}\")
async def get_labels(image_id: str):
    record = db.get_label(image_id)
    if not record:
        raise HTTPException(status_code=404, detail=\"Image not found.\")
    return {
        \"image_id\": record[0],
        \"image_path\": record[1],
        \"labels\": record[2].split(\",\"),
        \"description\": record[3]
    }

@app.get(\"/all_labels\")
async def all_labels():
    records = db.get_all_labels()
    results = []
    for rec in records:
        results.append({
            \"image_id\": rec[0],
            \"image_path\": rec[1],
            \"labels\": rec[2].split(\",\"),
            \"description\": rec[3]
        })
    return {\"images\": results}
