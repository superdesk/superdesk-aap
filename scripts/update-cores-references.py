#!/usr/bin/env python3
import feedparser
import fileinput
import re
import sys
import getopt

TO_BE_UPDATED = [
    # superdesk-core
    {
        'feed_url': 'https://github.com/superdesk/superdesk-core/commits/',
        'file_name': 'server/requirements.txt',
        'pattern': 'superdesk-core.git@([a-f0-9]*)'
    },
    # superdesk-client-core
    {
        'feed_url': 'https://github.com/superdesk/superdesk-client-core/commits/',
        'file_name': 'client/package.json',
        'pattern': 'superdesk-client-core#([a-f0-9]*)'
    }
]

def get_last_commit(url):
    feed = feedparser.parse(url)
    return feed['entries'][0]['id'].split('/')[1][:9]


def replace_in_file(filename, search, new_value):
    textfile = open(filename, 'r')
    filetext = textfile.read()
    textfile.close()
    matches = re.findall(search, filetext)
    with fileinput.FileInput(filename, inplace=True) as file:
        for line in file:
            print(line.replace(matches[0], new_value), end='')


def get_branch():
    branch = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hb:', ['branch='])
    except getopt.GetoptError:
        print('usage: {} -b <branch_name>'.format(sys.argv[0]))
        return
    for opt, arg in opts:
        if opt == '-h' or opt not in ('-b', '--branch'):
            print('usage: {} -b <branch_name>'.format(sys.argv[0]))
        elif opt in ('-b', '--branch'):
            branch = arg
    return branch


if __name__ == '__main__':
    branch = get_branch()
    if not branch:
        print('usage: {} -b <branch_name>'.format(sys.argv[0]))
        sys.exit(2)

    print('modiying files.......')
    for repo in TO_BE_UPDATED:
        last_commit_hash = get_last_commit(repo['feed_url'] + '{}.atom'.format(branch))
        replace_in_file(repo['file_name'], repo['pattern'], last_commit_hash)
        print('modified file: {}'.format(repo['file_name']))
    print('all files modified')
