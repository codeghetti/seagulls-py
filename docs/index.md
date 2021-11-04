---
title: "Home"
---

# seagulls-py

## Development Environment
These are development environment instructions based on the assumption that you are on an Ubuntu
machine.

Python development environments are complete chaos. Do what ever you want but these steps below will
absolutely work.

## Direnv
[direnv]: <https://direnv.net>
We use [direnv] to automatically define some environment variables and to activate the virtualenv
when you access the code's directory in your terminal. On most Ubuntu versions, you can install it
by running `sudo apt install direnv` and adding the below line to your `~/.bashrc` file:

```bash
eval "$(direnv hook bash)"
```

Then, add this snippet to `~/.config/direnv/direnvrc` in order to add `poetry` support to `direnv`:
```bash
layout_poetry() {
  if [[ ! -f pyproject.toml ]]; then
    log_error 'No pyproject.toml found. Use `poetry new` or `poetry init` to create one first.'
    exit 2
  fi

  # create venv if it doesn't exist
  poetry run true

  export VIRTUAL_ENV=$(poetry env info --path)
  export POETRY_ACTIVE=1
  PATH_add "$VIRTUAL_ENV/bin"
}
```

### Pyenv
[pyenv]: <https://github.com/pyenv/pyenv> "Pyenv"
[pyenv-installer]: <https://github.com/pyenv/pyenv-installer> "Pyenv Installer"
[pyenv-prereqs]: <https://github.com/pyenv/pyenv/wiki/Common-build-problems> "Pyenv Prerequisites"
Use [pyenv] to manage multiple versions of python and to decouple your development
environments from any system python installations. You can use the [pyenv-installer] if you're
comfortable piping scripts into bash from their site!

Make sure you install the [prerequisites] before installing `pyenv` and any `python` version.

```bash
$ curl https://pyenv.run | bash
```

Then make sure to have these in your `.bashrc` file:

```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Reload your terminal session, install `python 2.9.2`, and set it as your default global python:
```bash
$ pyenv install 3.9.2
$ pyenv global 3.9.2
```

You can make which your new python is being used by running `pyenv versions` and `python --version`.

### Poetry
[poetry]: <https://python-poetry.org> "Poetry"
[pipx]: <https://pipxproject.github.io/pipx/> "pipx"
We use [poetry] to manage our python packages because it's shiny, new, and all the cool kids are
doing it. We use [pipx] to install `poetry` because it works for most folks. Make sure to run these
commands from the `python 3.9.2` installation we created above.

```bash
$ pip install pipx
$ pipx install poetry
```

Now you can finally clone this repo, change into the code's directory, and initialize your env:
```bash
$ git clone git@github.com:owl-games/seagulls-py.git
$ cd seagulls-py
$ poetry install
$ direnv allow .
```

If everything has gone as planned, you can run the `seagulls` command and start editing code.

## Attribution

These are some of the open source projects that helped us develop seagulls.py:

- [Kenney: UI Pack](https://www.kenney.nl/assets/ui-pack)
- [pygame](https://www.pygame.org/)
