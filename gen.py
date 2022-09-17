# Standard library imports
import time

# External library imports
import typer

# Local imports
from helpers import get_config
from builder.builder import Builder
from generator.generator import Generator
from generator import exceptions as gen_exceptions
from builder.exceptions import NoTemplateDirectoryFound, ProjectDirectoryNotFound

app = typer.Typer()


@app.command("init")
def initialize_project(filepath: str = "."):

    builder = Builder(filepath)
    try:
        builder.build()
    except ProjectDirectoryNotFound:
        typer.secho("\nSpecified project directory was not found", fg="red")
        return
    except NoTemplateDirectoryFound:
        typer.secho(
            "\nPlease add the original templates directory as an environment variable",
            fg="red",
        )
        typer.secho("\n\nSet it to the variable GEN_TEMPLATES", fg="blue")
        return
    except FileExistsError as e:  # Usually means the project has already been initialized
        typer.secho(f"\n{str(e)}", fg="red")
        return

    typer.secho("\nInitialized project", fg="green")


@app.command("make")
def generate_sites(
    filename: str = "",
    articles: bool = typer.Option(default=False),
    pages: bool = typer.Option(default=False),
):

    # TODO: Add support for making only articles or only pages or both.
    processed_articles = processed_pages = 0
    start_time = time.time()
    if not filename:
        try:
            generator = Generator()
            processed_articles = generator.generate_all_articles()
            processed_pages = generator.generate_all_pages()
        except gen_exceptions.ConfigNotFound:
            typer.secho(
                "\n'config.json' not found. Please make sure to run the command from the root of the directory",
                fg="red",
            )
            return
        except gen_exceptions.InvalidConfig as e:
            typer.secho("\nInvalid config", fg="red")
            typer.secho(e.error)
            return
    end_time = time.time()
    total_time = end_time - start_time
    typer.secho(
        f"\nProcessed {processed_articles} articles and {processed_pages} pages in {total_time:.3f} seconds.",
    )


@app.command("update")
def update_directory(directory: str):

    try:
        config: dict[str, str] = get_config()
    except FileNotFoundError:
        typer.secho(
            "\n'config.json' was not found. Please run the command from the root directory of the project",
            fg="red",
        )
        return

    if "project_directory" not in config:
        typer.secho("\n'project_directory' missing in 'config.json'", fg="red")
        return

    builder = Builder(config["project_directory"])
    directories = {
        "templates": builder.update_templates_directory,
    }
    update = directories.get(directory, None)

    if not update:
        typer.secho("\nInvalid directory name", fg="red")
        return

    update()
    typer.secho(f"\nUpdated '{directory}' successfully!", fg="green")


if __name__ == "__main__":

    app()
