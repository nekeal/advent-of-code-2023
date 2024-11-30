# ⭐ Advent of Code - Python ⭐

[![GitHub](https://img.shields.io/github/license/nekeal/advent-of-code-python-cli.svg)](https://github.com//nekeal/advent-of-code-python-cli/blob/master/LICENSE)
![GitHub Workflow Status](https://github.com/github/docs/actions/workflows/test.yml/badge.svg)
---
**Source Code**: [https://github.com/nekeal/advent-of-code-python-cli](https://github.com/nekeal/advent-of-code-python-cli)

---

## Installation

This project comes as a standalone python package with a CLI tool to help you with boilerplate code and basic tasks.
Recommended way to use it is via pipx or uvx:

```sh
pipx run --spec aoc-python-cli aoccli
```
or
```sh
uvx --from aoc-python-cli aoccli
```

Alternatively, you can install it with pip in the same virtualenv as you are using for your solutions:

```sh
pip install aoc-python-cli
```

## Use this project as a template

In the master branch I will keep the template with sample day 0 solution.
Therefore, I strongly recommend to use this branch as a template for your own solutions by
forking this repository or working with a copy of it.

## Usage

This template comes with a CLI tool powered by [Typer](https://github.com/tiangolo/typer) to help you with boilerplate
code and basic tasks like creating a directory for a new day, running tests, etc.

> [!NOTE]
> To use the CLI tool you need to install requirements. For details see [Development](#development) section.

### Starting solution for a new day

```sh
aoc new-day <day>
```
It will create a `aoc_solutions/<year>/day_<day>` directory with a `__init__.py` and a `test_solution.py` python files.
It will also create text files for both test and real data in the `data/` directory.

You can specify custom data and solutions directories with `---data-directory` and `--directory` flags.
```sh
aoccli new-day --data-directory input_data -d advent_solutions 1
```
This command will create the following directory structure relatively to the current working directory:
```
input_data
└── <current_year>
    ├── 01_input.txt
    └── 01_test_input.txt
aoc_solutions
└── <current_year>
    └── day_05
        ├── __init__.py
        └── test_solution.py
```

> [!NOTE]
> Alternatively you can provide a path to template directory `aoc new-day <day> -t /path/to/template/directory` that will be copied to the new day directory.
> This can be useful if you already have a template for your solutions. However, by using this option you will
> lose the ability to run, verify, and submit a challenge from the CLI tool.


#### NEW! Downloading input data

Now this template uses [advent-of-code-data](https://github.com/wimglenn/advent-of-code-data) package to download
your personal input data. To use it you need to set `AOC_SESSION` environment variable to your session cookie value.
You can find it in your [browser's dev tools](https://github.com/wimglenn/advent-of-code-wim/issues/1)
after logging in to the Advent of Code website.

### Implementing a solution for a day

`BaseChallenge` class is provided to help you with the boilerplate code. By default, each day's solution inherits
from this class. You need to implement the `part1` and `part2` methods, and they should return the correct answer for
each part.

### Running solution and checking the answer

This will usually be used for debugging purposes.

```sh
$ aoc run 0
Using data from 00_input.txt
Day 0 - Part 1: 1
Day 0 - Part 2: 55
```

This command will run the solution for the given day using `data/<year>/00_input.txt` file and print the answers
for both parts.

If you want to see the result only for the test data, you can use the `-t/--test-data` flag.
```sh
$ aoc run <day> -t
Using data from 00_test_input.txt
Day 0 - Part 1: 1
Day 0 - Part 2: 10
```

Alternatively you can also specify the path to the input file instead of using the default one.

```sh
$ aoc run 0 -f custom_input.txt
Using data from custom_input.txt                                                                                                        hello, nekeal ⭐
Day 0 - Part 1: 1
Using data from custom_input.txt
Day 0 - Part 2: 33
```
### Verifying solution

You can verify your solution by running [pytest](https://github.com/pytest-dev/pytest) tests.
There is a generic test case for each day that checks both parts of a solution against the correct answer.
To use it you need to configure correct answers on the test class for a given day.
command will run the solution for the given day using `data/00_input.txt` file and print the answers
for both parts.
```python
class TestChallenge(BaseTestChallenge):
    challenge_class = Challenge
    expected_results_from_test_data = ("Expected result for part 1", "Expected result for part 2")
    expected_results_from_real_data = ("Expected result for part 1", "Expected result for part 2")
```

Then you can run the tests for a given day with:
```sh
aoc verify <day>
```
To test only part 1 or part 2, you can use the `-1/-2` flag.
```sh
aoc verify <day> -1
```

To test only for sample data, you can use the `-t/--test-data-only` flag.
```sh
aoc verify <day> -t
```

To check for a regression (😉) you can run all tests at once:
```sh
aoc verify
```

### Running tests after each change

If you don't like the idea of running tests manually, there is a pre-installed [pytest-watcher](https://github.com/olzhasar/pytest-watcher)
package that will run tests for you after each change in the code.

```sh
ptw aoc_solutions
```

### Submitting solution

Thanks to [advent-of-code-data](https://github.com/wimglenn/advent-of-code-wim/issues/1) package, you can submit your
solution directly from the command line.

```sh
aoc submit <day> <part>
```

Under the hood, it will run the solution for the given day and part,
and submit the answer to the Advent of Code website.

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.11+
* Create a virtual environment and install dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Testing

```sh
aoc verify
```

### Pre-commit

Pre-commit hooks run all the auto-formatting (`ruff format`), linters (e.g. `ruff` and `mypy`), and other quality
 checks to make sure the changeset is in good shape before a commit/push happens.

You can install hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want to run all checks manually for all files:

```sh
pre-commit run --all-files
```

---

This project was generated using the [cookiecutter-python-package](https://github.com/nekeal/cookiecutter-python-package) template.
