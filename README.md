<div align="center">
  <h1>pre-commit-hooks</h1>

  <br />
  <a href="https://github.com/Payadel/pre-commit-hooks/issues/new?assignees=&labels=bug&template=BUG_REPORT.md&title=bug%3A+">Report a Bug</a>
  ·
  <a href="https://github.com/Payadel/pre-commit-hooks/issues/new?assignees=&labels=enhancement&template=FEATURE_REQUEST.md&title=feat%3A+">Request a Feature</a>
  .
  <a href="https://github.com/Payadel/pre-commit-hooks/issues/new?assignees=&labels=question&template=SUPPORT_QUESTION.md&title=support%3A+">Ask a Question</a>
</div>

<div align="center">
<br />

[![code with love by Payadel](https://img.shields.io/badge/%3C%2F%3E%20with%20%E2%99%A5%20by-Payadel-ff1414.svg?style=flat-square)](https://github.com/Payadel)

![Build Status](https://github.com/payadel/pre-commit-hooks/actions/workflows/build.yaml/badge.svg?branch=dev)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/payadel/pre-commit-hooks)

![GitHub](https://img.shields.io/github/license/Payadel/pre-commit-hooks)
[![Pull Requests welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg?style=flat-square)](https://github.com/Payadel/pre-commit-hooks/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22)

</div>

This project provides **Git hooks** for the [pre-commit](https://pre-commit.com/) framework. This project has several
hooks,
each of which is explained below.

## Prerequisites

Install pre-commit base this guide: [pre-commit installation guide](https://pre-commit.com/#install)

## Hook: run_scripts

### About

#### Summary

`run_scripts` allows you to execute a set of related scripts with a title and a
condition. This hook receives a list of files and folders in its parameter and collects the set of scripts from the
folders. Then, it executes them and makes sure that all the scripts complete successfully. If a script encounters an
error and exits with a non-zero code, the hook displays the details of the error. This hook is reliable and designed
specifically for this purpose.

#### Explain

**Question:** What should you do if you have one or more related scripts that you want to run with a specific title and
condition?

Basic solution: You could create a script file and place each script inside it. However, this approach may require
manually adding scripts from different folders or writing a script to gather all the files in a folder before executing
them. Additionally, controlling the outputs can be challenging. While this approach is viable, it can be troublesome,
error-prone, lacks specific versioning, and isn't easy to manage across different projects.

**Better solution:** Use this hook. It takes a list of files and folders as parameters, collects the set of scripts from
the specified folders, and executes them, ensuring that all scripts run successfully. If a script encounters an error
and exits with a non-zero code, the hook displays the error details. It is a thoroughly tested, reliable, and
purpose-built solution.

#### Built With

`run_scripts` hook is compatible with Python 3.8 and later versions.

### Getting Started

#### Usage

To use `run_scripts` hook in your project, you need to:

1. Install [pre-commit](https://pre-commit.com/) framework on your system. You can do this by
   running `pip install pre-commit`.
2. Add the following code to your `.pre-commit-config.yaml` file:

```yaml
- repo: https://github.com/Payadel/pre-commit-hooks
  rev: v0.1.5  # Ensure it is latest
  hooks:
    - id: run_scripts
      args: [ '-f=path/to/file', '-d=path/to/directory' ]
      stages: [ push ]
      pass_filenames: false

```

3. Run `pre-commit install` to install the hook.

### Features

- Allows you to execute related scripts with a title and a condition
- Collects scripts from folders and executes them
- Makes sure all scripts complete successfully
- Displays details of any errors encountered during execution

## Hook: document oriented

### About

#### Summary

Before each push, `document-oriented` makes sure that if the source has changed, at least one document file has been
updated, otherwise it stops the push and reminds that the document needs to be updated as well. You can specify the
pattern of sources and
documents for this hook.

### Explain

Documentation is a crucial component of any project. To ensure that your project is visible, used, and has contributors,
it must have a comprehensive and up-to-date documentation. It is essential to update the relevant documents after making
changes to the code without delay.

While most developers understand the significance of documentation, they may occasionally forget or procrastinate
updating it. This issue is particularly prevalent in projects with multiple active programmers that are developed over
an extended period.

To help you tackle this problem, this hook can be used. If your documents are in your code repository, you can specify
the pattern of sources and documents using this hook. Before each push, this hook checks all the commits that are going
to be pushed. If the source has been modified, it ensures that at least one document has been updated; otherwise, it
halts the push operation and reminds you to update the relevant documents.

#### Built With

`document_oriented` hook is compatible with Python 3.8 and later versions.

### Getting Started

#### Usage

To use `document_oriented` hook in your project, you need to:

1. Install [pre-commit](https://pre-commit.com/) framework on your system. You can do this by
   running `pip install pre-commit`.
2. Add the following code to your `.pre-commit-config.yaml` file:

```
- repo: https://github.com/Payadel/pre-commit-hooks
  rev: v0.1.5  # Ensure it is latest
  hooks:
    - id: document-oriented
      args: ['--doc=*.md', '--source=src/*']
```

3. Run `pre-commit install` to install the hook.

### Features

- Ensures that project documentation is up-to-date
- Can specify the pattern of sources and documents

#### FAQ

##### Q: What if I want to skip the document update check for certain commits?

A: You can skip the document update check for certain commits by adding the `SKIP=document-oriented` flag to
your `git commit` command. For example:

```
SKIP=document-oriented git commit -m "Commit message"
```

## CHANGELOG

Please see the [CHANGELOG.md](CHANGELOG.md) file.

## Roadmap

See the [open issues](https://github.com/Payadel/pre-commit-hooks/issues) for a list of proposed features (and known
issues).

- [Top Feature Requests](https://github.com/Payadel/pre-commit-hooks/issues?q=label%3Aenhancement+is%3Aopen+sort%3Areactions-%2B1-desc) (
  Add your votes using the 👍 reaction)
- [Top Bugs](https://github.com/Payadel/pre-commit-hooks/issues?q=is%3Aissue+is%3Aopen+label%3Abug+sort%3Areactions-%2B1-desc) (
  Add your votes using the 👍 reaction)
- [Newest Bugs](https://github.com/Payadel/pre-commit-hooks/issues?q=is%3Aopen+is%3Aissue+label%3Abug)

## Support

Reach out to the maintainer at one of the following places:

- [GitHub issues](https://github.com/Payadel/pre-commit-hooks/issues/new?assignees=&labels=question&template=04_SUPPORT_QUESTION.md&title=support%3A+)

## Project assistance

If you want to say **thank you** or/and support active development of this project:

- Add a [GitHub Star](https://github.com/Payadel/pre-commit-hooks) to the project.
- Tweet about the project.
- Write interesting articles about the project on [Dev.to](https://dev.to/), [Medium](https://medium.com/) or your
  personal blog.

Together, we can make this project **better**!

## Contributing

First off, thanks for taking the time to contribute! Contributions are what make the free/open-source community such an
amazing place to learn, inspire, and create. Any contributions you make will benefit everybody else and are **greatly
appreciated**.

Please read [our contribution guidelines](docs/CONTRIBUTING.md), and thank you for being involved!

## Authors & contributors

The original setup of this repository is by [Payadel](https://github.com/Payadel).

For a full list of all authors and contributors,
see [the contributors page](https://github.com/Payadel/pre-commit-hooks/contributors).

## Security

This project follows good practices of security, but 100% security cannot be assured. this project is provided **"as
is"** without any **warranty**.

_For more information and to report security issues, please refer to our [security documentation](docs/SECURITY.md)._

## License

This project is licensed under the **GPLv3**.

See [LICENSE](LICENSE) for more information.

## Related

- [pre-commit](https://pre-commit.com)
