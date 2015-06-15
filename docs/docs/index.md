# <a href=#intro>Introduction to Goulash</a>

What IS goulash?  It's sort of like soup, but more viscous, and as for what is actually inside the truth is that no one really knows.  Likewise for this library.  Random odds and ends, common tools and patterns shared by other projects.

Detailed API is available [here](/api), read on for the highlights.

## <a href=#installation>Installing goulash</a>

Install with ipython:

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

# Commands

### Boilerplate generators

| Command | Description |
|---------|-------------|
| **goulash-boiler --docs** *src_root* | Create documentation boilerplate in directory *src_root* |
| **goulash-boiler --tox** *src_root* | Create tox boilerplate in directory *src_root* |
| **goulash-boiler --fabric** *src_root* | Creates fabric boilerplate in directory *src_root* |
| **goulash-boiler --project** *src_root* | Creates project boilerplate in directory *src_root* |
| **goulash-boiler --python** *src_root* | Create python source project boilerplate in directory *src_root* |

### Documentation helpers

| Command | Description |
|---------|-------------|
| **goulash-docs --boilerplate *doc_root* | Same as **goulash-boiler --docs *doc_root>/..**      |
| **goulash-docs --refresh *doc_root* | Refresh and rebuild documentation in directory *doc_root* |


# Contributing

Pull requests welcome.  You might like to run the tests:

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
