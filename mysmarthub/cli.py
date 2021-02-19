import inspect
import json
import os
import shutil

import click

try:
    from mysmarthub import settings
except ModuleNotFoundError:
    import settings


def get_root_path(file_name):
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    folder = os.path.dirname(os.path.abspath(filename))
    path = os.path.join(folder, file_name)
    return path


class JsonFile:
    def __init__(self, file):
        self.file = file
        self.apps = self.get_data()

    def get_data(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, 'r') as f:
                    json_data = json.load(f)
            except (json.decoder.JSONDecodeError, FileNotFoundError):
                return {}
            else:
                return json_data
        return {}


def smart_print(text='', char='-'):
    if not char:
        char = ' '
    columns, _ = shutil.get_terminal_size()
    if text:
        print(f' {text} '.center(columns, char))
    else:
        print(f''.center(columns, char))


def open_json_file(file):
    try:
        with open(file, 'r') as f:
            json_data = json.load(f)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        return {}
    else:
        return json_data


def start_logo():
    smart_print('', '*')
    smart_print(f'{settings.TITLE} v{settings.VERSION}', '=')
    smart_print(f'{settings.DESCRIPTION}')


def end_logo():
    smart_print(f'{settings.YANDEX}', '-')
    smart_print(f'{settings.COPYRIGHT}', '=')
    smart_print('', '*')


def get_default_file(name=settings.FILE_NAME):
    json_file = get_root_path(name)
    return json_file


def get_app(obj):
    while 1:
        num_app_dict = {n: name for n, name in enumerate(obj.apps.keys(), 1)}
        smart_print('List of applications')
        for n, name in num_app_dict.items():
            print(f'{n}. {name}')
        click.echo(f'0. Exit')
        smart_print()
        num = click.prompt('Application number + Enter', type=int)
        if not num:
            return 0
        if num not in num_app_dict:
            click.echo('Error! Enter the application number from the list.')
            continue
        app = num_app_dict[num]
        return app


def get_action(link_dict):
    while 1:
        smart_print('Action selection menu')
        if 'description' in link_dict:
            click.echo(f'i: Info')
        elif "link" in link_dict:
            click.echo('o: Official site')
        if 'clone' in link_dict:
            click.echo(f'c: Clone')
        if 'download' in link_dict:
            click.echo(f'd: Download')
        if 'pip' in link_dict:
            click.echo(f'p: Install with pip')
        click.echo("  b: back")
        char = click.getchar()
        if char in ('i', 'ш'):
            menu = 'info'
        elif char in ("o", "щ"):
            menu = "open"
        elif char in ("c", "с"):
            menu = "clone"
        elif char in ("d", "в"):
            menu = "downloads"
        elif char in ("p", "з"):
            menu = "pip"
        elif char in ("b", "и"):
            menu = "quit"
        else:
            click.echo("Invalid input")
            continue
        return menu


def open_site_menu(obj, app):
    while 1:
        smart_print("Open site")
        site = obj.apps[app]['link']
        click.echo(site)
        smart_print()
        click.echo('o: Open site')
        click.echo("  b: back")
        char = click.getchar()
        if char in ("b", "и"):
            return "main"
        elif char in ('o', "щ"):
            click.launch(site)
        else:
            click.echo("Invalid input")
        smart_print()
        input('Enter to continue...')


def clone_menu(obj, app):
    while 1:
        smart_print("Clone link")
        site = obj.apps[app]['clone']
        click.echo(site)
        smart_print()
        click.echo('c: Clone')
        click.echo("  b: back")
        char = click.getchar()
        if char in ("b", "и"):
            return "main"
        elif char in ("c", "с"):
            os.system(f'git clone {site}')
        else:
            click.echo("Invalid input")
        smart_print()
        input('Enter to continue...')


def downloads_menu(obj, app):
    while 1:
        smart_print("Downloads link")
        site = obj.apps[app]['download']
        click.echo(site)
        smart_print()
        click.echo('d: Downloads')
        click.echo("  b: back")
        char = click.getchar()
        if char in ("b", "и"):
            return "main"
        elif char == 'd':
            os.system(f'wget {site}')
        else:
            click.echo("Invalid input")
        smart_print()
        input('Enter to continue...')


def pip_menu(obj, app):
    while 1:
        smart_print("Pip install")
        app_name = obj.apps[app]['pip']['name']
        link = obj.apps[app]['pip']['link']
        click.echo(f'Name: {app_name}')
        click.echo(f'Link: {link}')
        smart_print()
        click.echo('o: Open')
        click.echo('i: Install')
        click.echo("  b: back")
        char = click.getchar()
        if char in ("b", "и"):
            return "main"
        elif char in ("o", "щ"):
            click.launch(link)
        elif char in ('i', 'ш'):
            smart_print()
            click.echo('Starting installation...')
            smart_print()
            status = os.system(f'pip install {app_name}')
            if status:
                os.system(f'pip3 install {app_name}')
            smart_print()
        else:
            click.echo("Invalid input")
        smart_print()
        input('Enter to continue...')


def info_menu(obj, app):
    smart_print()
    click.echo(f'{obj.apps[app]["description"]}')
    smart_print()
    input('Enter to continue...')
    return 'main'


@click.command()
def cli():
    start_logo()
    default_file = get_default_file()
    json_file = JsonFile(default_file)
    while 1:
        app = get_app(json_file)
        if not app:
            break
        link_dict = json_file.apps[app]
        menu = 'main'
        while 1:
            if menu == "main":
                smart_print(f'Application selected: {app}')
                menu = get_action(link_dict=link_dict)

            elif menu == 'info':
                menu = info_menu(json_file, app)

            elif menu == "open":
                menu = open_site_menu(json_file, app)

            elif menu == "clone":
                menu = clone_menu(json_file, app)

            elif menu == "downloads":
                menu = downloads_menu(json_file, app)

            elif menu == "pip":
                menu = pip_menu(json_file, app)

            elif menu == "quit":
                break
    end_logo()


if __name__ == '__main__':
    cli()
