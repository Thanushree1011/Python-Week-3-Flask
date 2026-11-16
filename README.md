# Python Week 3 – Flask Projects

Two Flask projects built in Week 3. Each has its own folder, README and tests.

| Project | What it is | Tech |
|---|---|---|
| [Notepad Tracker](Notepad_Tracker/) | A web text editor that auto-saves your files and commits every change to Git, with per-file history | Flask, Git, JavaScript |
| [Northwind REST API](Northwind%20REST%20API/) | A REST API for customers, products and orders in the Northwind MySQL database | Flask, SQLAlchemy, MySQL, Pydantic |

## Repository structure

```text
Python-Week-3-Flask/
├── Notepad_Tracker/
└── Northwind REST API/
```

## Getting started

Each project is run on its own. Clone the repo, then open the project's folder and follow the setup steps in its README.

```bash
git clone https://github.com/Thanushree1011/Python-Week-3-Flask.git
cd Python-Week-3-Flask
```

- **Notepad Tracker:** `cd Notepad_Tracker`, then see [its README](Notepad_Tracker/README.md). It needs Python and Git.
- **Northwind REST API:** `cd "Northwind REST API"`, then see [its README](Northwind%20REST%20API/README.md). It needs a running MySQL server with the Northwind database and a `.env` file with your credentials.

## Running the tests

Run the tests from inside each project folder:

```bash
python -m pytest
```
