##<a href=#intro>What IS goulash?</a>

What IS goulash?  It's sort of like soup, but more viscous, and as for what is actually inside the truth is that no one really knows.  Likewise for this library.  Random odds and ends, common tools and patterns shared by other projects.

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
