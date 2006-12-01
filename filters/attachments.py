#!/usr/bin/python
# attachments -- Courier filter which blocks specified attachment types
# Copyright (C) 2004  Robert Penz <robert@penz.name>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import sys
import re
import email.Utils


blockedPattern = re.compile(r'^.*\.(scr|exe|com|bat|pif|lnk|sys|mid|vb|js|ws|shs|ceo|cmd|cpl|hta|vbs)$', re.I)

# Record in the system log that this filter was initialized.
sys.stderr.write('Initialized the "attachments" python filter\n')


def doFilter(bodyFile, controlFileList):
    try:
        msg = email.message_from_file(open(bodyFile))
    except Exception, e:
        return "554 " + str(e)

    for part in msg.walk():
        # multipart/* are just containers
        if part.get_content_maintype() == 'multipart':
            continue

        filename = part.get_filename()
        if not filename:
            # Check the "name" parameter
            rawname = part.get_param('name')
            try:
                filename = email.Utils.collapse_rfc2231_value(rawname)
            except:
                pass

        if filename and blockedPattern.match(filename):
            return "554 The extension of the attached file is blacklisted"

    # nothing found --> to the next filter
    return ''


if __name__ == '__main__':
    # For debugging, you can create a file that contains a message
    # body, possibly including attachments.
    # Run this script with the name of that file as an argument,
    # and it'll print either a permanent failure code to indicate
    # that the message would be rejected, or print nothing to
    # indicate that the remaining filters would be run.
    if len(sys.argv) != 2:
        print "Usage: attachments.py <message_body_file>"
        sys.exit(0)
    print doFilter(sys.argv[1], [])
