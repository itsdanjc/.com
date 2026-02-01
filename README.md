# itsdanjc.com

## Usage

### Building site
```text
$ sitegen build

options:
  -h, --help            show this help message and exit
  -f, --force           force rebuild of all pages
  -c, --clean           clear the build directory, then build
  -d, --dry-run         run as normal. but don't create build files
  -r, --site-root PATH  location of webroot, if not at the current working directory
  --no-rss              do not update or create rss feed
  --no-sitemap          do not update or create sitemap  
```

### Show site structure
```text
$ sitegen tree

options:
  -h, --help            show this help message and exit
  -i, --reindex         ignore cache and reindex
  -r, --site-root PATH  location of webroot, if not at the current working directory
```
