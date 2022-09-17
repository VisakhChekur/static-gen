# Standard library imports
import shutil
from pathlib import Path
from typing import Callable

# External library imports
import markdown
import typer

from generator import exceptions

# Local imports
from generator.parser import Parser
from generator.templater import ArticleTemplater, PageTemplater
from generator.types import FileDetails
from helpers import get_config


class Generator:
    """A class to generate the HTML content as well as the metadata."""

    def __init__(self, theme: str = "default"):

        self.theme: str = theme

        self._project_dir: Path
        self._content_dir: Path
        self._publish_dir: Path
        (
            self._project_dir,
            self._content_dir,
            self._publish_dir,
        ) = self._get_directories()

        self._parser: Parser = Parser()
        self._article_templater: ArticleTemplater = ArticleTemplater()
        self._page_templater: PageTemplater = PageTemplater()

    def generate_single_article(self, filepath: Path):
        """Generates the HTML file for an article and saves it."""

        parsed_contents = self._parser.parse(filepath)
        parsed_contents["content"] = markdown.markdown(parsed_contents["content"])
        rendered_html = self._article_templater.render(parsed_contents)
        self._save_rendered_html(filepath, rendered_html)

    def generate_single_page(self, filepath: Path):
        """Generates the HTML file for a page (home page, about me etc.) and saves it."""

        parsed_contents = self._parser.parse(filepath)
        parsed_contents["content"] = markdown.markdown(parsed_contents["content"])
        template_name = self._get_page_template_name(filepath)
        rendered_html = self._page_templater.render(
            parsed_contents, template=template_name
        )
        self._save_rendered_html(filepath, rendered_html)

    def generate_all_pages(self) -> int:
        """Generates and saves all the HTML files in the pages directory. Returns the number
        of HTML files generated."""

        self._set_theme()

        return self._generate_all(
            self._content_dir / "pages", generator_method=self.generate_single_page
        )

    def generate_all_articles(self) -> int:
        """Generates and saves all the HTML files for all markdown files in the articles
        directory. Returns the number of HTML files generated."""

        # TODO: Only set theme if the theme has changed.
        self._set_theme()

        return self._generate_all(
            self._content_dir / "articles",
            generator_method=self.generate_single_article,
        )

    # ----- HELPER METHODS -----
    def _generate_all(
        self, dirpath: Path, *, generator_method: Callable[[Path], None]
    ) -> int:
        """Generates HTML files for all markdown files in a given directory. All
        subdirectories will also be checked recursively for markdown files. Returns
        the number of processed files."""

        # Getting the markdown files
        md_files = [path for path in dirpath.rglob("*.md")]

        missing_metadata: list[FileDetails] = []
        invalid_metadata: list[FileDetails] = []

        # Generating the HTML file
        for md_file in md_files:
            try:
                generator_method(md_file)  # type: ignore
            except exceptions.NoMetadata:
                file_details = FileDetails(md_file.name, md_file)
                missing_metadata.append(file_details)
            except exceptions.InvalidMetadataSyntax:
                file_details = FileDetails(md_file.name, md_file)
                invalid_metadata.append(file_details)

        processed_files = len(md_files) - len(missing_metadata) - len(invalid_metadata)
        if len(missing_metadata) or len(invalid_metadata):
            self._print_errors(missing_metadata, invalid_metadata)

        return processed_files

    def _print_errors(
        self,
        missing_metadata: list[FileDetails],
        invalid_metadata: list[FileDetails],
    ):
        """Prints the errors in the files that were not processed."""

        if len(missing_metadata):
            typer.secho("\nMissing metadata for the following:\n", fg="magenta")
            for file_details in missing_metadata:
                details = f"Filename: {file_details.filename} | Filepath: {file_details.filepath}"
                typer.secho(details)

        if len(invalid_metadata):
            typer.secho("\nInvalid metadata syntax for the following:\n", fg="magenta")
            for file_details in invalid_metadata:
                details = f"Filename: {file_details.filename} | Filepath: {file_details.filepath}"
                typer.secho(details)

    def _save_rendered_html(self, filepath: Path, content: str) -> None:
        """Saves the rendered HTML file in the publish directory."""

        fp = self._publish_dir / (filepath.stem + ".html")
        with open(fp, "w+") as f:
            f.seek(0)
            f.write(content)

    def _get_directories(self) -> tuple[Path, Path, Path]:
        """Returns the project, content and publish directory paths."""

        config = get_config()
        if "project_directory" not in config:
            raise exceptions.InvalidConfig(
                "Missing 'project_directory' in 'config.json'"
            )

        project_dir = Path(config["project_directory"])
        content_dir = project_dir / "content"
        publish_dir = project_dir / "publish"
        if not content_dir.exists():
            raise FileNotFoundError("'content' directory was not found")
        if not publish_dir.exists():
            raise FileNotFoundError("'publish' directory was not found")

        return project_dir, content_dir, publish_dir

    def _set_theme(self):
        """Creates the appropriate static directory with the theme related files
        in the publish directory."""

        theme_name, theme_dir = self._get_theme_directory()
        if theme_name != self.theme:
            typer.secho(
                f"\nCouldn't find theme {self.theme} and fell back to theme '{theme_name}'",
                fg="red",
            )

        publish_static_dir = self._publish_dir / "static"
        shutil.copytree(theme_dir, publish_static_dir, dirs_exist_ok=True)

    def _get_theme_directory(self) -> tuple[str, Path]:
        """Tries to find the directory with the files related to the theme.
        If such a directory does not exist then it falls back to the "default" theme."""

        templates_dir = self._project_dir / "templates"
        if not templates_dir.exists():
            raise FileNotFoundError("'templates' directory was not found")

        theme_dir = templates_dir / self.theme
        if theme_dir.exists():
            return self.theme, theme_dir

        default_theme = self._get_default_theme()
        default_dir = templates_dir / "themes" / default_theme
        if not default_dir.exists():
            message: str = f"couldn't find theme '{self.theme}' and tried to \
             fall back to '{default_theme}' theme but couldn't find that as well"

            raise FileNotFoundError(message)

        return default_theme, default_dir

    def _get_default_theme(self) -> str:
        """Returns the default theme set up in the project configuration."""

        config = get_config()
        return config.get("theme", "default")

    def _get_page_template_name(self, filepath: Path) -> str:
        """Creates the page template name from the filename and returns it."""

        return filepath.stem + "_template.html"
