import mimetypes
import re
from pathlib import Path

from cvaugmentor.domain.schemas.media import MediaKind

DIGITS = re.compile(r"([0-9]+)")


def _alphanumeric_key(path: Path) -> list[object]:

    """

    The sort key that orders 2 before 10, which a plain string sort does not.

    """

    return [int(part) if part.isdigit() else part.lower() for part in DIGITS.split(path.name)]


class LocalWorkspace:

    """

    Reads what a directory on this machine holds.


    Usage
    -----
    Entries come back in the order a person reading filenames expects, so
    frame_2.png precedes frame_10.png. The kind of a file is read from its
    name rather than its bytes, which is what lets a listing be filtered
    without decoding everything in the directory.
    ```python
    from cvaugmentor.adapters.workspace import LocalWorkspace

    workspace = LocalWorkspace()
    entries = workspace.list_entries(Path("samples"))
    ```

    """

    def list_entries(self, directory: Path) -> list[Path]:

        """

        Lists the files a directory holds directly, ordered for a reader.


        Parameters
        ----------
        directory : Path
            The directory to list.


        Returns
        -------
        list[Path]
            Every file directly inside it, alphanumerically ordered.


        Raises
        ------
        NotADirectoryError
            If `directory` does not name a directory.

        """

        if not directory.is_dir():
            raise NotADirectoryError(f"directory must name a directory. Received: {directory}")


        return sorted((entry for entry in directory.iterdir() if entry.is_file()), key=_alphanumeric_key)


    def is_kind(self, path: Path, kind: MediaKind) -> bool:

        """

        Whether a path names a medium of the given kind.


        Parameters
        ----------
        path : Path
            The path whose name is read.

        kind : MediaKind
            The medium kind to test for.


        Returns
        -------
        bool
            True when the name's media type belongs to that kind.


        Raises
        ------
        None.

        """

        guessed = mimetypes.guess_type(path.name)[0]

        return guessed is not None and guessed.startswith(f"{kind}/")
