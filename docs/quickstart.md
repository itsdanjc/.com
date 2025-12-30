# Getting Started
This guide you through installing, and building a site.


## Prerequisites
- [Git](https://git-scm.com/)
- [Python (3.10+)](https://python.org)
- Some web server. *(This guide provides examples for nginx or apache)*.


## Installation

The first step is to clone the `composeit` repository to your local machine:

You can clone and install **anywhere on your system**. You should use only one installation to manage any 
number of sites you wish to host.

>   [!IMPORTANT]
>   Avoid installing composeit directly into a directory you plan to use as your webroot. Doing so may 
>   prevent the site from building correctly.

```bash
$ git clone https://github.com/itsdanjc/composeit.git
$ cd composeit
```


Then, setup python:
```bash
$ python -m venv .venv
```
Enter enviroment, and install dependencies:

```bash
$ pip install -r requirements.txt
```

Verify installation:

```bash
$ python -m composeit --version
```

You now have `composeit` up and running!

## Setup a Site

Composeit doesn’t need much configuration to get a site working. Just point it to your content, 
and it will generate the pages for you.

Create the following directories in your webroot:
```bash
$ cd /path/to/your/webroot
$ mkdir _public     # Content files are stored here.
$ mkdir _fragments  # For the HTML templates.
```

Create the first page:
```bash
$ echo "# My Website" > _public/index.md
```

Build for the first time:
```bash
$ /path/to/.venv/python -m composeit build
```

>   [!NOTE]
>   Currently, `composeit` must be run from the virtual environment created during installation.
>   This is temporary and will be fixed in a future release. As a fix, you could
>   create a bash script to handle this automatically:
>
>   ```bash
>   #!/bin/bash
>   # Temporary wrapper to run composeit from its virtual environment
>
>   # Adjust this path to the virtual environment
>   VENV_PATH="/path/to/.venv"
>
>   # Execute composeit using the virtual environment's Python
>   "$VENV_PATH/bin/python" -m composeit "$@"
>   ```
>
>   ```bash
>   $ composeit --version
>   ```

You should see `index.html` in your webroot.

## Configure Your Webserver
### Nginx
Add the following to your nginx config:
``` title="nginx.conf"
server {
    listen       80;
    server_name  example.com;

    location /_fragments {
        return 404; # Restrict access to templates
    }

    location /_public {
        return 404; # Restrict access to content files
    }

    location / {
        root   /path/to/your/webroot;
        index  index.html index.htm; # Optional: default index files
    }
}
```
### Apache
Add the following to your Apache config:
``` title="apache.conf"
<VirtualHost *:80>
    ServerName example.com
    DocumentRoot "/path/to/your/webroot"

    # Restrict access to templates
    <Directory "/path/to/your/webroot/_fragments">
        Require all denied
    </Directory>

    # Restrict access to content files
    <Directory "/path/to/your/webroot/_public">
        Require all denied
    </Directory>

    <Directory "/path/to/your/webroot">
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>

    # Optional: default index files
    DirectoryIndex index.html index.htm
</VirtualHost>
```