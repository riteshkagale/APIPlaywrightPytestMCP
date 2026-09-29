import json

import pytest
from playwright.sync_api import APIRequestContext

from test_data.api_test_data import (
    BASE_URL,
    EXPECTED_POST_ID,
    EXPECTED_USER_ID,
    POST_ENDPOINT,
)


@pytest.mark.api
def test_get_post_details(api_request_context: APIRequestContext) -> None:
    endpoint = f"{BASE_URL}{POST_ENDPOINT}"
    response = api_request_context.get(endpoint)
    response_body = response.text()

    print("========================================")
    print("API RESPONSE")
    print("========================================")
    print(f"Status Code:\n{response.status}")
    print("\nResponse Headers:")
    for header_name in ("content-type", "cache-control"):
        if header_name in response.headers:
            print(f"{header_name}: {response.headers[header_name]}")

    if response.status != 200:
        print(f"\nResponse Body:\n{response_body}")

    assert response.status == 200, (
        f"Expected status 200 but received {response.status}. "
        f"Response body: {response_body}"
    )

    content_type = response.headers.get("content-type", "")
    assert "application/json" in content_type, (
        f"Expected JSON Content-Type but received '{content_type}'"
    )

    response_data = response.json()
    assert isinstance(response_data, dict), (
        f"Expected response JSON to be an object but received "
        f"{type(response_data).__name__}"
    )

    required_fields = ("id", "title", "body", "userId")
    for field in required_fields:
        assert field in response_data, (
            f"Required field '{field}' is missing from response"
        )

    assert type(response_data["id"]) is int, (
        f"Expected 'id' to be an integer but received "
        f"{type(response_data['id']).__name__}"
    )
    assert type(response_data["userId"]) is int, (
        f"Expected 'userId' to be an integer but received "
        f"{type(response_data['userId']).__name__}"
    )
    assert isinstance(response_data["title"], str), (
        f"Expected 'title' to be a string but received "
        f"{type(response_data['title']).__name__}"
    )
    assert isinstance(response_data["body"], str), (
        f"Expected 'body' to be a string but received "
        f"{type(response_data['body']).__name__}"
    )

    assert response_data["id"] == EXPECTED_POST_ID, (
        f"Expected id {EXPECTED_POST_ID} but received {response_data['id']}"
    )
    assert response_data["userId"] == EXPECTED_USER_ID, (
        f"Expected userId {EXPECTED_USER_ID} but received "
        f"{response_data['userId']}"
    )
    assert response_data["title"].strip(), "Expected 'title' to be non-empty"
    assert response_data["body"].strip(), "Expected 'body' to be non-empty"

    print(f"\nResponse Body:\n{json.dumps(response_data, indent=4)}")
    print("========================================")
