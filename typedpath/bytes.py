from typedpath.base import TypedFile


class BytesFile(TypedFile):
    default_suffix = ".bin"

    def write(self, data: bytes) -> int:
        return self.write_path().write_bytes(data)

    def read(self) -> bytes:
        return self.read_path().read_bytes()
