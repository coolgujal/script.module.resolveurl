"""
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
"""

import json
from resolveurl.plugins.lib import helpers
from resolveurl import common
from resolveurl.resolver import ResolveUrl, ResolverError


class XStreamCDNResolver(ResolveUrl):
    name = 'XStreamCDN'
    domains = ["xstreamcdn.com", "gcloud.live", "there.to", "animeproxy.info", "myvidis.top"]
    pattern = r'(?://|\.)((?:xstreamcdn\.com|gcloud\.live|there\.to|animeproxy\.info|myvidis\.top))/v/([\w-]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.RAND_UA,
                   'Referer': web_url,
                   'X-Requested-With': 'XMLHttpRequest'}

        r = self.net.http_POST(web_url,
                               form_data={'r': '', 'd': 'xstreamcdn.com'},
                               headers=headers
                               )

        jsonData = json.loads(r.content)
        if jsonData:
            sources = [(item.get('label', 'mp4'), item['file']) for item in jsonData['data']]
            return helpers.pick_source(sources) + helpers.append_headers(headers)

        raise ResolverError('Unable to locate video')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://{host}/api/source/{media_id}')
