# Lab 1 - Issue to PR with Copilot coding agent

**Time:** 35 minutes  
**Goal:** Turn an incomplete request into a testable issue, then supervise a coding agent
until it produces a reviewable PR.

## 1. Confirm the starter is healthy

```bash
python scripts/preflight.py
python scripts/validate.py
```

Open `/products` in Swagger UI and inspect the current response.

## 2. Create and improve the issue

Create an issue with the **Lab 1: Product search** template. The initial sentence is
deliberately insufficient. Replace it with a requirement that includes all of the
following:

### Required API behavior

`GET /products` accepts these optional query parameters:

| Parameter | Rules |
|---|---|
| `q` | Case-insensitive partial match against product name or category |
| `sort` | `name` or `price`; invalid values return HTTP 422 |
| `order` | `asc` or `desc`; default `asc`; invalid values return HTTP 422 |
| `page` | Integer >= 1; default 1 |
| `page_size` | Integer from 1 through 20; default 20 |

The response keeps the existing `items`, `total`, `page`, and `page_size` shape.
`total` is the number of matching records before pagination. Search, sorting, and
pagination must work together. Existing `GET /products/{product_id}` behavior must not
change.

### Required validation

```bash
python scripts/validate.py
pytest -q -m lab1
```

Turn the rules into checkable acceptance criteria in the issue.

## 3. Assign the coding agent

1. Assign the issue to Copilot coding agent.
2. Open the agent session log.
3. Check whether its plan mentions input validation, ordering of filter/sort/pagination,
   compatibility, and tests.
4. Do not intervene only because the implementation differs from what you expected.
   Intervene when an acceptance criterion or safety constraint is missed.

## 4. Review the PR

Use this review checklist:

- [ ] Diff is limited to the requested behavior.
- [ ] Query parameters are constrained by FastAPI/Pydantic rather than manual string checks.
- [ ] `total` is calculated before pagination.
- [ ] Existing tests pass.
- [ ] `pytest -q -m lab1` passes.
- [ ] CI detects the product router change and runs the Lab 1 acceptance tests.
- [ ] CI is green.
- [ ] PR summary states assumptions and commands run.

If something is missing, comment with evidence and a concrete expected result, for example:

```text
The acceptance test for combined search + sorting + pagination still fails.
Keep total as the pre-pagination match count and add a regression test before updating the PR.
```

## Debrief

Compare the original one-line issue with the final issue. Identify which added detail most
changed the agent's plan or implementation.

If a rule such as category search is omitted from the issue, expect the matching acceptance
test to fail. Use that failure as evidence to improve the requirement rather than weakening
the test.
