from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import tempfile
from pathlib import Path
import sys

sys.path.append("src")

from parser import ResumeParser


app = FastAPI(
    title="Automated Resume Analyzer API",
    description="Upload a PDF/DOCX resume and get structured JSON output.",
    version="1.0"
)

parser = ResumeParser()


@app.get("/")
def home():
    return {
        "message": "Automated Resume Analyzer API is running",
        "docs": "Go to /docs to test the API"
    }


@app.post("/parse-resume/")
async def parse_resume(file: UploadFile = File(...)):
    try:
        file_extension = Path(file.filename).suffix.lower()

        if file_extension not in [".pdf", ".docx"]:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Invalid file format. Please upload PDF or DOCX."
                }
            )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file_extension
        ) as temp_file:
            temp_file.write(await file.read())
            temp_path = temp_file.name

        parsed_data, cleaned_text = parser.parse_file(temp_path)

        return {
            "status": "success",
            "file_name": file.filename,
            "parsed_resume": parsed_data
        }

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(error)
            }
        )