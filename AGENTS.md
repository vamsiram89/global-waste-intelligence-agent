# AGENTS.md

## Project Mission

Global Waste Intelligence Agent predicts inventory, food, plastic, and production waste before it happens, then recommends prevention actions that are explainable and safe for an MVP demo.

## Development Guidelines

- Keep the MVP modular and beginner-friendly.
- Prefer explainable rules over opaque AI for the first version.
- Use environment variables for configuration and secrets.
- Never recommend donating expired food.
- All redistribution actions require human approval in this MVP.
- Keep API schemas stable and documented.
- Add tests whenever logic changes.

## Local Commands

```powershell
pip install -r requirements.txt
python -m backend.seed_data
uvicorn backend.main:app --reload --port 8000
streamlit run frontend/streamlit_app.py
pytest
```

