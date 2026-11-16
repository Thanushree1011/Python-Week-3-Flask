# Notepad Tracker

A Flask text editor that saves your file a couple of seconds after you stop
typing and automatically commits every change to Git. Create and edit files in
any folder on your machine and browse each file's commit history.

## Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows  (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
```

Git must be installed and on your PATH.

## Run

```bash
python run.py
```

Open http://127.0.0.1:5000, click **WORKSPACE**, and enter the full path of a
folder (e.g. `C:\Users\you\Notes`).

## How it works

- Typing triggers an auto-save 2 seconds after your last keystroke
  (`AUTO_SAVE_DELAY` in `app/static/js/editor.js`). Ctrl+S saves immediately.
- Each save that changes the file creates one Git commit for that file only.
- If the folder is not inside a Git repository, one is created there. If it is
  already inside a repository, commits go to that repository.
- **History** lists the last 20 commits for the open file.
- If Git has no user configured, commits use the identity
  `Notepad Tracker <notepad@local>`.

## Security note

The app accepts any absolute path and has no login. It listens on
127.0.0.1 only and runs with debug off. Do not expose it to a network.

## Tests

```bash
python -m pytest
```