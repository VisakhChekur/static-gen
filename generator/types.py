from typing import TypedDict, NamedTuple
from pathlib import Path


class PartitionedType(TypedDict):
    """Type that represents the dictionary that holds the partitioned file content."""

    content: str
    metadata: list[str]


class ParsedFileData(TypedDict):
    """Type that represents the dictionary that holds the data after parsing the file."""

    content: str
    metadata: dict[str, str]


class FileDetails(NamedTuple):
    """Type that represents the namedtuple that holds the details of a file."""

    filename: str
    filepath: Path
