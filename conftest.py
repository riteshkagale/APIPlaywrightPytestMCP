import pytest
from playwright.sync_api import APIRequestContext, Playwright, sync_playwright


@pytest.fixture
def api_request_context() -> APIRequestContext:
    with sync_playwright() as playwright:  # type: Playwright
        request_context = playwright.request.new_context()
        try:
            yield request_context
        finally:
            request_context.dispose()
