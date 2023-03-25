import click

from golem_garden.user_interface.command_line_interface import chat_with_golem


@click.command()
@click.option('--cli', is_flag=True, help="Run the command line interface.")
def main(cli: bool = True):
    if cli:
        chat_with_golem()


if __name__ == "__main__":
    main()
