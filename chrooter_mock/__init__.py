#!/bin/env python
from __future__ import print_function

import sys
from subprocess import call

from chrooter.provider import Provider


class MockEnv(object):
    def __init__(self, distro):
        self.command = ['mock_runner.sh']
        self.distro = distro

    def start_interactive_shell(self):
        command = list(self.command)
        command.extend((
            '--shell',
            self.distro,
        ))
        return call(command)

    def execute_scripts(self, scripts):
        command = list(self.command)
        for script in scripts:
            command.extend((
                '--execute-script',
                script,
            ))
        return call(command)


class MockProvider(Provider):
    def run(self, args):
        rc = 0
        mock_env = MockEnv(distro=args.distro)
        if args.scripts:
            rc = mock_env.execute_scripts(args.scripts)
        if args.shell:
            rc = mock_env.start_interactive_shell()
        sys.exit(rc)

    def populate_parser(self, parser):
        group = parser.add_mutually_exclusive_group(
            required=True
        )
        group.add_argument(
            '-s',
            '--execute-script',
            dest='scripts',
            action='append',
            help='Script ot run, can be specified more than once',
        )
        group.add_argument(
            '-S',
            '--shell',
            action='store_true',
            help=(
                'Run an interactive shell, if ant script is specified, the '
                'shell will be started after the script run'
            ),
        )
