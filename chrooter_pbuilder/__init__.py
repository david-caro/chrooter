#!/bin/env python
from __future__ import print_function

import sys
from subprocess import call
import os

from chrooter.provider import Provider


class PbuilderEnv(object):
    def __init__(self, distro):
        self.rootdir = os.path.realpath(
            os.path.join(os.curdir, 'pdbuilder_root')
        )
        self.aptcachedir = os.path.join(
            self.rootdir,
            'apt-cache',
        )
        self.basetgz = os.path.join(
            self.rootdir,
            'base.tgz',
        )
        self.command = [
            'pbuilder',
            '--buildplace', self.rootdir,
            '--aptcache', self.rootdir,
            '--basetgz', self.basetgz,
        ]
        if distro.startswith('deb-'):
            distro = distro[4:]
        self.distro = distro
        if not os.path.exists(self.rootdir):
            os.makedirs(self.rootdir)

    def start_interactive_shell(self):
        command = list(self.command)
        command.append('--login')
        return call(command)

    def execute_scripts(self, scripts):
        command = list(self.command)
        for script in scripts:
            command.extend((
                '--execute-script',
                script,
            ))
        return call(command)

    def create(self, extra_packages=None):
        command = list(self.command)
        if extra_packages:
            command.append((
                '--extrapackages',
                ','.join(extra_packages)
            ))
        command.extend((
            '--distribution', self.distro,
            '--create',
        ))
        return call(command)

    def update(self):
        command = list(self.command)
        command.extend((
            '--distribution', self.distro,
            '--update',
        ))
        return call(command)


class PbuilderProvider(Provider):
    def run(self, args):
        rc = 0
        pbuilder_env = PbuilderEnv(distro=args.distro)
        pbuilder_env.create(extra_packages=args.extra_packages)
        if args.scripts:
            rc = pbuilder_env.execute_scripts(args.scripts)
        if args.shell:
            rc = pbuilder_env.start_interactive_shell()
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
        parser.add_argument(
            '--extra-package',
            action='append',
            help='Also install the given package when creating the chroot'
        )
