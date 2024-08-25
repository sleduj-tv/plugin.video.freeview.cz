# Author: cache-sk
# Created on: 19.12.2021
# License: AGPL v.3 https://www.gnu.org/licenses/agpl-3.0.html

import xbmcgui
import xbmcplugin

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


CHANNELS = {
    'pcsk':'http://88.212.15.47/live/prima_cool_avc_25p/playlist.m3u8',
    'jojsvet':'http://88.212.15.47/live/test_joj_svet/playlist.m3u8',
    'cai':'http://88.212.15.47/live/test_cai_hevc/playlist.m3u8',
    'prima_comedy_central':'https://stream-17.mazana.tv/V2_emn.m3u8s?codec_id=1369&session=prima_comedy_central'
}

HEADERS={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36','referer':'http://live.streaming.sk/'}

def play(_handle, _addon, params):
    channel = params['channel']
    if not channel in CHANNELS:
        raise #TODO

    li = xbmcgui.ListItem(path=CHANNELS[channel]+'|'+urlencode(HEADERS))
    li.setProperty('inputstreamaddon','inputstream.adaptive') #kodi 18
    li.setProperty('inputstream','inputstream.adaptive') #kodi 19
    li.setProperty('inputstream.adaptive.manifest_type','hls')
    xbmcplugin.setResolvedUrl(_handle, True, li)
