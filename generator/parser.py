# Standard library imports
from pathlib import Path

# Local imports
from generator.types import PartitionedType, ParsedFileData
from generator.exceptions import NoMetadata, InvalidMetadataSyntax


class Parser:
    """Handles parsing the markdown files."""

    def parse(self, filepath: Path) -> ParsedFileData:

        partitioned_file_contents = self._partition_file_content(filepath)
        # This returns a dictionary and not a ParsedFileData object at runtime
        # For more information, refer: PEP 589 (https://peps.python.org/pep-0589/)
        return ParsedFileData(
            content=partitioned_file_contents["content"],
            metadata=self._parse_metadata(partitioned_file_contents["metadata"]),
        )

    def _partition_file_content(self, filepath: str | Path) -> PartitionedType:
        """Returns the metadata and the contents stored in the file as
        strings."""

        with open(filepath, "r") as f:
            metadata_exists = False
            metadata = []

            # Reading all the lines until the metadata starts
            for line in f:
                if line.startswith("---"):
                    metadata_exists = True
                    break
            if not metadata_exists:
                raise NoMetadata()

            # Getting the metadata
            for line in f:
                # End of metadata
                if line.startswith("---"):
                    break
                metadata.append(line.rstrip("\n"))  # type: ignore

            # The rest of the lines would be the content
            content = "".join(f)
        return {"metadata": metadata, "content": content}

    def _parse_metadata(self, metadata: list[str]) -> dict[str, str]:
        """Parses the metadata and returns a dictionary containing
        the key value pairs as per the metadata."""

        parsed_metadata: dict[str, str] = {}
        for data in metadata:
            split_data = data.split(":")
            if len(split_data) != 2:
                raise InvalidMetadataSyntax("missing ':' or too many ':'")
            parsed_metadata[split_data[0]] = split_data[1].strip()

        return parsed_metadata
