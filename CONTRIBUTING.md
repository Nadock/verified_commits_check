# Contributing

When contributing to this repository, please first check the open issues incase some has already suggested a similar change, otherwise open a new issue.

## Setting up a development environment

We use `pipenv` to manage Python dependencies and `make` to automate common tasks. You can setup a `pipenv` environment by running the following:

```bash
$> make setup
```

## Adding new messenger backends

1. Add a method to `src/messenger.py` with the following method signature:

```python
def send_to_X(*, author: str, repo: str, commits: List[dict]):
```

1. Implement the required logic to send to the new messenger backend in that function. Pull any other required configuration from environment vairables.

1. Add unit tests covering your new messenger to `src/messenger_test.py`.

1. Ensure all existing unit tests and other checks pass by running the following commands:

```bash
$> make black-check
$> make pytest
$> make pylint
$> make mypy
```

1. Add any new environment variables to the `action.yml` and update the `README.md` as needed.

1. Open a new pull request and assign yourself, be prepared to make changes if requested.
