from typedpath.base import PathLikeLike, TypedFile


class TextFile(TypedFile):
    default_suffix = ".txt"

    def __init__(self, path: PathLikeLike, *, encoding: str | None = None) -> None:
        super().__init__(path)

        self._encoding = encoding

    def write(
        self,
        data: str,
        *,
        errors: str | None = None,
        newline: str | None = None,
    ) -> int:
        return self.write_path().write_text(
            data, encoding=self._encoding, errors=errors, newline=newline
        )

    def read(self, errors: str | None = None) -> str:
        return self.read_path().read_text(encoding=self._encoding, errors=errors)
