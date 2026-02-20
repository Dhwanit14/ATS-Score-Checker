# 🚀 AI-Powered Resume Matcher (ATS Optimizer)

An intelligent application designed to bridge the gap between job seekers and Applicant Tracking Systems (ATS). This tool uses Large Language Models (LLMs) to provide semantic analysis, rather than simple keyword matching, helping candidates align their resumes with specific Job Descriptions (JD).

🌟 Key Features
- Semantic Analysis: Uses Google Gemini 1.5 Flash to understand the context of your experience and identify critical skill gaps.
- AI-Optimized Summary: Instantly generates a professional 3-sentence summary that naturally incorporates missing keywords to pass ATS filters.
- Support for Multiple Formats: Seamlessly processes both `.pdf` and `.docx` files.
- Real-Time Feedback: Provides a match probability score (0-100%) and actionable recruiter-style advice.
- Responsive Mobile UI: Optimized for use on both desktop and mobile devices via local network hosting.

🛠️ Tech Stack
- Backend: [Python 3.11](https://www.python.org/), [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/)
- AI Engine: [Google Gemini SDK](https://ai.google.dev/)
- Document Processing: [PyMuPDF](https://pymupdf.readthedocs.io/) (PDF) and [python-docx](https://python-docx.readthedocs.io/) (Word)
- Frontend: HTML5, CSS3, [Jinja2 Templates](https://jinja.palletsprojects.com/)

📋 How to Run (Easy Steps)

1. Clone the Repository
```bash
git clone [https://github.com/your-username/jd-matcher-pro.git](https://github.com/your-username/jd-matcher-pro.git)
cd jd-matcher-pro

2. Install Dependencies
Bash
pip install -r requirements.txt

3. Set Up Your API Key
Create a file named .env in the root directory.
Add your Google Gemini API Key:

    GEMINI_API_KEY=your_actual_key_here

4. Launch the Application : terminal
uvicorn app:app --reload
Open your browser and navigate to http://127.0.0.1:8000



🏗️ Architecture
The application follows a modern server-side rendering (SSR) pattern:

User: Uploads a resume and pastes a Job Description.

FastAPI: Extracts text from documents and sends a structured prompt to Gemini.

Gemini AI: Analyzes the data and returns a JSON response.

Jinja2: Renders the result page with the match score and AI-generated summary.

📄 License
This project is open-source and available under the MIT License.