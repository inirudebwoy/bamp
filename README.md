Bamp
=====
**Pronounciation**

- [**IPA**](https://en.wiktionary.org/wiki/Wiktionary:International_Phonetic_Alphabet): /bæmp/

**Verb**

1. simple past tense and past participle of [bump](https://stackoverflow.com/questions/4181185/what-does-bump-version-stand-for)

What does it do?
=====================
Bamp saves you precious time by bamping version in all configured files, creating
commit and tag (coming this fall) with one simple command.
Bamp follows SemVer when bamping versions, bringing a bit of sanity into this
world of dependencies.

Quick start
==============
Easiest way to explain how to start is with examples of how to use Bamp.
Imagine a developer of a fresh library called *notlob* who has just started and is about
to release his first version. Bamp for *notlob* is configured with location of files
to bamp and the current version to minimise the effort.

* increasing the `minor` part of the version.

    $ bamp minor
    New version: 0.1.0

* increasing the `patch` part of the version.

    $ bamp patch
    New version: 0.1.1

* increasing the `major` part of the version.

    $ bamp major
    New version: 1.0.0

* increasing the `minor` part of the version with git commit.

    $ bamp minor --commit
    New version: 1.1.0

* increasing the `patch` part of the version with git commit and custom message.

    $ bamp patch --commit --message "Bamping!"

Configuration
=================

Configuration of bamp is stored in INI format. First place where bamp checks
for configuration is `bamp.cfg` in the current directory. If `bamp.cfg` can't be located
bamp checks for `bamp` section in `setup.cfg`.

Example `bamp.cfg` config file.

    [bamp]
    version=0.0.1
    files=
        setup.py
        src/__init__.py
    vcs=git
    commit=True
    message=Bamp version: {current_version} -> {new_version}
    tag=False
    allow_dirty=False


All the options can be passed as arguments to `bamp` executable.
