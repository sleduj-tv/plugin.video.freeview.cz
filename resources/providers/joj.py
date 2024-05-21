# -*- coding: utf-8 -*-
# Author: cache-sk
# Created on: 10.10.2019
# License: AGPL v.3 https://www.gnu.org/licenses/agpl-3.0.html

import xbmcgui
import xbmcplugin
import requests.cookies
from bs4 import BeautifulSoup
import re
import random

try:
    from urllib import urlencode
    from urllib import quote
except ImportError:
    from urllib.parse import urlencode
    from urllib.parse import quote

CHANNELS = {
    'joj':{'base':'https://live.joj.sk', 'iframe':'https://media.joj.sk/', 'fget':False, 'with':'joj.m3u8'},
    'plus':{'base':'https://plus.joj.sk/live', 'iframe':'https://media.joj.sk/', 'fget':False, 'with':'plus.m3u8'},
    'wau':{'base':'https://wau.joj.sk/live', 'iframe':'https://media.joj.sk/', 'fget':False, 'with':'wau.m3u8'},
    'family':{'base':'https://jojfamily.blesk.cz/live', 'iframe':'https://media.joj.sk/', 'fget':True},
    'joj24':{'base':'https://joj24.noviny.sk/', 'iframe':'https://media.joj.sk/', 'fget':False, 'with':'joj_news.m3u8'},
    'jojko':{'base':'https://live.joj.sk', 'iframe':'https://media.joj.sk/', 'fget':False, 'replace':'joj.m3u8','with':'jojko.m3u8'},
    'jojcinema':{'base':'https://live.joj.sk', 'iframe':'https://media.joj.sk/', 'fget':False, 'replace':'joj.m3u8','with':'cinema.m3u8'},
    'csfilm':{'base':'https://live.joj.sk', 'iframe':'https://media.joj.sk/', 'fget':False, 'replace':'joj.m3u8','with':'cs_film.m3u8'},
    'cshistory':{'base':'https://live.joj.sk', 'iframe':'https://media.joj.sk/', 'fget':False, 'replace':'joj.m3u8','with':'cs_history.m3u8'},
    'csmystery':{'base':'https://live.joj.sk', 'iframe':'https://media.joj.sk/', 'fget':False, 'replace':'joj.m3u8','with':'cs_mystery.m3u8'},
    'jojsport':{'base':'https://live.joj.sk', 'iframe':'https://media.joj.sk/', 'fget':False, 'replace':'joj.m3u8','with':'joj_sport.m3u8'},
    'iihf1':{'iihf':'https://iihf.worker.tivio.studio/?channelName=sport1'},
    'iihf2':{'iihf':'https://iihf.worker.tivio.studio/?channelName=sport2'}
}

FALLBACK = "https://live.cdn.joj.sk/live/%%?loc=SK&exp=1716281798&hash=9d0862c9645f8f9ffd8736a3e732735333d1b1b665c1a9bf3db84bc8b10c0038"

IIHF = 'https://iihf.worker.tivio.studio/?channelName='

IIHF_HEADERS={
    'accept':'application/json',
    'content-type':'application/json',
    'origin':'https://plus.joj.sk',
    'referer':'https://plus.joj.sk/',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

FGET = "http://p.xf.cz/fget.php?url="

HEADERS={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

def brexit(_addon, _handle, word):
    xbmcgui.Dialog().ok(_addon.getAddonInfo('name'), _addon.getLocalizedString(30105) + word)
    xbmcplugin.setResolvedUrl(_handle, False, xbmcgui.ListItem())
    return False

def getIIHF(uri):
    session = requests.Session()
    response = session.get(uri, headers=IIHF_HEADERS)
    data = response.json()
    if 'sourceUrl' in data:
        return {'url':data['sourceUrl'], 'manifest':'mpd', 'headers':IIHF_HEADERS}
    return None

def findIIHF(html):
    items = html.find_all('div',{"class": "tivio-iihf-player"},True)
    if len(items) == 1:
        print("freeview: joj - iihf found")
        chName = items[0]['channelname']
        return chName
    return None

def playFromPage(_handle, _addon, channel):
    jojsport = channel == 'jojsport'
    channel = CHANNELS[channel]
    if "direct" in channel:
        hls = channel["direct"]
        headers = HEADERS
    elif 'iihf' in channel:
        try:
            iihf = getIIHF(channel['iihf'])
            if iihf is not None:
                return iihf
            else:
                return brexit(_addon, _handle, 'iihf')
        except:
            return brexit(_addon, _handle, 'iihf')
    else:
        session = requests.Session()
        if channel['fget']:
            # temporary
            session.verify = False
        headers = {}
        headers.update(HEADERS)
        if jojsport:
            #another temporary iihf hack
            chsport = None
            response = session.get(CHANNELS['joj']['base'], headers=headers)
            html = BeautifulSoup(response.content, features="html.parser")
            joj = findIIHF(html)
            print("freeview: jojsport - joj is "+str(joj))
            response = session.get(CHANNELS['plus']['base'], headers=headers)
            html = BeautifulSoup(response.content, features="html.parser")
            plus = findIIHF(html)
            print("freeview: jojsport - plus is "+str(plus))
            if joj is None and plus is None:
                # cant detect joj sport, can be sport1 or sport2, use default process
                pass
            elif joj is None:
                if plus == 'sport1':
                    chsport = 'sport2'
                elif plus == 'sport2':
                    chsport = 'sport1'
            elif plus is None:
                if joj == 'sport1':
                    chsport = 'sport2'
                elif joj == 'sport2':
                    chsport = 'sport1'
            else:
                # both sport used, use default process
                pass
            print("freeview: jojsport - should be "+str(chsport))
            if chsport is not None:
                try:
                    iihf = getIIHF(IIHF+chsport)
                    if iihf is not None:
                        return iihf
                except: 
                    pass

        response = session.get(channel['base'], headers=headers)
        html = BeautifulSoup(response.content, features="html.parser")
        
        player = None
        items = html.find_all('iframe',{},True)
        if len(items) > 0:
            for iframe in items:
                if channel['iframe'] in iframe['src']:
                    player = iframe['src']
                    break
        else:
            return brexit(_addon, _handle, 'iframe')

        if player is None:
            print("freeview: joj - player not found")
            if 'replace' not in channel:
                # temporary test iihf
                chName = findIIHF(html)
                if chName is not None:
                    try:
                        iihf = getIIHF(IIHF+chName)
                        if iihf is not None:
                            return iihf
                    except: 
                        pass
            # try fallback
            if 'with' in channel:
                print("freeview: joj - fallback applied")
                hls = FALLBACK.replace("%%", channel['with'])
                headers = {'Referer':channel['iframe'], 'Origin':channel['iframe']}
                headers.update(HEADERS)
                return {'url':hls, 'manifest':'hls', 'headers':headers}
            else:
                return brexit(_addon, _handle, 'iframe')
            
        if channel['fget']:
            #TODO - sooo lazy..
            response = session.get(FGET+quote(player), headers=headers)
        else:
            headers = {'Referer':channel['base']}
            headers.update(HEADERS)
            response = session.get(player, headers=headers)
        
        content = response.content
        try:
            content = content.decode('utf-8')
        except AttributeError:
            pass
        matches = re.search('"hls": "(.*)"', content)
        hls = matches.group(1)
        
        if 'replace' in channel and 'with' in channel:
            hls = hls.replace(channel['replace'], channel['with'])
        
        headers = {'Referer':channel['iframe'], 'Origin':channel['iframe']}
        headers.update(HEADERS)

    return {'url':hls, 'manifest':'hls', 'headers':headers}

def play(_handle, _addon, params):
    channel = params['channel']
    if not channel in CHANNELS:
        raise #TODO

    data = playFromPage(_handle, _addon, channel)
    
    uheaders = urlencode(data['headers'])
    
    li = xbmcgui.ListItem(path=data['url']+'|'+uheaders)
    li.setProperty('inputstreamaddon','inputstream.adaptive') #kodi 18
    li.setProperty('inputstream','inputstream.adaptive') #kodi 19
    li.setProperty('inputstream.adaptive.stream_headers', uheaders)
    li.setProperty('inputstream.adaptive.manifest_headers', uheaders)
    li.setProperty('inputstream.adaptive.manifest_type',data['manifest'])
    xbmcplugin.setResolvedUrl(_handle, True, li)
