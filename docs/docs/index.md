##<a href=#intro>What IS goulash?</a>

It's sort of like soup, but more viscous, and as for what is actually inside the truth is that no one really knows.  Like the titular foodstuff, this library is a curated froth.   `Goulash` contains random odds and ends, and stuff that won't stay DRY eventually goes in here after I've rewritten it a few times in different projects.

More specifically, `goulash` contains stuff like command-line [documentation and python-project boilerplate generation](#) and [conspicuously missing utilities from `os` and `fabric` modules](#).  I'll throw in [best-in-class decorator patterns](#) and [common abstract datastructure](#) copy-pasta from stackoverflow if I end up looking it up too often.

Detailed API is available [here](/api), API highlights are [here](#), and command-line utilities are described [here](#).

## <a href=#installation>Installing goulash</a>

Install with pypi:

```shell
   $ pip install goulash
```

Or try the bleeding edge:

```shell
   $ git clone https://github.com/mattvonrocketstein/goulash.git
   $ cd goulash
   $ virtualenv venv
   $ source venv/bin/activate
   $ python setup.py develop
```

# Contributing

Github is [here](https://github.com/mattvonrocketstein/goulash).  Pull requests welcome.  You might also like to run the tests:

```shell
  $ cd goulash
  $ source venv/bin/activate
  $ pip install tox
  $ tox
```

To rebuild the documentation:

```shell
  $ cd goulash
  $ source venv/bin/activate
  $ goulash-docs --refresh
```
