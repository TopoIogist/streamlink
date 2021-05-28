import re

from streamlink.stream import HTTPStream
from streamlink.stream import HLSStream
from streamlink.plugin import Plugin
import datetime

class Trovo(Plugin):
    url_re = re.compile(r"https?://(?:www\.)?trovo\.live/")
    streams_re = re.compile(r'playUrl:"([^"]+)",desc:"([^"]+)"', re.DOTALL)

    @classmethod
    def can_handle_url(cls, url):
        return cls.url_re.match(url) is not None

    def _get_streams(self):
        res = self.session.http.get(self.url)
        self.session.http.headers.update({'Origin': "https://trovo.live"})
        for m in self.streams_re.finditer(res.text):
            if "liveplay.trovo.live" in m.group(1):
                yield m.group(2), HTTPStream(self.session, m.group(1).replace('\\u002F', '/') + "&_f_=" + str(int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)))
            elif "vod.trovo.live" in m.group(1):
                yield m.group(2), HLSStream(self.session, m.group(1).replace('\\u002F', '/') + "&_f_=" + str(int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)))


__plugin__ = Trovo
