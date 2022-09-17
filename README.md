# GEN

A static site generator that will generate HTML files from markdown files made using Python.

NOTE: This is made for personal use. So you use at your own risk!!

# How?

* uses [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/) as the template engine
* uses [Markdown](https://daringfireball.net/projects/markdown/) to convert the markdown files into HTML files
* uses [Typer](https://typer.tiangolo.com/) for the CLI

# Installation

1. Clone the repository 

    `git clone https://github.com/VisakhChekur/static-gen.git`

2. Install the dependencies 

    * with [Poetry](https://python-poetry.org/)

        * `poetry install`

    * without [Poetry](https://python-poetry.org/)
        * `pip install -r requirements.txt`

3. Add the path to the directory that holds `gen.py` to the PATH environment variable

4. Set the path to the `templates` directory as `GEN_TEMPLATES` environment variable.

# Usage

* `gen init` - creates the initial project structure

* `gen make` - creates the HTML files and saves them to the `publish` directory as well as the necessary static files
    * NOTE: this must be ran at the root of your project where `config.json`

# Configuration

* `config.json` holds the configuration details of the project which can be modified as needed

* `theme` can be changed to change the default theme

# Creating Themes

1. create a new folder in the `templates/themes/` directory with the name of your theme
2. change the value of `theme` to the name of your theme in `config.json`
3. run `gen make` at the root of your project where `config.json` lies