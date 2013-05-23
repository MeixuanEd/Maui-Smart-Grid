#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'

import smtplib
from datetime import datetime
from mecoconfig import MECOConfiger
import sys
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email import Encoders


class MECONotifier(object):
    """
    Notification services for MECO data processing.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.config = MECOConfiger()

    def sendNotificationEmail(self, msgBody):
        """
        :param msgBody: The body of the message to be sent.
        :returns: True for success, False for an error.
        """

        errorOccurred = False
        user = self.config.configOptionValue('Notifications', 'email_username')
        password = self.config.configOptionValue('Notifications',
                                                 'email_password')
        fromaddr = self.config.configOptionValue('Notifications',
                                                 'email_fromaddr')
        toaddr = self.config.configOptionValue('Notifications',
                                               'email_recipients')
        server = smtplib.SMTP(
            self.config.configOptionValue('Notifications', 'email_smtp_server'))

        try:
            server.starttls()
        except smtplib.SMTPException, e:
            errorOccurred = True
            print "Exception = %s" % e

        try:
            server.login(user, password)
        except smtplib.SMTPException, e:
            errorOccurred = True
            print "Exception = %s" % e

        senddate = datetime.strftime(datetime.now(), '%Y-%m-%d')
        subject = "HISEP Notification"

        msgHeader = "Date: %s\r\nFrom: %s\r\nTo: %s\r\nSubject: " \
                    "%s\r\nX-Mailer: " \
                    "My-Mail\r\n\r\n" % (
                        senddate, fromaddr, toaddr, subject)

        msgBody = "This is a message from the Hawaii Smart Energy Project " \
                  "MECO Project notification system.\n\n" + msgBody

        msgBody += '\nThis email account is not monitored so don\'t send ' \
                   'messages to it with the expectation of a reply.'

        msgBody += '\n\nYou are receiving this message because you are on the' \
                   ' recipient list for notifications for the Hawaii Smart ' \
                   'Energy Project.'

        try:
            sys.stderr.write("Sending email notifications.\n")
            server.sendmail(fromaddr, toaddr, msgHeader + msgBody)
            server.quit()
        except smtplib.SMTPException, e:
            errorOccurred = True
            print "Exception = %s" % e

        return errorOccurred != True

    def sendMailWithAttachments(self, msgBody, files = []):
        """
        Send email along with attachments.

        :param msgBody
        :param files: List of file paths.
        :returns: True if no exceptions are raised.
        """

        sys.stderr.write("Sending multipart email.\n")

        errorOccurred = False
        assert type(files) == list

        user = self.config.configOptionValue('Notifications', 'email_username')
        password = self.config.configOptionValue('Notifications',
                                                 'email_password')

        send_to = self.config.configOptionValue('Notifications',
                                                'email_recipients')
        send_from = self.config.configOptionValue('Notifications',
                                                  'email_fromaddr')

        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = send_to
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = "HISEP Notification"

        msg.attach(MIMEText(msgBody))

        for f in files:
            sys.stderr.write("Attaching file %s.\n" % f)
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(f, "rb").read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="%s"' % os.path.basename(f))
            msg.attach(part)

        server = smtplib.SMTP(
            self.config.configOptionValue('Notifications', 'email_smtp_server'))
        try:
            server.starttls()
        except smtplib.SMTPException, e:
            errorOccurred = True
            print "Exception = %s" % e

        try:
            server.login(user, password)
        except smtplib.SMTPException, e:
            errorOccurred = True
            print "Exception = %s" % e

        server.sendmail(send_from, send_to, msg.as_string())
        server.quit()

        if errorOccurred == False:
            sys.stderr.write('No exceptions occurred.\n')

        return errorOccurred
