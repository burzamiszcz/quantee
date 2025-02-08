# README
Note: This task was completed in a hurry due to time constraints. I hope everything will work without any issues. I put in my best effort to ensure the quality of the solution, but I am aware that some parts might be unclear but I will be happy to clarify them if needed. :)

## Prerequisites
This project requires **Docker** and **docker-compose** to be installed on your system.

## Setup Instructions

1. **Create a virtual environment (venv):**
   - In the terminal, navigate to the project folder and create a virtual environment:
     ```bash
     python -m venv venv
     ```

2. **Activate the virtual environment:**
   - **Windows:**
     ```bash
     .\venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

3. **Install the required dependencies:**
   - Install the project dependencies using the `server/requirements.txt` file:
     ```bash
     pip install -r server/requirements.txt
     ```

## Running Tests

Test are covering only the server side, not the client
To run tests, use `pytest` with the following command:

```bash
pytest server/tests.py
```



## Running the Server

To start the server using Docker, run the following command:

```bash
docker-compose up --build --scale client=0
```
The client=0 parameter defines the number of clients to be started.
This has been tested with up to 6 clients.


# API Endpoints Documentation

## 1. Upload File
**Endpoint:** `POST /upload/`  
**Description:** Uploads a file to the server in chunks. Only allowed file types can be uploaded.  

**Allowed File Types:**  
- txt  
- pdf  
- png  
- jpg  
- jpeg  
- gif  
- mp4  
- mkv  

**Request:**  
Form data with a file.

**Response:**  
```json
{
  "filename": "example.jpg",
  "location": "./uploads/example.jpg"
}
```

### Errors:  
- **400 Bad Request:** If the file type is not allowed.  
- **500 Internal Server Error:** If there is an issue saving the file.

---

## 2. List Uploaded Files

**Endpoint:** `GET /files/`  
**Description:** Returns a list of all uploaded files, including their name, size, and location.

### Response:
```json
[
  {
    "name": "example.jpg",
    "size": 102400,
    "location": "./uploads/example.jpg"
  },
  {
    "name": "document.pdf",
    "size": 204800,
    "location": "./uploads/document.pdf"
  }
]
```
