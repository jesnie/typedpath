from typedpath.base import TypedFile


class BytesFile(TypedFile):
    """A file containing raw bytes."""

    default_suffix = ".bin"

    def write(self, data: bytes) -> int:
        """Sets the contents of this file."""
        return self.write_path().write_bytes(data)

    def read(self) -> bytes:
        """Gets the contents of this file."""
        return self.read_path().read_bytes()
