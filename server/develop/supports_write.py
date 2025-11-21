from typing import Protocol

class SupportsWrite(Protocol):
    def write(self, __s: str) -> object:
        """Writes a string to the underlying stream."""
        ...