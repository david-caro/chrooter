#!/bin/env python
from __future__ import print_function

import sys
import logging

from chrooter.provider import Provider
from chrooter.utils import call


LOGGER = logging.getLogger(__name__)


class MockEnv(object):
    def __init__(self, distro):
        self.command = ['mock_runner.sh']
        self.distro = distro

    def set_try_proxy(self):
        self.command.append('--try-proxy')

    def set_mock_confs_dir(self, mock_confs_dir):
        self.command.extend((
            '--mock-confs-dir',
            mock_confs_dir,
        ))

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
                self.distro,
            ))
        return call(command)


class MockProvider(Provider):
    def run(self, args, scripts=None, interactive=False):
        rc = 0
        mock_env = MockEnv(distro=args.distro)

        if args.mock_confs_dir:
            mock_env.set_mock_confs_dir(args.mock_confs_dir)
        if args.try_proxy:
            mock_env.set_try_proxy()

        if scripts:
            rc = mock_env.execute_scripts(scripts)
        if interactive:
            rc = mock_env.start_interactive_shell()
        sys.exit(rc)

    def populate_parser(self, parser):
        parser.add_argument(
            '-P', '--try-proxy',
            action='store_true',
            help=(
                'If set, will try to use the proxied config and set the '
                'proxy inside the mock env'
            )
        )
        parser.add_argument(
            '-C', '--mock-confs-dir',
            help=(
                'Directory where the base mock configs are located (default '
                'is /etc/mock'
            )
        )
