# Introduction

Thank you for considering contributing to SpiceyPy!

By following these guidelines you are demonstrating your good intentions and vibes to the maintainers, and you are making the open source community possible.
In return, the maintainers should respond to issues, changes, and pull requests in a similar manner.

We are open to many contributions, in particular bug reports and documentation improvements are examples of helpful contributions that are essential to the growth of the project.
Feature additions are also very welcome, as it is not always possible to accommodate feature requests promptly.

Contributions of feature additions must be consistent with the objectives and intended scope for the project as understood by the project maintainers.
Smaller feature additions are preferred over larger conglomerations as they will be easier to review individually.
In short: *Be excellent to each other* :guitar::guitar::guitar:

# Ground Rules

The most important rule is that communications must be respectful and considerate to all parties. Contributors must respect that
the maintainers are people, and maintainers must also be considerate in return. Users who are new to open source may want to consult [this blog post](https://snarky.ca/why-i-took-october-off-from-oss-volunteering/)
to gain a view of open source volunteering from the maintainers' perspective.

Other Responsibilities
* Keep Contribution Pull Requests (PRs) small and specific; ideal contributions will have 400 or fewer lines with changes.
* Do not Spam with commits! Keep it to 3 or less per day. Each push in a PR sends out multiple emails and github notifications.
* Test your code before making the pull request locally, see the guide below for details on how to test.
* Add tests for new functions, and fix tests that break from your changes (not by commenting them out!).
* Ensure any new code is platform-neutral.
* Create issues for any major changes and enhancements that you wish to make.
* Be welcoming to newcomers and encourage diverse new contributors from all backgrounds. See the [Python Community Code of Conduct](https://www.python.org/psf/codeofconduct/).

# Philosophy

The philosophy of SpiceyPy is to provide a pythonic interface to CSPICE and not much else. Kernel management and higher level OO interfaces are out of scope currently.
SpiceyPy is an alternative for users of ICY and MICE who want to use FOSS, so users should expect some minor differences between the CSPICE and SpiceyPy APIs. These differences in wrapper functions aim to
provide a simpler interaction to CSPICE than would be found in C code. Users should not have to interact directly with the ctypes code underlying SpiceyPy, and
things like parameters for array dimensions should be handled by the wrapper functions as much as possible. Functions should be named directly for the corresponding CSPICE function
without the corresponding underscores or 'c's unless they otherwise shadow another name. Each function should have a brief docstring that outlines the 'what' for function inputs and outputs and a short description.
Links to the corresponding NAIF documentation must be included to give users more detail on the specifics about what the function does and how to use it. The reason for this is that the NAIF documentation is extensive and good.

## Code Style

Code Style is subjective but has been set by the prevailing code style in SpiceyPy and is enforced during code review. If in doubt about style, look at other code in the codebase to see what
decisions have been made elsewhere and try to match that code. Other things include (this may get updated):

* Use `.format` instead of `%` for string formatting; see [https://pyformat.info/](https://pyformat.info/)
* Do not use trailing commas unless making singleton tuples.
* Use spaces between items in lists and dicts (spaces after commas).
* Do not use a newline between the end of function docstrings and the start of function code.
* Do not use huge, deeply-nested list comprehensions.
* Lines may run long, when needed.

# Your First Contribution

Are you unsure where to begin contributing to SpiceyPy? You can start by looking through the current beginner and help-wanted issues. If none are present, then ask in the gitter or `#tools` or `#spice` rooms in the http://openplanetary.co/ slack.
Are you working on your first Pull Request? You can learn how from this *free* series, [How to Contribute to an Open Source Project on GitHub](https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github).
At this point, you're ready to make your changes! Feel free to ask for help; everyone is a beginner at first!
If a maintainer asks you to "rebase" your PR, they're saying that a lot of code has changed, and that you need to update your branch so it's easier to merge.

# How to Test

SpiceyPy uses [pytest](https://docs.pytest.org/en/latest/) for tests. If you are unfamiliar with pytest, then read some of those docs and come back here when done ...
Good, the best way to get started is to look at the existing test code:  tests for wrapper functions are located in `test_wrapper.py` and are good examples to follow for code
style. Tests for SpiceyPy functions are modeled after the corresponding tests in the NAIF documentation. Any state should be cleared at the end of the test (typically via spice.kclear()), and temporary files
should be deleted when finished; see other tests for examples of this.

Once you have written tests, execute them with the command `pytest` and you should see them run. SpiceyPy relies on a number of SPICE kernels that it will download
before some tests fully execute and those files will also be deleted after the tests finish. To allow for rapid development and testing, the deletion of kernels can
be stopped by setting the environment variable `spiceypy_do_not_remove_kernels` to any non-empty string before the test.

# How to submit a pull request

Here is the general process for making a code contribution to SpiceyPy. SpiceyPy is MIT-licensed; as such all contributions must be made with the same license.

1. Create your own fork of the project
2. Make the changes in your fork on a new branch
3. Make a pull request that should be a single commit onto the main branch with a detailed commit message.

Commit messages should start with a title line followed by a newline followed by a markdown-formatted list of changes.

# How to report a bug

### Security

Security is scary and hard to do correctly. If you find an issue please fix it and submit a PR ASAP with an explanation of what happened. Sending PMs to notify the maintainers as soon a you discover a security issue is also apreciated.

### How to file a bug report.

When filing an issue, make sure to answer these five questions:

1. What version of Python are you using (including minor number)?
2. What operating system and processor architecture are you using?
3. What did you do?
4. What did you expect to see?
5. What did you see instead?

### How to suggest a feature or enhancement

Feature requests should be made as issue reports with descriptions.

# Code review process

The core team will review Pull Requests as they are posted and make suggestions in comments on the PR. In general, comments made
by the maintainers should be followed (but can be contested with civil discussions and evidence), and a PR might not be merged if changes suggested by the maintainers are not resolved.
PRs that are inactive after a month or so can be closed, but will be reopened once activity resumes or upon contributor request.

# Community

SpiceyPy has a gitter room with a link in the readme, and the maintainer hangs out on the http://openplanetary.co/ slack.
