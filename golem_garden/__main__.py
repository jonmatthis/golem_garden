from golem_garden.user_interface.command_line_interface import chat_with_golem
from golem_garden.user_interface.jupyter_widget import run_qtconsole


def main(cli: bool = False):
    if cli:
        chat_with_golem()
    else:
        run_qtconsole()


if __name__ == "__main__":
    main()
