## Contributing (code) to Ad Simulo

Thanks for contributing to Ad Simulo!

(This guide is work in progress)

* Use GitHub's PRs to send patches.
* Try to mirror the idiom of the surrounding code, even if you don't like it.
* New functionality should have tests. (scripts / examples may be exempt).
* Poetry is used as dependency and package manager
* Make sure the tests pass. Locally, this can be done with:
    ```
    poetry run pytest
    ```
* black (configured in `pyproject.toml`) is used as a formatter. You can run this with:
    ```
    poetry run black .
    ```
* [Pre-commit](https://github.com/kafkaphoenix/adsimulo/blob/main/.pre-commit-config.yaml)
    ```
    poetry run pre-commit install
    ```
    to set up the git hook scripts. Now pre-commit will run automatically on ```git commit```

    You can also run the tests with:
    ```
    poetry run pre-commit run --all-files
    ```
* black, pytest, isort, flake8 and other hooks will be automatically run as a Github action for PRs and on main.
* Commits should correspond to some logical unit of change. Not too small, not too big.
* Write meaningful commit messages (but there is no grammatical or syntactical pattern that you must follow)
