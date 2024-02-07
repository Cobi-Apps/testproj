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


def status_up_to_date():
    branch_status =  process_git('status')
    return 'up to date' in branch_status.split('\n')[1]


def get_version():
    return process_git('describe --tags --abbrev=0')


def set_tag(tag):
    process_git(f'tag {tag}')
    process_git(f'git push origin {tag}')


def commits_after_tag():
    commits_no = process_git('describe --tags')
    if '-' not in commits_no:
        return 0
    return int(commits_no.split('-')[1])


def main():
    version = get_version()
    branch = get_branch()
    print (status_up_to_date())
    print(f'Branch:  {branch}\nVersion: {version}')
    if not re.search('[0-9]*.[0-9]*.[0-9]*', version):
        print ('Last tag is not a compatible version number')
        return
    else:
        if commits_after_tag() and branch.lower() in ['master', 'main']:
            version_numbers = [int(d) for d in version.split('.')]
            version_increase = 'x'
            release_types = {
                'p': 2,
                '': 2,
                'm': 1,
                'j': 0,
            }
            while version_increase not in list(release_types.keys()) + ['q']:
                version_increase = input('Type of release major(j)/minor(m)/patch(p) or Q to quit?  ').lower()
            if version_increase == 'q':
                return
            version_numbers[release_types[version_increase]] += 1
            new_version = '.'.join([str(v) for v in version_numbers])
            set_tag(new_version)
            print(f'New version {new_version}')
        else:
            print(f'Not updated, commits after version/tag {commits_after_tag()}')


if __name__ == '__main__':
    main()
