# Verified Commits Alert

## Todo

- [ ] Write `README.md`
- [x] Add example workflow file
- [x] Test irl
- [x] Add our own workflows to run pylint/pytest/black/mypy on PR
- [ ] Confirm/finalise action name
- [ ] Make repo public

## Badges

<p align="center">
    [![pylint](https://github.com/Nadock/verified_commits_alert/workflows/pylint/badge.svg)](https://github.com/nadock/verified_commits_alert/actions/?query=workflow%3Apylint)
    [![pytest](https://github.com/Nadock/verified_commits_alert/workflows/pytest/badge.svg)](https://github.com/nadock/verified_commits_alert/actions/?query=workflow%3Apytest)
    [![mypy](https://github.com/Nadock/verified_commits_alert/workflows/mypy/badge.svg)](https://github.com/nadock/verified_commits_alert/actions/?query=workflow%3Amypy)
    [![black](https://github.com/Nadock/verified_commits_alert/workflows/black/badge.svg)](https://github.com/nadock/verified_commits_alert/actions/?query=workflow%3Ablack)
    [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
</p>

## Example workflow

You can see this example in action in this repository [here](https://github.com/nadock/verified_commits_alert/actions?query=workflow%3A%22An+example+workflow%22).

```yaml
name: An example workflow


on: push


jobs:
  unverified_commit_check:
    name: Check for unverified commits
    runs-on: ubuntu-latest
    steps:
      - uses: nadock/verified_commits_alert@v1
```
