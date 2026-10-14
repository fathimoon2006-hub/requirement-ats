from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "ATS Backend Running!"}

@app.post("/analyze/")
async def analyze_resume(file: UploadFile = File(...), job_description: str = ""):
    text = ""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(await file.read()))
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    
    # Simple ATS Score Logic
    keywords = ["python", "java", "sql", "machine learning", "react", "html", "css", "javascript"]
    score = 0
    matched = []
    text_lower = text.lower()
    for kw in keywords:
        if kw in text_lower or kw in job_description.lower():
            if kw in text_lower:
                matched.append(kw)
                score += 10
    
    score = min(score + 40, 95) # base score
    
    return {
        "score": score,
        "matched_keywords": matched,
        "total_words": len(text.split()),
        "resume_text_preview": text[:500]
    }
