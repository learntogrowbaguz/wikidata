#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2024 emijrp <emijrp@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random
import re
import string
import sys
import time
import urllib.parse

import pywikibot
from pywikibot import pagegenerators
from wikidatafun import *

def main():
    sitewp = pywikibot.Site('en', 'wikipedia')
    sitecommons = pywikibot.Site('commons', 'commons')
    sitewd = pywikibot.Site('wikidata', 'wikidata')
    repowd = sitewd.data_repository()
    randomstart = ''.join(random.choice("!¡()" + string.ascii_letters + string.digits) for xx in range(4))
    randomstart = randomstart[0].upper() + randomstart[1:]
    gen = pagegenerators.AllpagesPageGenerator(site=sitewp, start=randomstart, namespace=0, includeredirects=False, content=True)
    pre = pagegenerators.PreloadingGenerator(gen, groupsize=50)
    for page in pre:
        if page.isRedirectPage():
            continue
        #print("==", page.title().encode('utf-8'), "==")
        wtitle = page.title()
        wtext = page.text
        #print(wtext)
        
        """
        tiene buena pinta pero algun error puede generar, revisar
        #mode1 filename compared to page title
        m = re.findall(r"(?im)\[\[\s*(?:File|Image)\s*:\s*([^\|\[\]]+?)\|", wtext)
        m = list(set(m))
        for mm in m:
            if len(mm) < 8 or not re.search(r"(?im)\.(jpe?g|gif|png|tiff?)", mm):
                continue
            if len(wtitle) < 8 or not " " in wtitle or re.search(r"(?im)[^a-záéíóúàèìòùäëïöüçñ\,\.\-\_ ]", wtitle):
                continue
            filename = "File:"+mm.strip()
            #cuidado al comparar, q si soy demasiado flexible con los simbolos (numeros por ej), puede salir como positivo cosas diferentes
            symbols = "[0-9\-\.\,\!\¡\"\$\&\(\)\*\?\¿\~\@\= ]*?"
            wtitlex = wtitle.replace(".", " ").replace(",", " ").replace("-", " ").replace("(", " ").replace(")", " ").replace("_", " ")
            wtitlex = wtitlex.replace(" ", symbols)
            titleregexp = r"(?im)^File:%s(%s|%s)%s\.(?:jpe?g|gif|png|tiff?)$" % (symbols, wtitle, wtitlex, symbols)
            regexpmonths = "(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|apr|jun|jul|aug|sept?|oct|nov|dec)"
            regexpdays = "(([012]?\d|3[01])(st|nd|rd|th))"
            filenameclean = re.sub(r"(?im)\b(cropp?e?d?|rotated?|portrait|before|after|cut|sir|prince|dr|in|on|at|en|circa|c|rev|img|imagen?|pic|picture|photo|photograph|foto|fotograf[íi]a|the|[a-z]+\d+|\d+[a-z]+|%s|%s)\b" % (regexpdays, regexpmonths), "", filename)
            #print(titleregexp, filenameclean)
            if re.search(titleregexp, filenameclean):
                print(page.full_url(), filename)
        
        continue
        """
        
        #mode2 linked thumb descriptions
        m = re.findall(r"(?im)\[\[\s*(?:File|Image)\s*:\s*([^\|\[\]]+?)(?:\|\s*(?:thumb|thumbnail|frame|center|right|left|upright|upleft|\d+px)\s*)*\s*\|\s*(?:(?:The|Oldtown of))?\s*\'*\[\[([^\|\[\]\#]+?)(?:\|[\|\[\]\#]*?)?\]\]\'*\s*(?:(?:in|on|at) (?:\[?\[?(?:\d+|night|sunset|sunrise|spring|summer|autumn|winter)\]?\]?|skyline|\(\d+\)))?\s*\.?\s*\]\]", wtext)
        for mm in m:
            filename = mm[0].strip()
            thumblink = mm[1].split("|")[0].strip()
            print(filename, thumblink)
            filepagewp = pywikibot.Page(sitewp, "File:"+filename)
            if filepagewp.exists():
                print("Existe pagina para este fichero en wp, saltamos")
                continue
            filepagecommons = pywikibot.Page(sitecommons, "File:"+filename)
            if not filepagecommons.exists():
                print("No existe pagina para este fichero en commons, saltamos")
                continue
            if filepagecommons.isRedirectPage():
                filepagecommons = filepagecommons.getRedirectTarget()
            thumblinkwp = pywikibot.Page(sitewp, thumblink)
            if not thumblinkwp.exists():
                print("No existe pagina para este thumblink en wp, saltamos")
                continue
            if thumblinkwp.isRedirectPage():
                thumblinkwp = thumblinkwp.getRedirectTarget()
            item = ''
            try:
                item = pywikibot.ItemPage.fromPage(thumblinkwp)
            except:
                pass
            if not item:
                print("No se encontro item asociado, saltamos")
                continue
            q = item.title()
            print(", ".join([filename, thumblinkwp.title(), item.title()]))
            print(filepagecommons.full_url())
            mid = "M" + str(filepagecommons.pageid)
            print(mid)
            
            claims = getClaimsFromCommonsFile(site=sitecommons, mid=mid)
            if not claims:
                print("Error al recuperar claims, saltamos")
                continue
            elif claims and "claims" in claims and claims["claims"] == { }:
                print("No tiene claims, no inicializado, inicializamos")
            
            if "claims" in claims:
                if "P180" in claims["claims"]: #p180 depicts
                    print("Ya tiene claim depicts, saltamos")
                    continue
                else:
                    claimstoadd = []
                    comments = []
                    depictsclaim = """{ "mainsnak": { "snaktype": "value", "property": "P180", "datavalue": {"value": {"entity-type": "item", "numeric-id": "%s", "id": "%s"}, "type":"wikibase-entityid"} }, "type": "statement", "rank": "preferred" }""" % (q[1:], q)
                    claimstoadd.append(depictsclaim)
                    comments.append("depicts")
                    
                    if claimstoadd and comments and len(claimstoadd) == len(comments):
                        overwritecomment = "BOT - Adding [[Commons:Structured data|structured data]] based on Wikipedia pages [[:en:%s|%s]]/[[:en:%s|%s]] and Wikidata item [[:d:%s|%s]]: %s" % (page.title(), page.title(), thumblinkwp.title(), thumblinkwp.title(), q, q, ", ".join(comments)),
                        addClaimsToCommonsFile(site=sitecommons, mid=mid, claims=claimstoadd, overwritecomment=overwritecomment, q=q)
                    else:
                        print("No se encontraron claims para anadir")
                        continue

if __name__ == '__main__':
    main()
