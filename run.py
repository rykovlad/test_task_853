import click

from parser.main import parse_and_push


@click.group()
def cli():
    pass

@click.command()
@click.option('--target_chat_username')
@click.option('--session_numb')
def task_parse_and_push(target_chat_username, session_numb) -> None:
    parse_and_push(target_chat_username, session_numb)



def add_commands(*commands):
    for command in commands:
        cli.add_command(command)


add_commands(task_parse_and_push)


if __name__ == '__main__':
    cli()