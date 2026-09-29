# API Playwright Pytest MCP

## Objective

This project demonstrates production-style API validation with Python, Pytest,
and Playwright's `APIRequestContext`. It validates the JSONPlaceholder post
endpoint without browser UI automation or Selenium.

## API under test

- Base URL: `https://jsonplaceholder.typicode.com`
- Endpoint: `GET /posts/1`

The test verifies status, JSON content type, object shape, required fields,
field types, expected identifiers, and non-empty text values. It also prints
the response status, relevant headers, and complete JSON body.

## Technology stack

- Python 3
- Pytest
- Playwright for Python API requests

## Prerequisites and installation

Use Python 3.10 or newer.

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

`playwright install` is included for a standard Playwright setup. This API-only
test does not launch a browser, so browser binaries are not required at runtime.

## Project structure

```text
api_playwright_pytest_mcp/
├── tests/
│   ├── __init__.py
│   └── api/
│       ├── __init__.py
│       └── test_post_api.py
├── test_data/
│   ├── __init__.py
│   └── api_test_data.py
├── conftest.py
├── pytest.ini
├── requirements.txt
├── README.md
└── .gitignore
```

## Playwright MCP validation

No Playwright MCP tool/server operation is exposed in the execution
environment for this task, so no MCP action is claimed. The endpoint was
validated directly with Playwright's Python `APIRequestContext`, which is the
same request capability used by the automated test. The observed live
response was:

```json
{
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}
```

The observed status was `200`, and the content type was
`application/json; charset=utf-8`. Relevant response headers included
`cache-control: max-age=43200`.

The intended AI-assisted workflow is: natural-language requirement, endpoint
exploration, response inspection, field identification, test design, code
generation, test execution, failure analysis, fix, and re-run. If an MCP
environment is available, its endpoint inspection should precede the code
generation step; this repository records the limitation rather than
misrepresenting MCP usage.

## APIRequestContext and fixture design

`conftest.py` creates one Playwright `APIRequestContext` per test, yields it,
and disposes it in a `finally` block. Tests therefore use a reusable client
fixture and do not duplicate setup or teardown. `APIRequestContext` sends HTTP
requests directly and does not require browser UI automation.

## Test execution

From the `api_playwright_pytest_mcp` directory:

```powershell
pytest -v
pytest -m api -v
pytest tests/api/test_post_api.py -v
pytest tests/api/test_post_api.py -v -s
```

The `-s` command displays the formatted response logging.

## Expected result and assertions

The API test is expected to pass with status `200`. Assertions provide
meaningful messages for non-200 responses, incorrect content type, invalid JSON
shape, missing fields, incorrect types, unexpected identifiers, and empty
title/body values. A non-200 response is printed before the test fails so the
actual service response is visible.

## Failure troubleshooting

When a failure occurs, first classify it as endpoint availability or network
connectivity, HTTP method, status expectation, JSON parsing, missing field,
unexpected value, wrong type, request-context setup, or assertion logic.
Inspect the printed status/body and response headers before changing the test.
The endpoint is public and may be temporarily unavailable or rate limited.

## Future extensions

The fixture and separated test data support additional tests such as
`test_get_multiple_posts()` and `test_get_post_comments()`. A larger framework
could add environment-based configuration, request helpers, schema validation,
response-time thresholds, retries for explicitly transient failures, CI
reporting, and contract tests while keeping test data and transport setup
reusable.
