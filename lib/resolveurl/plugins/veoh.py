"""
    Plugin for ResolveUrl
    Copyright (C) 2011 anilkuj
    Copyright (C) 2019 cache-sk

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

import json
from resolveurl.plugins.lib import helpers
from resolveurl import common
from resolveurl.resolver import ResolveUrl, ResolverError


class VeohResolver(ResolveUrl):
    name = "veoh"
    domains = ["veoh.com"]
    pattern = r'(?://|\.)(veoh\.com)/(?:watch/|.+?permalinkId=)?([0-9a-zA-Z/]+)'

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.CHROME_USER_AGENT, 'Referer': web_url}
        html = self.net.http_GET(web_url, headers=headers).content
        _data = json.loads(html)
        if 'video' in _data and 'src' in _data['video']:
            sources = []
            _src = _data['video']['src']
            if 'HQ' in _src:
                sources.append((720, _src['HQ']))
            if 'Regular' in _src:
                sources.append((480, _src['Regular']))

            if len(sources) > 0:
                return helpers.pick_source(sources) + helpers.append_headers(headers)

        raise ResolverError('Unable to locate video')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://www.{host}/watch/getVideo/{media_id}')
