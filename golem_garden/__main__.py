from golem_garden.command_line_interface import chat_with_golem


def main(cli: bool = True):
    if cli:
        chat_with_golem()


if __name__ == "__main__":
    main()
