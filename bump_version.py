import argparse
import re
import sys
from datetime import datetime
from enum import Enum
from os.path import join, dirname, realpath

BASE_PATH = dirname(realpath(__file__))

VERSION_FILE_LOCATION = join(BASE_PATH, 'pyzonky', '__init__.py')
CHANGELOG_FILE = join(BASE_PATH, 'CHANGELOG.md')


def get_actual_version(file_version=VERSION_FILE_LOCATION):
    with open(file_version) as fp:
        version_file_content = fp.read()
    return re.search("(\d+\.\d+\.\d+)", version_file_content).group()


def get_increased_version(version_type):
    actual_version = get_actual_version()
    major, minor, patch = [int(x) for x in actual_version.split(sep='.')]
    if version_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif version_type == 'minor':
        minor += 1
        patch = 0
    elif version_type == 'patch':
        patch += 1
    else:
        print("No version type specified.")

    return "{}.{}.{}".format(major, minor, patch)


valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}


def replace_file_version(old_version, new_version, file_version=VERSION_FILE_LOCATION):
    with open(file_version) as fp:
        version_file_content = fp.read()

    new_version_file_content = version_file_content.replace(old_version, new_version)

    with open(file_version, 'w') as fp:
        fp.write(new_version_file_content)


def change_version(version_type):
    actual_version = get_actual_version()
    new_version = get_increased_version(version_type)
    print("Actual version: {}\nNew version: {}".format(get_actual_version(), new_version))
    print("Change version: [y/n]")
    answer = input("Answer: ").lower()
    if not valid[answer]:
        sys.exit(0)
    else:
        replace_file_version(old_version=actual_version, new_version=new_version)
        edit_changelog(new_version=new_version)
        print("Done")


def edit_changelog(new_version, change_log_file=CHANGELOG_FILE):
    with open(change_log_file) as fp:
        file_content = fp.read()

    unreleased_line = "## [Unreleased]"
    replacement_text = "{}\n\n## {} - {}".format(unreleased_line, new_version, datetime.now().strftime("%Y-%m-%d"))
    new_file_content = file_content.replace(unreleased_line, replacement_text)

    with open(change_log_file, 'w') as fp:
        fp.write(new_file_content)


class Commands(Enum):
    NEXT = 'next'
    PRINT = 'print'

    def __str__(self):
        return self.value


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bump version')

    parser.add_argument('command', type=Commands, choices=list(Commands), help='Program commands')
    parser.add_argument('--major', action='store_true', help='Increase major version')
    parser.add_argument('--minor', action='store_true', help='Increase minor version')
    parser.add_argument('--patch', action='store_true', help='Increase patch version')
    args = parser.parse_args()

    if args.major:
        version_type = 'major'
    elif args.minor:
        version_type = 'minor'
    else:
        version_type = 'patch'

    if args.command == Commands.PRINT:
        print(get_actual_version())
    if args.command == Commands.NEXT:
        change_version(version_type)
