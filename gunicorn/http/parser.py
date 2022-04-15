# -*- coding: utf-8 -
#
# This file is part of gunicorn released under the MIT license.
# See the NOTICE for more information.
from typing import Any

from gunicorn.http.message import Request
from gunicorn.http.unreader import SocketUnreader, IterUnreader


class Parser(object):

    # gunicorn-note: 默认为 Request 类
    mesg_class: Request.__class__ = None

    def __init__(self, cfg, source, source_addr):
        self.cfg = cfg
        if hasattr(source, "recv"):
            self.unreader = SocketUnreader(source)
        else:
            self.unreader = IterUnreader(source)
        self.mesg: Request = None
        self.source_addr = source_addr

        # request counter (for keepalive connetions)
        self.req_count = 0

    def __iter__(self):
        return self

    def __next__(self):
        # Stop if HTTP dictates a stop.
        if self.mesg and self.mesg.should_close():
            raise StopIteration()

        # Discard any unread body of the previous message
        # gunicorn-note: 默认 self.mesg 是Request的实例
        if self.mesg:
            # gunicorn-note: read 会调用 SocketUnreader 的 chunk 方法，进行socket recv
            data = self.mesg.body.read(8192)
            while data:
                data = self.mesg.body.read(8192)

        # Parse the next request
        self.req_count += 1
        self.mesg = self.mesg_class(self.cfg, self.unreader, self.source_addr, self.req_count)
        if not self.mesg:
            raise StopIteration()
        return self.mesg

    next = __next__


class RequestParser(Parser):

    mesg_class = Request
