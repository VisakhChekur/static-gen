# Standard library imports
from pathlib import Path
from typing import Optional

# External library imports
import typer
from jinja2 import Environment, FileSystemLoader


# Local imports
from generator.types import ParsedFileData
from helpers import get_config


# ----- CONSTANTS -----


# TODO: Find out a better way of handling this so that I'm not doing so many file reads.
def get_templates_dir() -> Path:
    try:
        config = get_config()
        return Path(config["project_directory"]) / "templates"
    except FileNotFoundError:
        return Path(".") / "templates"
    except KeyError:
        return Path(".") / "templates"


class Templater:
    """Base class that handles the templating using Jinja2."""

    JINJA_ENV = Environment(
        loader=FileSystemLoader(get_templates_dir()), autoescape=False
    )

    @staticmethod
    def get_templates_list() -> list[str]:
        """Returns a list of the templates"""
        return Templater.JINJA_ENV.list_templates()

    def render(self, filedata: ParsedFileData) -> str:
        raise NotImplementedError("to be implemented by subclass")

    def _create_jinja_variables(self, filedata: ParsedFileData) -> dict[str, str]:

        jinja_variables: dict[str, str] = {**filedata["metadata"]}
        jinja_variables["content"] = filedata["content"]
        return jinja_variables


class ArticleTemplater(Templater):
    def render(self, filedata: ParsedFileData) -> str:

        jinja_variables = self._create_jinja_variables(filedata)
        article_template = Templater.JINJA_ENV.get_template("article_template.html")
        return article_template.render(jinja_variables)


class PageTemplater(Templater):
    # TODO: Find out if there's a way to properly override where Pylance doesn't complain.
    def render(self, filedata: ParsedFileData, *, template: str) -> str:  # type: ignore

        jinja_variables = self._create_jinja_variables(filedata)
        page_template = Templater.JINJA_ENV.get_template(template)
        return page_template.render(jinja_variables)
