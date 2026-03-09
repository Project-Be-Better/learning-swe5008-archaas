# Agentic AI + LangGraph Workspace

This repository is set up as a Python starter workspace for building agentic AI apps with LangGraph.

## 1) Create and Activate a Virtual Environment (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If script execution is blocked, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## 2) Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3) Configure Environment Variables

Create a `.env` file from `.env.example` and set your key:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

## 4) Run the Agent

```powershell
python -m agentic_workspace.main
```

## Project Structure

```text
.
|-- .env.example
|-- pyproject.toml
|-- requirements.txt
`-- src/
	`-- agentic_workspace/
		|-- __init__.py
		`-- main.py
```

## What the Starter Includes

- LangGraph state machine wiring (`START -> agent -> tools -> agent -> END`)
- A sample tool (`add`) so you can test tool-calling behavior
- `.env`-based runtime configuration for model/provider settings

## Optional Dev Tools

```powershell
pip install -e .[dev]
ruff check .
```
