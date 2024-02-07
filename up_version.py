import json
import os
import re
import subprocess


def process_git(command):
    return subprocess.check_output(['git'] + command.split(' ')).decode('utf8').strip()


def get_git_revision_hash():
    return process_git('rev-parse HEAD')


def get_git_revision_short_hash():
    return process_git('rev-parse --short HEAD')


def get_branch():
    return process_git('rev-parse --abbrev-ref HEAD')


def commits():
    return process_git('log --pretty=oneline')


def get_version():
    return process_git('describe --tags --abbrev=0')


def set_tag(tag):
    return process_git(f'tag {tag}')


def commits_after_tag():
    commits_no = process_git('describe --tags')
    if '-' not in commits_no:
        return 0
    return int(commits_no.split('-')[1])


version = get_version()
if re.search('[0-9]*.[0-9]*.[0-9]*', version) and commits_after_tag():

    version_numbers = [int(d) for d in version.split('.')]
    version_increase = 'x'

    release_types = {
        'p': 2,
        '': 2,
        'm': 1,
        'j': 0,
    }

    while version_increase not in list(release_types.keys()):
        version_increase = input('Type of release patch(p)/minor(m)/major(j)?')

    version_numbers[release_types[version_increase]] += 1
    set_tag('.'.join([str(v) for v in version_numbers]))
    print ('.'.join([str(v) for v in version_numbers]))


