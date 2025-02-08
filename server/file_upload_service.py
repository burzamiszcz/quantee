from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
from typing import List
import aiofiles

app = FastAPI()

# Directory to store uploaded files
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Allowed file extensions for upload
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "mp4", "mkv"}

# Size of each chunk in bytes (10MB)
CHUNK_SIZE = 10 * 1024 * 1024  # 10MB per chunk

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)) -> dict:
    """
    Handles file uploads in chunks. The file is saved to the server in chunks 
    to allow for large file uploads. Only allowed file types are accepted.

    Args:
        file (UploadFile): The file being uploaded.

    Returns:
        dict: A response containing the filename and location of the uploaded file.

    Raises:
        HTTPException: If the file type is not allowed or there is an error saving the file.
    """
    extension = file.filename.split(".")[-1]
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")

    file_location = UPLOAD_DIR / file.filename

    try:
        async with aiofiles.open(file_location, "wb") as buffer:
            while chunk := await file.read(CHUNK_SIZE):
                await buffer.write(chunk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

    return {"filename": file.filename, "location": str(file_location)}

@app.get("/files/", response_model=List[dict])
def list_files() -> List[dict]:
    """
    Lists all files in the upload directory, including their name, size, 
    and location.

    Returns:
        List[dict]: A list of dictionaries containing file details like name, 
                    size, and locationł
    """
    files = []
    for file_path in UPLOAD_DIR.iterdir():
        files.append({
            "name": file_path.name,
            "size": file_path.stat().st_size,
            "location": str(file_path)
        })
    return files
