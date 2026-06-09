# Resume Review Agent

A simple AI app that reviews resumes and gives suggestions.

## What it does
- Reviews a resume
- Gives feedback and score
- Suggests improvements
- Finds relevant job openings

## Setup
1. Create a virtual environment
   ```bash
   python -m venv .resumereviewenv
   .\.resumereviewenv\Scripts\activate
   ```
2. Install packages
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with:
   ```env
   API_KEY=your_openai_key
   MODEL=gpt-4
   SERPER_API_KEY=your_serper_key
   ```

## Run the app
```bash
python app.py
```

Open:
- http://localhost:8000/docs

## API example
### Text resume
```bash
curl -X POST "http://localhost:8000/review-resume/text" \
  -H "Content-Type: application/json" \
  -d '{"resume_text":"Your resume text here","location":"New Delhi"}'
```

### PDF resume
```bash
curl -X POST "http://localhost:8000/review-resume/file" \
  -F "file=@resume.pdf" \
  -F "location=New Delhi"
```

## Notes
- Use `.env` for secrets
- Do not commit `.env` to Git
