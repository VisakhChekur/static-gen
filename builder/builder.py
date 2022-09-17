# Standard library imports
import os
import json
import shutil
from pathlib import Path

# Local imports
from builder.exceptions import NoTemplateDirectoryFound, ProjectDirectoryNotFound


class Builder:
    """Class that handles building the initial project structure."""

    content_subdirectories: list[str] = ["articles", "pages"]

    def __init__(self, directory_path: str):

        self._project_directory: Path = Path(directory_path)

    def build(self):

        self._validate_project_directory()
        self._project_directory = Path(self._project_directory)
        self._build_content_directory()
        self._build_publish_directory()
        self._build_templates_directory()
        self._build_config_json()

    def update_templates_directory(self):
        """Updates the templates directory."""

        self._build_templates_directory()

    def _build_content_directory(self):
        """Builds the 'content' directory at the root of the project directory.
        This also builds the 'articles' and 'pages' subdirectories within the 'content'
        directory."""

        content_directory_path = self._project_directory / "content"
        for sub_dir in Builder.content_subdirectories:
            dir_path = content_directory_path / sub_dir
            dir_path.mkdir(parents=True)

    def _build_publish_directory(self):
        """Builds the 'publish' directory at the root of the project directory."""

        publish_directory_path = self._project_directory / "publish"
        publish_directory_path.mkdir()

    def _build_templates_directory(self):
        """Builds the 'templates' directory at the root of the project directory."""

        # Getting templates directory
        stored_templates_dir = os.getenv("GEN_TEMPLATES")
        if not stored_templates_dir:
            raise NoTemplateDirectoryFound()

        # Copying the templates to the project
        templates_dir_path = self._project_directory / "templates"
        shutil.copytree(stored_templates_dir, templates_dir_path, dirs_exist_ok=True)

    def _build_config_json(self):
        """Creates the `config.json` file at the root of the project directory."""

        config = self._get_configuration()
        config_fp = self._project_directory / "config.json"
        with open(config_fp, "w+") as f:
            f.seek(0)
            json.dump(config, f)

    def _get_project_details(self) -> dict[str, str]:
        """Gets the details of the project and creates the configurations."""

        site_name = input("Enter the name of the website: [default: None]")
        theme_input = input("Enter the name of the default theme: [default: default]")
        return {
            "project_name": site_name or "default",
            "theme": theme_input or "default",
        }

    def _get_configuration(self) -> dict[str, str]:
        """Returns the project configuration dictionary."""

        config = {
            "project_directory": str(self._project_directory.absolute()),
        }

        # Returning the two dictionaries after merging them
        return config | self._get_project_details()

    # ----- VALIDATIONS -----
    def _validate_project_directory(self):
        """Ensures the given path exists. Raises the FileNotFoundError if it doesn't exist."""

        if not self._project_directory.exists():
            raise ProjectDirectoryNotFound()
