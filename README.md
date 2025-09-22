
Cuely Merged Project
====================

This package merges the Figma-generated React frontend with your Python backend logic (Ollama/Whisper).
Files:
- frontend/  (React + Vite project)
- backend/   (FastAPI backend)

Quickstart (child-friendly, step-by-step)
----------------------------------------

Prerequisites:
1. Install Node.js (v16+). See: https://nodejs.org/
2. Install Python (3.10+).
3. Optionally create a virtual environment for Python.

Run the backend:
1. Open a terminal.
2. Go to the backend folder:
   cd backend
3. Install Python dependencies:
   pip install -r requirements.txt
   (If you don't want Whisper or Ollama, you may remove those lines from requirements.txt)
4. Start the backend:
   uvicorn main:app --reload --port 8000

Run the frontend:
1. Open a new terminal.
2. Go to the frontend folder:
   cd frontend
3. Install Node dependencies:
   npm install
4. Start the dev server:
   npm run dev
   (Vite will usually run on http://localhost:5173)

How it works:
- Speak into the browser (the app uses Web Speech API). When you finish, the browser creates text.
- The browser sends the text to the backend at http://localhost:8000/api/ask
- The backend calls Ollama (gemma:2b by default) and returns the answer.
- The browser shows the AI's answer in the chat area.

If you want server-side transcription (uploading audio files), use /api/transcribe endpoint.

Notes:
- The backend uses the 'ollama' Python package. Make sure Ollama is installed and configured on your machine (ollama daemon), or adjust the backend to call your LLM differently.
- CORS is open for localhost; change in production.

