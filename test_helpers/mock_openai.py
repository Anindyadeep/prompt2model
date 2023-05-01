"""Tools for mocking OpenAI API responses (for testing purposes)."""

import json


class MockCompletion:
    """Mock openai completion object."""

    def __init__(self, content: str):
        """Initialize a new instance of `MockCompletion` class.

        Args:
            content: The mocked content to be returned, i.e.,
            `json.dumps({"comment": "This is a great movie!",
            "label": 1})`.
        """
        self.choices = [{"message": {"content": content}}]

    def __repr__(self):
        """Return a string representation of the `MockCompletion` object.

        Returns:
            _string: A string representation of the object, including its choices.
        """
        _string = f"<MockObject choices={self.choices}>"
        return _string


def mock_openai_response(prompt: str, content: dict) -> MockCompletion:
    """Generate a mock completion object containing a choice with example content.

    This function creates a `MockCompletion` object with a `content` attribute set to
    a JSON string representing an example label and comment. The `MockCompletion`
    object is then returned.

    Args:
        prompt: A mocked prompt that won't be used.
        content: The example content to be returned.

    Returns:
        a `MockCompletion` object.
    """
    _ = prompt
    example_content = json.dumps(content)
    mock_completion = MockCompletion(content=example_content)
    return mock_completion