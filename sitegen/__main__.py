import os
import argparse
import logging
import time
from pathlib import Path
from typing import Optional
from jinja2 import TemplateError
from .log import configure_logging
from .site import SiteRoot
from .build import build as build_page
from .cli import  BuildStats
from . import __version__

logger = logging.getLogger(__name__)
cwd = Path(os.getcwd())

def main(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(prog="cli")
    commands = parser.add_subparsers(dest="command", required=True)

    # Global Arguments
    parser.add_argument("-v", "--verbose", action="store_true", help="Show more info in logs")
    parser.add_argument("--version", action="version", version=__version__)

    # Build command
    build_cmd = commands.add_parser("build", help="Build the site.")
    build_cmd.add_argument(
        "-f","--force", action="store_true", help="Rebuild all pages.")
    build_cmd.add_argument(
        "-c","--clean", action="store_true", help="Clear the output directory, then build.")
    build_cmd.add_argument(
        "-d","--dry-run", action="store_true", help="Run as normal. but don't create build files.")
    build_cmd.add_argument(
        "-p", "--working-dir", type=Path, default=cwd,
        help="Use the specified directory, instead of the current directory")

    args = parser.parse_args(argv)
    configure_logging(args.verbose)
    match args.command:
        case "build":
            build(
                force=args.force,
                directory=args.working_dir,
                perform_clean=args.clean,
                dry_run=args.dry_run,
            )
        case _:
            parser.print_help()



def build(force: bool, directory: Path, perform_clean: bool, dry_run: bool) -> None:
    logger.info("Building site at %s.", directory)
    s_time = time.perf_counter()
    site = SiteRoot(directory)
    build_stats = BuildStats()
    site.make_tree()
    i, m = 0, len(site.tree)
    logger.info("Building %d pages...", len(site.tree))

    for context in site.tree:
        i += 1
        if not (context.is_modified or force):
            logger.debug("%s not modified.",context.source_path.name)
            continue

        try:
            logger.info("[%d/%d] %s.",i, m, context.source_path.name)
            build_page(context)

        except (OSError, TemplateError) as e:
            build_stats.errors += 1
            logger.error("%s: %s",context.source_path.name, "".join(e.args))

        build_stats.add_stat(context.build_reason)

    e_time = time.perf_counter()
    build_stats.time_seconds = e_time - s_time

    logger.info(build_stats.summary(m))

if __name__ == "__main__":
    main()
