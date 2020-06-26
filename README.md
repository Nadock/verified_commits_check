# Verified Commits Check

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

A GitHub Action to check commits pushed to a repositiory to ensure they are verified (aka signed).

## Setup

Copy the text below into a file in your repository called `.github/workflows/verified_commits_check.yml`, then just commit and push it!

```yaml
# .github/workflows/verified_commits_check.yml
name: Run verified commits check

on: push

jobs:
  verified_commit_check:
    name: Check for unverified commits
    runs-on: ubuntu-latest
    steps:
      - uses: nadock/verified_commits_check@v1
```

You can see this example in action in this repository [here](https://github.com/nadock/verified_commits_check/actions?query=workflow%3A%22An+example+workflow%22).

## Common questions

**What are verified commits?**

Verified commits are commits that have been GPG signed by their author, ensuring they truely do come from a trusted source. GitHub has more details in their documentation [here](https://help.github.com/en/github/authenticating-to-github/managing-commit-signature-verification), including how to setup commit signing if you haven't already.

When you commits are verified, you should see the "Verified" badge on your commits like this:

![An example of the verified commits badge](./img/verified_badge_example.png)

**Why not just use the branch protection rule?**

GitHub provides a branch protection rule to prevent unverified commits from being merged into protected branches. However, you usually get little or no warning you've mistakenly pushed unsiged commits until you try to merge your PR. This action will warn you whenever you push unverified commits, allowing you to notice and fix the issue sooner.

**I wish it sent messages to X...**

Okay technically not a question, but if you want to add support for sending a message to some other service when unverified commits are detected (other than the default failed action email) I welcome pull requests to add support. Please check the [`CONTRIBUTING.md`](https://github.com/Nadock/verified_commits_check/blob/master/CONTRIBUTING.md) file for more detials.
