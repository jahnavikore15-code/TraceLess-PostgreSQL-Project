# TraceLess – Digital Footprint Tracker

A beginner-friendly web application to manually register online accounts, review inactive accounts, and maintain a privacy checklist.

## Technology
- Python + Flask
- PostgreSQL
- HTML, CSS, JavaScript
- pgAdmin 4

## Setup (Windows / VS Code)

1. Install Python, PostgreSQL and pgAdmin 4.
2. Open this folder in VS Code.
3. Open the VS Code terminal (`Terminal > New Terminal`).
4. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and activate again.

5. Install packages:

   ```powershell
   pip install -r requirements.txt
   ```

6. In pgAdmin, connect to your PostgreSQL server. Right-click **Databases > Create > Database**, name it `traceless_db`, and save.
7. Copy `.env.example` to a new file named `.env`. Put your PostgreSQL password in `DB_PASSWORD`. Do not share `.env` or upload it to GitHub.
8. Run the application:

   ```powershell
   python app.py
   ```

9. Open http://127.0.0.1:5000 and register an account. The app creates its tables automatically on first run.

## Notes
- The app stores account labels/usernames that you enter; never enter actual passwords.
- The inactivity indicator uses a 90-day threshold.
- The Footprint Health Score is an illustrative organization score, not a cybersecurity audit or measurement of actual exposure.
- For a public deployment, set a strong random `SECRET_KEY`, use HTTPS, and configure a managed PostgreSQL database.
