## Contributing (code) to Ad Simulo

Thanks for contributing to Ad Simulo!

(This guide is work in progress)

* Use GitHub's PRs to send patches.
* Try to mirror the idiom of the surrounding code, even if you don't like it.
* New functionality should have tests. (scripts / examples may be exempt).
* Make sure the tests pass. Locally, this can be done with:

```
PYTHONPATH=. pytest tests
```

* flake8 (configured in `setup.cfg`) is used as a linter. You can run this with:

```
flake8
```

* [Pre-commit](https://github.com/kafkaphoenix/adsimulo/blob/main/.pre-commit-config.yaml)

```
pre-commit install
```
to set up the git hook scripts. Now pre-commit will run automatically on ```git commit```

You can also run the tests with:

```
pre-commit run --all-files
```

* `flake8`, tests and pre-commit hooks will be automatically run as a Github action for PRs and on main.

* Commits should correspond to some logical unit of change. Not too small, not too big.
* Write meaningful commit messages (but there is no grammatical or syntactical pattern that you must follow)
