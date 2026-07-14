# Lab 2 - CodeQL and Copilot code review

**Time:** 30 minutes  
**Goal:** Create a deliberately vulnerable PR, distinguish tool findings from human
decisions, and direct the coding agent to remediate confirmed problems.

> This lab contains intentionally insecure code for training. Use only this sample repository.

## 1. Prepare an isolated vulnerable branch

Start from a clean, current `main` branch:

```bash
git switch main
git pull
git switch -c lab2-insecure-report
python scripts/prepare_lab2.py
git diff
python scripts/validate.py
```

Commit and push the change, then open a PR to `main`. The script does not commit or push.

The generated endpoint is:

```text
GET /reports/sales?category=Laptop&formula=total
```

## 2. Wait for independent review signals

1. Open the PR **Checks** tab and wait for CodeQL.
2. Open the repository **Security > Code scanning** view if your role permits it.
3. Request a Copilot code review from the PR reviewer menu.
4. Read the code yourself before asking an agent to fix it.

Expected CodeQL targets include user-controlled SQL construction and dynamic code
execution. Code review should also discuss validation, exception handling, stack-trace
disclosure, test coverage, and maintainability. Not every review comment is a CodeQL
finding.

## 3. Triage before remediation

Record each item in the PR description or a comment:

| Finding | Source | Classification | Evidence / decision |
|---|---|---|---|
| Example: SQL injection | CodeQL | Confirmed - must fix | Request input reaches an interpolated SQL query |

Use only these classifications:

- **Confirmed - must fix**
- **Needs human decision**
- **Not applicable / false positive**

## 4. Create the remediation issue

Create an issue from **Lab 2: Security remediation** and link the vulnerable PR. Assign it
to Copilot coding agent or ask the agent to update the existing PR.

Watch for these behaviors:

- It uses SQLite parameter binding rather than filtering unsafe characters.
- It removes dynamic Python execution rather than trying to blacklist expressions.
- It returns a stable public error without a stack trace.
- It adds exploit-focused regression tests.
- It does not disable CodeQL or ignore review comments.

## 5. Verify the remediation

```bash
python scripts/validate.py
```

Also test normal behavior and representative attacks through Swagger UI. Confirm that the
updated CodeQL check and CI are green, then resolve review threads only after verifying the
code.

## Fallback when a hosted feature is unavailable

- If CodeQL is unavailable, inspect the instructor-provided expected findings and continue
  with triage.
- If Copilot code review returns no comments, use Copilot Chat:

```text
Review app/routers/reports.py for exploitable security issues, correctness problems,
error disclosure, and missing regression tests. Cite the affected lines and do not edit yet.
```

Reset an uncommitted Lab 2 preparation with:

```bash
python scripts/prepare_lab2.py --reset
```

