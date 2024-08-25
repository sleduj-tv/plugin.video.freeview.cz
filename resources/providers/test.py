# -*- coding: utf-8 -*-
# Author: cache-sk
# Created on: 10.10.2019
# License: AGPL v.3 https://www.gnu.org/licenses/agpl-3.0.html

import xbmcgui
import xbmcplugin

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


CHANNELS = {
    'pcsk':{'mpd':'https://dash2.antik.sk/stream/nvidia_prima_cool/playlist_cbcs.mpd','hls':'http://88.212.15.47/live/test_prima_cool_hd_hevc_50/playlist.m3u8'},
    'jojsvet':{'mpd':'https://dash2.antik.sk/stream/hisi_joj_svet/playlist_cbcs.mpd','hls':'http://88.212.15.47/live/test_joj_svet/playlist.m3u8'},
}

HEADERS={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

def play(_handle, _addon, params):
    channel = params['channel']
    if not channel in CHANNELS:
        raise #TODO

    prefer_mpd = xbmcplugin.getSetting(_handle, 'ockompd') == 'true'

    channel = CHANNELS[channel]

    if prefer_mpd:
        li = xbmcgui.ListItem(path=channel['mpd']+'|'+urlencode(HEADERS))
        li.setProperty('inputstreamaddon','inputstream.adaptive') #kodi 18
        li.setProperty('inputstream','inputstream.adaptive') #kodi 19
        li.setProperty('inputstream.adaptive.manifest_type','mpd')
        xbmcplugin.setResolvedUrl(_handle, True, li)
    else:
        li = xbmcgui.ListItem(path=channel['hls']+'|'+urlencode(HEADERS))
        li.setProperty('inputstreamaddon','inputstream.adaptive') #kodi 18
        li.setProperty('inputstream','inputstream.adaptive') #kodi 19
        li.setProperty('inputstream.adaptive.manifest_type','hls')
        xbmcplugin.setResolvedUrl(_handle, True, li)
