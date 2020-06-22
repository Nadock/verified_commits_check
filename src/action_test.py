import pytest

from . import action


@pytest.mark.parametrize(
    "path, content", [("../events/unit_test_0.json", {"test": True})]
)
def test_load_event(path, content):
    result = action.load_event(path)
    assert result == content
