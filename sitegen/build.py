from __future__ import annotations
import logging
import re
from datetime import datetime, timezone
from io import TextIOWrapper
from charset_normalizer import from_path
from marko import Markdown, MarkoExtension
from marko.block import Document, Heading
from jinja2 import Environment, Template
from typing import Iterable, Final, Any, TypeAlias, Union
from markupsafe import Markup
from abc import ABC, abstractmethod
from .exec import FileTypeError
from .context import BuildContext, TemplateContext, FileType, Metrics
from .templates import PAGE_FALLBACK

logger = logging.getLogger(__name__)

PAGE_DEFAULT: Final[str] = "# {heading}\n{body}"
PAGE_DEFAULT_BODY: Final[str] = "*Nothing here yet...*"

DEFAULT_EXTENSIONS: Final[frozenset[str]] = frozenset(
    {'footnote', 'toc', 'codehilite', 'gfm'}
)

PageTitle: TypeAlias = Markup
PageBody: TypeAlias = Union[Document, str]


class Page(ABC):
    title: PageTitle
    body: PageBody
    template: Template
    context: BuildContext
    type: FileType
    metadata: dict[str, Any]
    jinja_env: Environment

    def __init__(self) -> None:
        pass

    @abstractmethod
    def parse(self) -> None:
        pass

    def read(self) -> str:
        """
        Prepare source file for reading.
        :return: File object as the built-in `open()` function does.
        :raise FileTypeError: Tried to open a non markdown file.
        :raise IOError: If source file cannot be opened for any reason.
        """
        path = self.context.source_path
        if not (path.suffix.lower() in self.type.value):
            raise FileTypeError("File not a markdown file.", path.suffix)

        charset = from_path(path).best()
        encoding = (charset.encoding if charset else "utf-8")

        try:
            return path.read_text(errors="ignore", encoding=encoding)
        except OSError as e:
            raise IOError(*e.args) from e

    def write(self, page_body: str) -> int:
        """
        Prepare destination file for writing.
        :return: File object as the built-in `open()` function does.
        :raise IOError: If source file cannot be opened for any reason.
        """
        path = self.context.dest_path

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            return path.write_text(page_body, errors="ignore", encoding="utf-8")

        except OSError as e:
            raise IOError(*e.args) from e

class MarkdownPage(Page, Markdown):
    def __init__(self, context: BuildContext):
        super(Page).__init__()
        self.__marko = Markdown(extensions=DEFAULT_EXTENSIONS)
        self.context = context
        self.type = FileType.MARKDOWN

    def parse(self) -> None:
        """
        Parse the body of this page.
        If the body of the source file is empty, will fallback to default content.
        :return: None
        """

        self.body = self.__marko.parse(
            self.read()
        )

        if len(self.body.children) == 0:
            default_heading = self.context.dest_path.stem
            default_body = PAGE_DEFAULT.format(heading=default_heading, body=PAGE_DEFAULT_BODY)
            self.body = self.__marko.parse(default_body)

        self.__extract_title()

    def __extract_title(self) -> None:
        # Set a default before attempting to get actual title
        title = Heading(
            re.match(Heading.pattern, "# Untitled")
        )

        for e in self.body.children:
            if isinstance(e, Heading) and e.level == 1:
                self.body.children.remove(e)  # type: ignore
                self.title = Markup(
                    self.__marko.renderer.render_children(e)
                )

        self.title = Markup(
            self.__marko.renderer.render_children(title)
        )

#    def get_template_context(self) -> TemplateContext:
#        t_c = TemplateContext()
#        with Metrics() as metrics:
#            t_c.modified = self.context.source_path_lastmod
#            t_c.yml = self.metadata
#            t_c.url = self.context.url_path
#            t_c.now = datetime.now(timezone.utc)
#
#            t_c.html = Markup(
#                super().render(self.body)
#            )
#
#            t_c.table_of_contents = Markup(
#                self.renderer.render_toc()
#            )
#
#            t_c.title = Markup(
#                self.renderer.render_children(self.title)
#            )
#
#        t_c.metrics = metrics
#        return t_c
#
#    def render(self, *templates: str | Template, **jinja_context) -> None:
#        """
#        Render this page object to HTML and write it to disk.
#
#        Uses the template `page.html` located in `_fragments` else,
#        will fallback to use `DEFAULT_PAGE_TEMPLATE`. Renders the page
#        using the current object as context.
#
#        :param templates:
#        :param jinja_context: Additional context when rendering.
#        :return: None
#        """
#        self.set_template(*templates, "page.html")
#        template_context = self.get_template_context()
#
#        template_context.metrics["template"] = self.template.name
#        with self.w_open() as f:
#            html = self.template.render(
#                page=template_context, **jinja_context
#            )
#
#            if not self.context.validate_only:
#                f.write(html)
#
#def build(
#        build_context: BuildContext,
#        extensions: Iterable[str | MarkoExtension] | None = None,
#        **jinja_context: Any
#) -> None:
#    """
#    Build a page from a Markdown document.
#
#    If no extensions are provided, the default extension list will be used.
#
#    :param build_context: BuildContext instance.
#    :param extensions: Optional iterable of Marko extension names or
#            extension instances to enable for Markdown parsing.
#    :param jinja_context: Additional context when rendering.
#    :return: None
#    """
#    if not extensions:
#        extensions = DEFAULT_EXTENSIONS
#
#    if build_context.type != FileType.MARKDOWN:
#        print(build_context.type)
#        logger.warning("%s is not a Markdown or HTML file.", build_context.source_path.name)
#        return
#
#    page = Page(build_context, extensions)
#    page.parse(PAGE_DEFAULT_BODY)
#
#    if page.metadata.get("is_draft", False):
#        logger.info("Page %s is draft. Skipping...", build_context.source_path)
#        return
#
#    page.render(**jinja_context)
