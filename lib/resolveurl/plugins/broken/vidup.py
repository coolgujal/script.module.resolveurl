"""
    Plugin for ResolveURL
    Copyright (C) 2020 gujal

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
"""
import re
from six.moves import urllib_error, urllib_parse
from resolveurl import common
from resolveurl.plugins.lib import helpers
from resolveurl.resolver import ResolveUrl, ResolverError


class VidUpResolver(ResolveUrl):
    name = "vidup.io"
    domains = ["vidup.tv", "vidup.io", "vidop.icu"]
    pattern = r'(?://|\.)(vid[ou]p\.(?:tv|io|icu))/(?:embed-|download/|embed/)?([0-9a-zA-Z]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'Referer': web_url, 'User-Agent': common.CHROME_USER_AGENT}
        html = self.net.http_GET(web_url, headers=headers).content
        sources = helpers.parse_sources_list(html)
        if sources:
            try:
                token = re.search(r'''var thief\s*=\s*["']([^"']+)''', html)
                if token:
                    vt_url = 'http://vidop.icu/jwv/%s' % token.group(1)
                    vt_html = self.net.http_GET(vt_url, headers=headers).content
                    vt = re.search(r'''\|([-\w]{50,})''', vt_html)
                    if vt:
                        sources = helpers.sort_sources_list(sources)
                        params = {'direct': 'false', 'ua': 1, 'vt': vt.group(1)}
                        return helpers.pick_source(sources) + '?' + urllib_parse.urlencode(params) + helpers.append_headers(headers)
                    else:
                        raise ResolverError('Video VT Missing')
                else:
                    raise ResolverError('Video Token Missing')
            except urllib_error.HTTPError:
                raise ResolverError('Unable to read page data')

        raise ResolverError('Unable to locate video')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://vidop.icu/embed/{media_id}')
