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
Bamp follows [SemVer](http://semver.org/) when bamping versions, bringing a bit of sanity into this
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
    allow_dirty=False

All the options can be passed as arguments to `bamp` executable. If one would like
to bamp minor part in a file with custom message would do it like this.

    bamp minor --version 2.15.10 --files setup.py --commit --message "Bamping!"

allow_dirty | -a/--allow-dirty
-------------------------------------
Flag indicating if bamp can create a commit in a dirty repository.

    allow_dirty=False

commit | -c/--commit
------------------------
Flag for creating a commit. If set to true bamp will use a default commit message or
use one provided via `-m/--message` argument or taken from the config file.

    commit=True

files | -f/--files
----------------------
List of path files which will be bamped. It is possible to specify more than one path.
`bamp` will check if each of the paths exists before proceeding.

    files=
        setup.py
        src/__init__.py

message | -m/--message
---------------------------
Commit message to be used when bamping. Following variables will be substituted:

* current_version - for the version before bamping
* new_version - for the version after bamping

    message=Bamp version: {current\_version} -> {new\_version}

vcs | -V/--vcs
-----------------
Set version control which is used. Only git is supported at this time.

    vcs=git

version | -v/--version
---------------------------
This allows to set the version number. This number will be seeked in files and
bamped accordingly. Bamp fails if the version can not be located.

    version=0.1.0
