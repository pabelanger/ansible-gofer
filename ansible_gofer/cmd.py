# Copyright 2015 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import argparse
import logging
import sys

from ansible_gofer import __version__
from ansible_gofer.playbook import Playbook


class Client(object):

    def main(self):
        self.parse_arguments()
        self.setup_logging()
        self.args.func()

    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'playbook')
        parser.add_argument(
            '-i', dest='inventory', default='/etc/ansible/hosts',
            help='specify inventory host file'),
        parser.add_argument(
            '--version', dest='version', action='version', version=__version__,
            help="show program's version number and exit")
        parser.set_defaults(func=self.runner)

        self.args = parser.parse_args()

    def runner(self):
        playbook = Playbook(
            playbook=self.args.playbook,
            inventory=self.args.inventory)
        playbook.run()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)


def main():
    client = Client()
    client.main()
    sys.exit(0)
