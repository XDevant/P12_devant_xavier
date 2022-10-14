from pathlib import Path
from datetime import datetime


def get_install_date(path=None):
    if not path:
        base = Path(__file__).resolve().parent.parent
        path = str(base)
    file = path + '\\errors.log'
    with open(file, 'r', encoding='cp1252') as f:
        for row in f:
            if "Started: " in row:
                try:
                    creation = ' '.join(row.split(' ')[1:])
                    return creation[:-1]
                except IndexError:
                    return None


def set_install_date(creation_date=None, path=None):
    if creation_date is None:
        creation_date = str(datetime.now())
        creation_date = ':'.join(creation_date.split(':')[:2])
    if not path:
        base = Path(__file__).resolve().parent.parent
        path = str(base)
    file = path + '\\errors.log'
    with open(file, 'w', encoding='cp1252') as f:
        print(f"Started: {creation_date}", file=f)


if __name__ == "__main__":
    set_install_date()
    print(get_install_date())
