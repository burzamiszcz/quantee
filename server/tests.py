import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import os
from file_upload_service import app, UPLOAD_DIR, ALLOWED_EXTENSIONS  

client = TestClient(app)

# Test for uploading a file with valid extensions
@pytest.mark.parametrize("filename", [
    ("test.txt"),
    ("image.png"),
    ("video.mp4"),
])
def test_upload_file(filename: str) -> None:
    """
    Test for uploading a file with valid extensions. It checks if the 
    file is uploaded successfully and the correct response is returned.
    """
    file_path = Path(f"test_{filename}")
    with open(file_path, "wb") as f:
        f.write(b"dummy content")

    with open(file_path, "rb") as f:
        response = client.post(
            "/upload",
            files={"file": (filename, f)},
        )
    
    os.remove(file_path)

    # Assert successful upload and correct response
    assert response.status_code == 200
    assert "filename" in response.json()
    assert "location" in response.json()

    uploaded_file = Path(response.json()["location"])
    assert uploaded_file.exists()
    assert uploaded_file.name == filename

    uploaded_file.unlink()


# Test for uploading a file with an invalid extension
def test_upload_file_invalid_extension() -> None:
    """
    Test for uploading a file with an invalid extension. It checks 
    if the server rejects the file and returns the correct error message.
    """
    file_path = Path("test_invalid.extension")
    with open(file_path, "wb") as f:
        f.write(b"dummy content")

    with open(file_path, "rb") as f:
        response = client.post(
            "/upload/",
            files={"file": ("test_invalid.extension", f)},
        )

    os.remove(file_path)

    # Assert that the response returns a "File type not allowed" error
    assert response.status_code == 400
    assert response.json() == {"detail": "File type not allowed"}


# Test for listing all uploaded files
def test_list_files() -> None:
    """
    Test for listing all uploaded files. It checks if files are listed 
    correctly and that the response contains the correct file information.
    """
    dummy_files = ["file1.txt", "file2.jpg"]
    for file_name in dummy_files:
        with open(UPLOAD_DIR / file_name, "wb") as f:
            f.write(b"dummy content")

    response = client.get("/files/")
    files = response.json()

    # Assert the list of files is returned correctly
    assert response.status_code == 200
    assert len(files) >= 2

    # Clean up the files after testing
    for file_name in dummy_files:
        (UPLOAD_DIR / file_name).unlink()


# Test for checking the allowed file extensions
@pytest.mark.parametrize("filename", [
    "file1.txt", "file2.pdf", "file3.png", "file4.mp4",
    "file5.mkv", "file6.gif", "file7.jpeg"
])
def test_allowed_extensions(filename: str) -> None:
    """
    Test for ensuring that only allowed file extensions are accepted.
    This checks if the file's extension matches the allowed extensions.
    """
    extension = filename.split(".")[-1]
    assert extension in ALLOWED_EXTENSIONS


# Test for simulating a large file upload (chunking)
def test_large_file_upload() -> None:
    """
    Test for uploading a large file, simulating chunked uploads to ensure
    the server handles large files correctly.
    """
    file_path = Path("test_large_file.mp4")
    with open(file_path, "wb") as f:
        f.write(b"0" * (1000 * 1024 * 1024))  # 1GB dummy data

    with open(file_path, "rb") as f:
        response = client.post(
            "/upload/",
            files={"file": ("test_large_file.mp4", f, "application/mp4")},
        )

    os.remove(file_path)

    # Assert successful upload and correct response
    assert response.status_code == 200
    assert "filename" in response.json()
    assert "location" in response.json()

    uploaded_file = Path(response.json()["location"])
    assert uploaded_file.exists()
    assert uploaded_file.name == "test_large_file.mp4"

    uploaded_file.unlink()
