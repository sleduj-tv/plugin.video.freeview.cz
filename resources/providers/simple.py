# -*- coding: utf-8 -*-
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
    'fashion':'http://lb.streaming.sk/fashiontv/stream/playlist.m3u8',
    'doktor':'https://live.tvdoktor.sk/high/index.m3u8',
    'szts':'https://dash2.antik.sk/live/tanecnesutaze/index.m3u8',
    'barrandovkrimi':'https://dash2.antik.sk/live/test_barrandov_plus_atk_1200/playlist.m3u8',
    'sporty':'https://dash2.antik.sk/live/sporty_tv/index.m3u8',
    'ok':'https://dash2.antik.sk/live/ok_tv/playlist.m3u8',
    'a11':'https://dash2.antik.sk/live/test_regionalni_tv/playlist.m3u8',
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


