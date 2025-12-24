from datetime import datetime
from marko import Markdown
from marko.block import Document

ENABLED_MARKO_EXTENSIONS = frozenset(
    {'footnote', 'toc', 'codehilite', 'gfm'}
)

class Page(Markdown):
    """
    Object representing a single page within the site.
    A subclass of `marko.Markdown`.
    """

    title: str
    body: Document
    last_modified: datetime

    def __init__(self):
        super().__init__(extensions=ENABLED_MARKO_EXTENSIONS)