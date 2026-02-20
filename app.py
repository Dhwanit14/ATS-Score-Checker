import time
import os
import fitz  # PyMuPDF
import docx
import json
import re
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from google import genai

# --- 1. SETUP ---
# PASTE YOUR KEY HERE
API_KEY = "YOUR_GEMINI_KEY" 

# Initialize the client
client = genai.Client(api_key=API_KEY)

app = FastAPI()  # <--- THIS WAS MISSING!
templates = Jinja2Templates(directory="templates")

# --- 2. HELPER FUNCTIONS ---

def read_resume(file: UploadFile) -> str:
    """Reads the uploaded file and returns text."""
    text = ""
    try:
        if file.filename.endswith(".pdf"):
            # Read PDF from memory
            with fitz.open(stream=file.file.read(), filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text()
        elif file.filename.endswith(".docx"):
            # Read DOCX
            doc = docx.Document(file.file)
            for para in doc.paragraphs:
                text += para.text + "\n"
    except Exception as e:
        print(f"Error reading file: {e}")
    return text

def analyze_with_gemini(resume_text: str, jd_text: str):
    """Sends the resume to Google Gemini for scoring AND rewriting."""
    
    # 1. DEFINE THE PROMPT FIRST
    prompt = f"""
    You are an expert AI Recruiter and Resume Writer.
    
    JOB DESCRIPTION:
    {jd_text}
    
    RESUME TEXT:
    {resume_text}
    
    TASK:
    1. Compare the resume to the JD.
    2. Provide a match score (0-100).
    3. List 3-5 missing keywords or skills.
    4. Provide 1 specific sentence of advice to improve the resume.
    5. WRITE A NEW PROFILE SUMMARY: Create a professional 3-sentence summary.
    
    OUTPUT FORMAT:
    Return ONLY raw JSON with these keys: 
    "match_percentage", "missing_keywords", "advice", "profile_summary".
    Do NOT use Markdown.
    """

    # 2. NOW START THE RETRY LOOP
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-flash-latest", 
                contents=prompt
            )
            
            # Robust Parsing
            json_match = re.search(r"\{.*\}", response.text, re.DOTALL)
            
            if json_match:
                clean_json = json_match.group(0)
                return json.loads(clean_json)
                
        except Exception as e:
            # Check for that 503 "High Demand" error we saw earlier
            if "503" in str(e) and attempt < 2:
                print(f"Google is busy, retrying in 2 seconds... (Attempt {attempt+1})")
                time.sleep(2)
                continue
            
            print(f"Gemini API Error: {e}")
            return {
                "match_percentage": 0,
                "missing_keywords": ["Connection Error"],
                "advice": "Check your API Key or try again in a minute.",
                "profile_summary": "N/A"
            }

# --- 3. ROUTES ---

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, jd: str = Form(...), resume: UploadFile = File(...)):
    # Step 1: Read File
    resume_text = read_resume(resume)
    
    # Step 2: Ask AI
    analysis = analyze_with_gemini(resume_text, jd)
    
    # Step 3: Show Result
    return templates.TemplateResponse("result.html", {
        "request": request,
        "score": analysis.get("match_percentage", 0),
        "missing": analysis.get("missing_keywords", []),
        "advice": analysis.get("advice", "No advice generated."),
        "summary": analysis.get("profile_summary", "No summary generated.")  # <--- NEW LINE
    })