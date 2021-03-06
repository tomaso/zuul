# Copyright 2013 Rackspace Australia
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import voluptuous as v

from zuul.reporter import BaseReporter


class SMTPReporter(BaseReporter):
    """Sends off reports to emails via SMTP."""

    name = 'smtp'
    log = logging.getLogger("zuul.reporter.smtp.Reporter")

    def report(self, source, pipeline, item, message=None):
        """Send the compiled report message via smtp."""
        if not message:
            message = self._formatItemReport(pipeline, item)

        self.log.debug("Report change %s, params %s, message: %s" %
                       (item.change, self.reporter_config, message))

        from_email = self.reporter_config['from'] \
            if 'from' in self.reporter_config else None
        to_email = self.reporter_config['to'] \
            if 'to' in self.reporter_config else None

        if 'subject' in self.reporter_config:
            subject = self.reporter_config['subject'].format(
                change=item.change)
        else:
            subject = "Report for change %s" % item.change

        self.connection.sendMail(subject, message, from_email, to_email)


def getSchema():
    smtp_reporter = v.Schema({
        'connection': str,
        'to': str,
        'from': str,
        'subject': str,
    })
    return smtp_reporter
