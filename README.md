# Verified Commits Check

## Todo

- [ ] Write `README.md`
- [x] Add example workflow file
- [x] Test irl
- [x] Add our own workflows to run pylint/pytest/black/mypy on PR
- [ ] Confirm/finalise action name
- [ ] Make repo public

## Badges

<!-- HTML here because we want centre alignment -->
<p align="center">
    <!-- pylint -->
    <a href="https://github.com/nadock/verified_commits_check/actions/?query=workflow%3Apylint">
        <img alt="black" src="https://github.com/Nadock/verified_commits_check/workflows/pylint/badge.svg">
    </a>
    <!-- pytest -->
    <a href="https://github.com/nadock/verified_commits_check/actions/?query=workflow%3Apytest">
        <img alt="black" src="https://github.com/Nadock/verified_commits_check/workflows/pytest/badge.svg">
    </a>
    <!-- mypy -->
    <a href="https://github.com/nadock/verified_commits_check/actions/?query=workflow%3Amypy">
        <img alt="black" src="https://github.com/Nadock/verified_commits_check/workflows/mypy/badge.svg">
    </a>
    <!-- black -->
    <a href="https://github.com/nadock/verified_commits_check/actions/?query=workflow%3Ablack">
        <img alt="black" src="https://github.com/Nadock/verified_commits_check/workflows/black/badge.svg">
    </a>
    <!-- codestyle:black -->
    <a href="https://github.com/psf/black">
        <img alt="black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
    </a>
</p>

## Example workflow

You can see this example in action in this repository [here](https://github.com/nadock/verified_commits_check/actions?query=workflow%3A%22An+example+workflow%22).

```yaml
name: An example workflow


on: push


jobs:
  unverified_commit_check:
    name: Check for unverified commits
    runs-on: ubuntu-latest
    steps:
      - uses: nadock/verified_commits_check@v1
```
