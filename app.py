import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import tempfile

# Load environment variables
load_dotenv()

# Import agent modules
from services.agent import ResumeReviewCrew
from services.extract_resume_data import extract_text_from_resume

# Initialize FastAPI app
app = FastAPI(
    title="Resume Review Agent API",
    description="API for reviewing resumes and finding relevant job opportunities",
    version="1.0.0"
)

# Pydantic models for request/response
class ResumeTextInput(BaseModel):
    resume_text: str
    location: str = "India"

class ResumeReviewResponse(BaseModel):
    status: str
    feedback: str
    improved_resume: str
    job_opportunities: str

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Resume Review Agent API is running"}

@app.post("/review-resume/text")
async def review_resume_text(input_data: ResumeTextInput):
    """
    Review a resume provided as text.
    
    Args:
        input_data: Contains resume_text and location
        
    Returns:
        JSON response with feedback, improved resume, and job opportunities
    """
    try:
        crew = ResumeReviewCrew()
        result = crew.kickoff(inputs={
            "resume": input_data.resume_text,
            "location": input_data.location
        })
        
        # Extract output from result
        output_text = result.output.raw if hasattr(result.output, 'raw') else str(result.output)
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Resume review completed successfully",
                "output": output_text,
                "location": input_data.location
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Error processing resume: {str(e)}"
            }
        )

@app.post("/review-resume/file")
async def review_resume_file(file: UploadFile = File(...), location: str = Form("India")):
    """
    Review a resume provided as a PDF file.
    
    Args:
        file: PDF resume file
        location: Job location preference
        
    Returns:
        JSON response with feedback, improved resume, and job opportunities
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            contents = await file.read()
            temp_file.write(contents)
            temp_file_path = temp_file.name
        
        try:
            # Extract text from PDF
            resume_text = extract_text_from_resume(temp_file_path)
            
            # Create crew and process resume
            crew = ResumeReviewCrew()
            result = crew.kickoff(inputs={
                "resume": resume_text,
                "location": location
            })
            
            # Extract output from result
            output_text = result.output.raw if hasattr(result.output, 'raw') else str(result.output)
            
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": "Resume review completed successfully",
                    "filename": file.filename,
                    "output": output_text,
                    "location": location
                }
            )
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Error processing resume file: {str(e)}"
            }
        )

@app.get("/")
async def root():
    """Root endpoint with API documentation"""
    return {
        "application": "Resume Review Agent API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "review_text": {
                "path": "/review-resume/text",
                "method": "POST",
                "description": "Review a resume provided as text"
            },
            "review_file": {
                "path": "/review-resume/file",
                "method": "POST",
                "description": "Review a resume provided as a PDF file"
            },
            "docs": "/docs",
            "swagger_ui": "/docs",
            "openapi_schema": "/openapi.json"
        }
    }

if __name__ == "__main__":
    try:
        import uvicorn
        print("Starting Resume Review Agent API on http://0.0.0.0:8000")
        print("API docs available at http://localhost:8000/docs")
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=8000,
            reload=True
        )
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
