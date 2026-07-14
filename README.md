# ASUS AI Coding Agent Workshop

A runnable Python + FastAPI workshop repository for practicing an agentic software
development workflow:

```text
Issue -> Copilot coding agent -> Pull request -> CI
      -> CodeQL + Copilot code review -> Agent remediation
      -> Repository instructions + Agent Skill + Hook
```

## Workshop labs

| Lab | Duration | Outcome |
|---|---:|---|
| [Lab 1: Issue to PR](docs/lab-1-agentic-workflow.md) | 35 min | Deliver search, sorting, and pagination through a coding-agent PR |
| [Lab 2: Secure review](docs/lab-2-secure-review.md) | 30 min | Triage CodeQL/review findings and remediate an insecure endpoint |
| [Lab 3: Agent guardrails](docs/lab-3-agent-guardrails.md) | 15 min | Validate repository instructions, a reusable skill, and an agent hook |

Instructor preparation is documented in
[docs/instructor-runbook.md](docs/instructor-runbook.md).

## Local setup

Python 3.10 or newer is required.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/validate.py
uvicorn app.main:app --reload
```

On Windows PowerShell, activate the environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

Open:

- API: <http://127.0.0.1:8000/products>
- Swagger UI: <http://127.0.0.1:8000/docs>
- Health check: <http://127.0.0.1:8000/health>

## Validation commands

```bash
python scripts/validate.py
pytest -q -m lab1
ruff check .
```

The normal test command excludes the intentionally failing Lab 1 acceptance tests.
Run `pytest -q -m lab1` while implementing Lab 1.

## Important workshop setup

- Use the advanced CodeQL workflow already included in this repository. Do not also
  enable CodeQL default setup.
- Coding agent must be enabled for the repository and assigned users.
- GitHub Actions and Copilot code review must be available in the workshop organization.
- No real credentials or production data are used in this repository.

