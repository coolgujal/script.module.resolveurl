'''
    Plugin for ResolveUrl
    Copyright (C) 2019 gujal

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import re
from resolveurl.plugins.lib import helpers
from resolveurl import common
from resolveurl.resolver import ResolveUrl, ResolverError


class VeryStreamResolver(ResolveUrl):
    name = "verystream"
    domains = ["verystream.com", "verystream.xyz", "woof.tube"]
    pattern = r'(?://|\.)((?:verystream|woof)\.(?:com|xyz|tube))/(?:stream|e|source)/([a-zA-Z0-9]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.FF_USER_AGENT, 'Referer': 'https://verystream.com/'}
        html = self.net.http_GET(web_url, headers=headers).content
        regex = '(%s~[~.:a-zA-Z0-9]+)' % media_id
        r = re.search(regex, html)
        if r:
            source = 'https://verystream.com/gettoken/{0}?mime=true'.format(r.group(1))
            headers.update({'Referer': web_url})
            return source + helpers.append_headers(headers)

        raise ResolverError("Could not locate video")

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, 'https://verystream.com/e/{media_id}')
