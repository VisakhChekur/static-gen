# External library imports
import typer

# Local imports
from builder.builder import Builder
from builder.exceptions import NoTemplateDirectoryFound, ProjectDirectoryNotFound
from generator.generator import Generator
from generator import exceptions as gen_exceptions

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
def generate_sites(filename: str = ""):

    processed_articles = 0
    if not filename:
        try:
            generator = Generator()
            processed_articles = generator.generate_all_articles()
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

    typer.secho(f"\nProcessed {processed_articles} articles", fg="blue")


if __name__ == "__main__":

    app()
