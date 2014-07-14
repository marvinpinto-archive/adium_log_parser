import os 
import re
import iso8601
import xml.etree.ElementTree as exml
import xml
import subprocess
import datetime

__all__ = ['AdiumLog']

class Message:
    """
    Cheap container class for all messages
    """

    def __init__(self):
        pass

    def __repr__(self):
        return("%s: %s" % (self.sender, self.text))

class AdiumLog:
    """
    Parses an Adium .chatlog.
    Takes a path to either a .chatlog bundle or older-style
    .chatlog file.
    """
    def __init__(self, path):
        self.path = path

        # in the case we are passed the raw xml
        if re.search('\.xml$', path):
            self.handle = open(path)

        # at some point adium went from using xml files with
        # .chatlog extension to OS X bundles with xml files inside
        if re.search('\.chatlog$', path):
            if os.path.isdir(path):
                basename = os.path.basename(path)
                basename = re.sub(r"chatlog$", "xml", basename, 1)
                xml_path = os.path.join(path, basename)
                if os.path.isfile(xml_path):
                    self.handle = open(xml_path)
            else:
                self.handle = open(path)
                        
        # elementree xml confuses me
        self.root = exml.fromstring(
                            re.sub('xmlns="http://purl.org/net/ulf/ns/0.4-02"', 
                            ' ', 
                            self.handle.read()))

        self.account = self.root.attrib['account']
        self.service = self.root.attrib['service']
        self.messages = []

        for logmsg in self.root.findall('message'):
            msg = Message()
            tags = [exml.tostring(i, encoding="UTF-8", method="html") 
                        for i in list(logmsg)]
            msg.html = "".join(tags)
            msg.text = "".join(logmsg.itertext())
            msg.time = iso8601.parse_date(logmsg.attrib['time'])
            msg.sender = logmsg.attrib['sender']
            self.messages.append(msg)

