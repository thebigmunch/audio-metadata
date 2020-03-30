## Forward

Due to general and personal experience, I feel compelled to
preface this with a short, pointed statement.

Developers, maintainers, and others usually contribute to open source software
in spare time from full lives. **We owe you nothing.**
Check your attitude and entitlement at the virtual door; they won't be tolerated.

For a longer, softer version of that message, check out [Brett Cannon's](https://snarky.ca)
*Setting expectations for open source participation* talk
([video](https://youtu.be/tzFWz5fiVKU?t=48m55s), [text](https://snarky.ca/setting-expectations-for-open-source-participation/)).

See the [Code of Conduct](https://github.com/thebigmunch/audio-metadata/blob/master/.github/CODE_OF_CONDUCT.md)
for behavioral expectations.


## In what ways can I contribute?

* Post in the [Development](https://forum.thebigmunch.me/c/dev/) category on the [Discourse forum](https://forum.thebigmunch.me/).
* Browse and comment on [issues](https://github.com/thebigmunch/audio-metadata/issues) or [pull requests](https://github.com/thebigmunch/audio-metadata/pulls).
* [Open an issue](https://github.com/thebigmunch/audio-metadata/issues/new) with a bug report or feature request.
* See current [projects](https://github.com/thebigmunch/audio-metadata/projects).
* Contact me by email at mail@thebigmunch.me.


## How do go about contributing?

### Submitting an issue

Bug reports and feature requests can be submitted to the
[Issue Tracker](https://github.com/thebigmunch/audio-metadata/issues).
For discussion and support, use the [Discourse forum](https://forum.thebigmunch.me).

Some general guidelines to follow:

* Use an appropriate, descriptive title.
* Provide as many details as possible.
* Don't piggy-back; keep separate topics in separate issues.

### Submitting code

An issue should be opened for discussion prior to making a Pull Request for most changes.

Keep your code consistent with the rest of the project.

* Tabs should be used for indentation of code.
* Don't use line continuation that aligns with opening delimiter.
* Readability and understandibility are more important than arbitrary rules.

[Pull Requests](https://help.github.com/articles/creating-a-pull-request) should originate from a
[feature branch][fb] in your [fork][fork], not from the **master** branch.

Commit messages should be written in a
[well-formed, consistent](https://sethrobertson.github.io/GitBestPractices/#usemsg) manner.
If the commit is linked to an issue, add a reference to that issue at the end of the commit message
in the form of ``[#00]``.
See the [commit log](https://github.com/thebigmunch/audio-metadata/commits) for acceptable examples.

Each commit should encompass the smallest logical changeset.
E.g. changing two unrelated things in the same file would be two commits rather than one commit of "Change filename".

If you need to make a change to your Pull Request, you should
[amend or rebase](https://www.atlassian.com/git/tutorials/rewriting-history) to change your previous commit(s)
then [force push](http://stackoverflow.com/a/12610763) to the [feature branch][fb] in your [fork][fork].

[fb]: https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/#creating-a-branch
[fork]: https://help.github.com/articles/fork-a-repo

## Misc
For anything else, contact the author by e-mail at <mail@thebigmunch.me>.
