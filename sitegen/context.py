from datetime import datetime, timezone
from pathlib import Path
from typing import Final, Optional


class BuildContext:
    """
    Initialize a build context from relative paths.

    :ivar curr_working_dir: Current working directory used as the base for all paths.
    :ivar source_path: Path to the source content directory relative to webroot.
    :ivar source_path_lastmod: The last modified date of the source file.
    :ivar dest_path: Path to the output destination directory relative to webroot.
    :ivar dest_path_lastmod: The last modified date of the destination file if exists.
    :ivar template_path: Path to the template directory relative to webroot.
    """
    curr_working_dir: Final[Path]
    source_path: Final[Path]
    source_path_lastmod: Final[datetime]
    dest_path: Final[Path]
    dest_path_lastmod: Final[Optional[datetime]]
    template_path = Final[Path]

    def __init__(self, cwd: Path, source: Path, dest: Path):
        self.curr_working_dir = cwd
        self.source_path = cwd.joinpath("_public", source)
        self.dest_path = cwd.joinpath(dest)
        self.template_path = cwd.joinpath("_fragments")

        self.source_path_lastmod = datetime.fromtimestamp(
            self.source_path.stat().st_mtime,
            tz=timezone.utc
        )

        if self.dest_path.exists():
            self.dest_path_lastmod = datetime.fromtimestamp(
                self.dest_path.stat().st_mtime,
                tz=timezone.utc
            )
        else:
            self.dest_path_lastmod = datetime.fromtimestamp(
                0,
                tz=timezone.utc
            )

    @property
    def is_modified(self) -> bool:
        if self.dest_path_lastmod:
            return self.source_path_lastmod > self.dest_path_lastmod
        return False
