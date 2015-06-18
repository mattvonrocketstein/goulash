##<a href=#intro>What IS goulash?</a>

What IS goulash?  It's sort of like soup, but more viscous, and as for what is actually inside the truth is that no one really knows.  Likewise for this library: it contains random odds and ends, common tools and patterns shared by other projects.  More specifically there's a lot of library and command-line helpers forthings like:

  * documentation and python-project boilerplate generation,
  * conspicuously missing utilities from the `os` and `fabric` libraries
  * common decorator patterns nicked from places like stackoverflow
  * tools for project management, and lots of other misc. stuff

Detailed API is available [here](/api), read on for the highlights.

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
