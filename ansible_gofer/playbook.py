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

import logging
import sys

from ansible import utils

from ansible import callbacks
from ansible.playbook import PlayBook

LOG = logging.getLogger(__file__)


class Playbook(object):

    def __init__(self, playbook, inventory):
        self.host_list = inventory
        self.playbook = playbook

    def run(self):
        # First pass of our playbook.
        self._run()
        # Second pass to ensure playbook is idempotent.
        results = self._run()

        LOG.info('Results')
        for host, stats in results.iteritems():
            LOG.info('%s: ok=%s | changed=%s | unreachable=%s | failed=%s' % (
                host, stats['ok'], stats['changed'], stats['unreachable'],
                stats['failures']))
            if stats['changed'] != 0:
                LOG.error('Playbook is not idempotent!')
                sys.exit(1)

    def _run(self):
        stats = callbacks.AggregateStats()
        playbook_callbacks = callbacks.PlaybookCallbacks(
            verbose=utils.VERBOSITY)
        runner_callbacks = callbacks.PlaybookRunnerCallbacks(
            stats, verbose=utils.VERBOSITY)

        playbook = PlayBook(
            callbacks=playbook_callbacks,
            any_errors_fatal=True,
            host_list=self.host_list,
            playbook=self.playbook,
            runner_callbacks=runner_callbacks,
            stats=stats)

        results = playbook.run()
        return results
