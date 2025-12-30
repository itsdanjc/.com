# About `composeit`

`composeit` is a tool for building static websites from text-based content. It was created for use on [itsdanjc.com](https://itsdanjc.com) and is designed to require very little configuration to get working.

Unlike many static site generators, `composeit` isn’t limited to a single type of content. You can mix things like blog posts and image galleries within the same site, rather than treating them as separate projects.

Templates are selected on a per-page basis instead of globally. This allows each page to define its own structure and features without affecting the rest of the site.

`composeit` can be used to build pages from the following inputs:


| Content in...   | Makes | Description                                                                        |
|-----------------|-------|------------------------------------------------------------------------------------|
| Markdown        | HTML  | Write the page body in Markdown; it is parsed and compiled into HTML.              |
| Markdown + YAML | HTML  | Extend Markdown pages with additional YAML data.                                   |
| HTML            | HTML  | Uses Jinja templates, useful for injecting full HTML snippets into complete pages. |
| YAML            | HTML  | Build pages from structured YAML data, such as populating index or listing pages.  |

A [Python API](./api/) is also available for extending or integrating `composeit` into other tools.


## Example Use-cases

`composeit` is intended for sites that don’t fit neatly into a single category. Common use cases include:

- **Personal websites** that combine static pages, blog-style content, and media galleries.
- **Project or portfolio sites** where different pages require different layouts or templates.
- **Small documentation sites** that need custom index pages or structured listings.
- **Content-driven sites** where pages are generated from structured YAML data rather than written by hand.

These are examples, not limitations - `composeit` can be used for any static site where page-level control is preferred over global configuration.