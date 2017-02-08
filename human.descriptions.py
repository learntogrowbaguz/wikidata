#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2017 emijrp <emijrp@gmail.com>
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

import re
import sys

import pwb
import pywikibot
from quickstatements import *

def main():
    targetlangs = ['es', 'ca', 'gl']
    site = pywikibot.Site('wikidata', 'wikidata')
    repo = site.data_repository()
    
    genders = {
        'Q6581097': 'male', 
        'Q6581072': 'female', 
    }
    
    #ca: https://ca.wikipedia.org/wiki/Llista_de_gentilicis#Llista_de_gentilicis_per_estat
    #en: https://en.wikipedia.org/wiki/List_of_adjectival_and_demonymic_forms_for_countries_and_nations
    #es: https://es.wikipedia.org/wiki/Anexo:Gentilicios
    #gl: https://web.archive.org/web/20060512203621/http://www.galegoenlinna.uvigo.es/fichasVer.asp?idFicha=132
    translationsNationalities = {
        'Afghan': {
            'ca': { 'male': 'afganès', 'female': 'afganesa' },
            'en': { 'male': 'Afghan', 'female': 'Afghan' }, 
            'es': { 'male': 'afgano', 'female': 'afgana' }, 
            'gl': { 'male': 'afgán', 'female': 'afgá' }, 
        },
        'Albanian': {
            'ca': { 'male': 'albanès', 'female': 'albanesa' },
            'en': { 'male': 'Albanian', 'female': 'Albanian' }, 
            'es': { 'male': 'albanés', 'female': 'albanesa' }, 
            'gl': { 'male': 'albanés', 'female': 'albanesa' }, 
        },
        'Algerian': {
            'ca': { 'male': 'algerià', 'female': 'algeriana' },
            'en': { 'male': 'Algerian', 'female': 'Algerian' }, 
            'es': { 'male': 'argelino', 'female': 'argelina' }, 
            'gl': { 'male': 'alxeriano', 'female': 'alxeriana' }, 
        },
        'Andorran': {
            'ca': { 'male': 'andorrà', 'female': 'andorrana' },
            'en': { 'male': 'Andorran', 'female': 'Andorran' }, 
            'es': { 'male': 'andorrano', 'female': 'andorrana' }, 
            'gl': { 'male': 'andorrano', 'female': 'andorrana' }, 
        },
        'Angolan': {
            'ca': { 'male': 'angolès', 'female': 'angolesa' },
            'en': { 'male': 'Angolan', 'female': 'Angolan' }, 
            'es': { 'male': 'angoleño', 'female': 'angoleña' }, 
            'gl': { 'male': 'angolano', 'female': 'angolana' }, 
        },
        'Argentine': {
            'ca': { 'male': 'argentí', 'female': 'argentina' },
            'en': { 'male': 'Argentine', 'female': 'Argentine' }, 
            'es': { 'male': 'argentino', 'female': 'argentina' }, 
            'gl': { 'male': 'arxentino', 'female': 'arxentina' }, 
        },
        'Argentinean': {
            'ca': { 'male': 'argentí', 'female': 'argentina' },
            'en': { 'male': 'Argentinean', 'female': 'Argentinean' }, 
            'es': { 'male': 'argentino', 'female': 'argentina' }, 
            'gl': { 'male': 'arxentino', 'female': 'arxentina' }, 
        },
        'Armenian': {
            'ca': { 'male': 'armeni', 'female': 'armènia' },
            'en': { 'male': 'Armenian', 'female': 'Armenian' }, 
            'es': { 'male': 'armenio', 'female': 'armenia' }, 
            'gl': { 'male': 'armenio', 'female': 'armenia' }, 
        },
        'Argentinian': {
            'ca': { 'male': 'argentí', 'female': 'argentina' },
            'en': { 'male': 'Argentinian', 'female': 'Argentinian' }, 
            'es': { 'male': 'argentino', 'female': 'argentina' }, 
            'gl': { 'male': 'arxentino', 'female': 'arxentina' }, 
        },
        'Australian': {
            'ca': { 'male': 'australià', 'female': 'australiana' },
            'en': { 'male': 'Australian', 'female': 'Australian' }, 
            'es': { 'male': 'australiano', 'female': 'australiana' }, 
            'gl': { 'male': 'australiano', 'female': 'australiana' }, 
        },
        'Austrian': {
            'ca': { 'male': 'austríac', 'female': 'austríaca' },
            'en': { 'male': 'Austrian', 'female': 'Austrian' }, 
            'es': { 'male': 'austríaco', 'female': 'austríaca' }, 
            'gl': { 'male': 'austríaco', 'female': 'austríaca' }, 
        },
        'Azerbaijani': {
            'ca': { 'male': 'azerbaidjanès', 'female': 'azerbaidjanesa' },
            'en': { 'male': 'Azerbaijani', 'female': 'Azerbaijani' }, 
            'es': { 'male': 'azerbaiyano', 'female': 'azerbaiyana' }, 
            'gl': { 'male': 'acerbaixano', 'female': 'acerbaixana' }, 
        },
        'Bahamian': {
            'ca': { 'male': 'bahamià', 'female': 'bahamiana' },
            'en': { 'male': 'Bahamian', 'female': 'Bahamian' }, 
            'es': { 'male': 'bahameño', 'female': 'bahameña' }, 
            'gl': { 'male': 'bahameño', 'female': 'bahameña' }, 
        },
        'Bahraini': {
            'ca': { 'male': 'bahrenià', 'female': 'bahreniana' },
            'en': { 'male': 'Bahraini', 'female': 'Bahraini' }, 
            'es': { 'male': 'bareiní', 'female': 'bareiní' }, 
            'gl': { 'male': 'bahrainí', 'female': 'bahrainí' }, 
        },
        'Bangladeshi': {
            'ca': { 'male': 'bangladeshià', 'female': 'bangladeshiana' },
            'en': { 'male': 'Bangladeshi', 'female': 'Bangladeshi' }, 
            'es': { 'male': 'bangladesí', 'female': 'bangladesí' }, 
            'gl': { 'male': 'bangladesí', 'female': 'bangladesí' }, 
        },
        'Barbadian': {
            'ca': { 'male': 'barbadià', 'female': 'barbadiana' },
            'en': { 'male': 'Barbadian', 'female': 'Barbadian' }, 
            'es': { 'male': 'barbadense', 'female': 'barbadense' }, 
            'gl': { 'male': 'barbadense', 'female': 'barbadense' }, 
        },
        'Belarusian': {
            'ca': { 'male': 'bielorús', 'female': 'bielorussa' },
            'en': { 'male': 'Belarusian', 'female': 'Belarusian' }, 
            'es': { 'male': 'bielorruso', 'female': 'bielorrusa' }, 
            'gl': { 'male': 'bielorruso', 'female': 'bielorrusa' }, 
        },
        'Belgian': {
            'ca': { 'male': 'belga', 'female': 'belga' },
            'en': { 'male': 'Belgian', 'female': 'Belgian' }, 
            'es': { 'male': 'belga', 'female': 'belga' }, 
            'gl': { 'male': 'belga', 'female': 'belga' }, 
        },
        'Belizean': {
            'ca': { 'male': 'belizià', 'female': 'beliziana' },
            'en': { 'male': 'Belizean', 'female': 'Belizean' }, 
            'es': { 'male': 'beliceño', 'female': 'beliceña' }, 
            'gl': { 'male': 'belizense', 'female': 'belizense' }, 
        },
        'Beninese': {
            'ca': { 'male': 'beninès', 'female': 'beninesa' },
            'en': { 'male': 'Beninese', 'female': 'Beninese' }, 
            'es': { 'male': 'beninés', 'female': 'beninesa' }, 
            'gl': { 'male': 'beninés', 'female': 'beninesa' }, 
        },
        'Beninois': {
            'ca': { 'male': 'beninès', 'female': 'beninesa' },
            'en': { 'male': 'Beninois', 'female': 'Beninois' }, 
            'es': { 'male': 'beninés', 'female': 'beninesa' }, 
            'gl': { 'male': 'beninés', 'female': 'beninesa' }, 
        },
        'Bermudan': {
            'ca': { 'male': 'de Bermudes', 'female': 'de Bermudes' },
            'en': { 'male': 'Bermudan', 'female': 'Bermudan' }, 
            'es': { 'male': 'bermudeño', 'female': 'bermudeño' }, 
            'gl': { 'male': 'bermudano', 'female': 'bermudana' }, 
        },
        'Bermudian': {
            'ca': { 'male': 'de Bermudes', 'female': 'de Bermudes' },
            'en': { 'male': 'Bermudan', 'female': 'Bermudan' }, 
            'es': { 'male': 'bermudeño', 'female': 'bermudeño' }, 
            'gl': { 'male': 'bermudano', 'female': 'bermudana' }, 
        },
        'Bhutanese': {
            'ca': { 'male': 'bhutanès', 'female': 'bhutanesa' },
            'en': { 'male': 'Bhutanese', 'female': 'Bhutanese' }, 
            'es': { 'male': 'butanés', 'female': 'butanesa' }, 
            'gl': { 'male': 'butanés', 'female': 'butanesa' }, 
        },
        'Bissau-Guinean': {
            'ca': { 'male': 'guineà', 'female': 'guineana' },
            'en': { 'male': 'Bissau-Guinean', 'female': 'Bissau-Guinean' }, 
            'es': { 'male': 'guineano', 'female': 'guineana' }, 
            'gl': { 'male': 'guineano', 'female': 'guineana' }, 
        },
        'Bolivian': {
            'ca': { 'male': 'bolivià', 'female': 'boliviana' },
            'en': { 'male': 'Bolivian', 'female': 'Bolivian' }, 
            'es': { 'male': 'boliviano', 'female': 'boliviana' }, 
            'gl': { 'male': 'boliviano', 'female': 'boliviana' }, 
        },
        'Bosnian': {
            'ca': { 'male': 'bosnià', 'female': 'bosniana' },
            'en': { 'male': 'Bosnian', 'female': 'Bosnian' }, 
            'es': { 'male': 'bosnio', 'female': 'bosnia' }, 
            'gl': { 'male': 'bosníaco', 'female': 'bosníaca' }, 
        },
        'Botswanan': {
            'ca': { 'male': 'botswanès', 'female': 'botswanesa' },
            'en': { 'male': 'Botswanan', 'female': 'Botswanan' }, 
            'es': { 'male': 'botsuano', 'female': 'botsuana' }, 
            'gl': { 'male': 'botswaniano', 'female': 'botswaniana' }, 
        },
        'Brazilian': {
            'ca': { 'male': 'brasiler', 'female': 'brasilera' },
            'en': { 'male': 'Brazilian', 'female': 'Brazilian' }, 
            'es': { 'male': 'brasileño', 'female': 'brasileña' }, 
            'gl': { 'male': 'brasileiro', 'female': 'brasileira' }, 
        },
        'Bruneian': {
            'ca': { 'male': 'bruneiès', 'female': 'bruneiesa' },
            'en': { 'male': 'Bruneian', 'female': 'Bruneian' }, 
            'es': { 'male': 'bruneano', 'female': 'bruneana' }, 
            'gl': { 'male': 'bruneano', 'female': 'bruneana' }, 
        },
        'Bulgarian': {
            'ca': { 'male': 'búlgar', 'female': 'búlgara' },
            'en': { 'male': 'Bulgarian', 'female': 'Bulgarian' }, 
            'es': { 'male': 'búlgaro', 'female': 'búlgara' }, 
            'gl': { 'male': 'búlgaro', 'female': 'búlgara' }, 
        },
        'Burkinabe': {
            'ca': { 'male': 'burkinès', 'female': 'burkinesa' },
            'en': { 'male': 'Burkinabe', 'female': 'Burkinabe' }, 
            'es': { 'male': 'burkinés', 'female': 'burkinesa' }, 
            'gl': { 'male': 'burkinense', 'female': 'burkinense' }, 
        },
        'Burkinabé': {
            'ca': { 'male': 'burkinès', 'female': 'burkinesa' },
            'en': { 'male': 'Burkinabé', 'female': 'Burkinabé' }, 
            'es': { 'male': 'burkinés', 'female': 'burkinesa' }, 
            'gl': { 'male': 'burkinense', 'female': 'burkinense' }, 
        },
        'Burmese': {
            'ca': { 'male': 'birmà', 'female': 'birmana' },
            'en': { 'male': 'Burmese', 'female': 'Burmese' }, 
            'es': { 'male': 'birmano', 'female': 'birmana' }, 
            'gl': { 'male': 'birmano', 'female': 'birmana' }, 
        },
        'Burundian': {
            'ca': { 'male': 'burundès', 'female': 'burundesa' },
            'en': { 'male': 'Burundian', 'female': 'Burundian' }, 
            'es': { 'male': 'burundés', 'female': 'burundesa' }, 
            'gl': { 'male': 'burundiano', 'female': 'burundiana' }, 
        },
        'Cabo Verdean': {
            'ca': { 'male': 'capverdià', 'female': 'capverdiana' },
            'en': { 'male': 'Cabo Verdean', 'female': 'Cabo Verdean' }, 
            'es': { 'male': 'caboverdiano', 'female': 'caboverdiana' }, 
            'gl': { 'male': 'caboverdiano', 'female': 'caboverdiana' }, 
        },
        'Cambodian': {
            'ca': { 'male': 'cambodjà', 'female': 'cambodjana' },
            'en': { 'male': 'Cambodian', 'female': 'Cambodian' }, 
            'es': { 'male': 'camboyano', 'female': 'camboyana' }, 
            'gl': { 'male': 'camboxano', 'female': 'camboxana' }, 
        },
        'Cameroonian': {
            'ca': { 'male': 'camerunès', 'female': 'camerunesa' },
            'en': { 'male': 'Cameroonian', 'female': 'Cameroonian' }, 
            'es': { 'male': 'camerunés', 'female': 'camerunesa' }, 
            'gl': { 'male': 'camerunés', 'female': 'camerunesa' }, 
        },
        'Canadian': {
            'ca': { 'male': 'canadenc', 'female': 'canadenca' },
            'en': { 'male': 'Canadian', 'female': 'Canadian' }, 
            'es': { 'male': 'canadiense', 'female': 'canadiense' }, 
            'gl': { 'male': 'canadense', 'female': 'canadense' }, 
        },
        'Chadian': {
            'ca': { 'male': 'txadià', 'female': 'txadiana' },
            'en': { 'male': 'Chadian', 'female': 'Chadian' }, 
            'es': { 'male': 'chadiano', 'female': 'chadiana' }, 
            'gl': { 'male': 'chadiano', 'female': 'chadiana' }, 
        },
        'Chilean': {
            'ca': { 'male': 'xilè', 'female': 'xilena' },
            'en': { 'male': 'Chilean', 'female': 'Chilean' }, 
            'es': { 'male': 'chileno', 'female': 'chilena' }, 
            'gl': { 'male': 'chileno', 'female': 'chilena' }, 
        },
        'Chinese': {
            'ca': { 'male': 'xinès', 'female': 'xinesa' },
            'en': { 'male': 'Chinese', 'female': 'Chinese' }, 
            'es': { 'male': 'chino', 'female': 'china' }, 
            'gl': { 'male': 'chinés', 'female': 'chinesa' }, 
        },
        'Colombian': {
            'ca': { 'male': 'colombià', 'female': 'colombiana' },
            'en': { 'male': 'Colombian', 'female': 'Colombian' }, 
            'es': { 'male': 'colombiano', 'female': 'colombiana' }, 
            'gl': { 'male': 'colombiano', 'female': 'colombiana' }, 
        },
        'Comoran': {
            'ca': { 'male': 'comorià', 'female': 'comoriana' },
            'en': { 'male': 'Comoran', 'female': 'Comoran' }, 
            'es': { 'male': 'comorense', 'female': 'comorense' }, 
            'gl': { 'male': 'comoriano', 'female': 'comoriana' }, 
        },
        'Comorian': {
            'ca': { 'male': 'comorià', 'female': 'comoriana' },
            'en': { 'male': 'Comorian', 'female': 'Comorian' }, 
            'es': { 'male': 'comorense', 'female': 'comorense' }, 
            'gl': { 'male': 'comoriano', 'female': 'comoriana' }, 
        },
        'Congolese': {
            'ca': { 'male': 'congolès', 'female': 'congolesa' },
            'en': { 'male': 'Congolese', 'female': 'Congolese' }, 
            'es': { 'male': 'congoleño', 'female': 'congoleña' }, 
            'gl': { 'male': 'congolés', 'female': 'congolesa' }, 
        },
        'Costa Rican': {
            'ca': { 'male': 'costa-riqueny', 'female': 'costa-riquenya' },
            'en': { 'male': 'Costa Rican', 'female': 'Costa Rican' }, 
            'es': { 'male': 'costarricense', 'female': 'costarricense' }, 
            'gl': { 'male': 'costarriqueño', 'female': 'costarriqueña' }, 
        },
        'Croatian': {
            'ca': { 'male': 'croat', 'female': 'croata' },
            'en': { 'male': 'Croatian', 'female': 'Croatian' }, 
            'es': { 'male': 'croata', 'female': 'croata' }, 
            'gl': { 'male': 'croata', 'female': 'croata' }, 
        },
        'Cuban': {
            'ca': { 'male': 'cubà', 'female': 'cubana' },
            'en': { 'male': 'Cuban', 'female': 'Cuban' }, 
            'es': { 'male': 'cubano', 'female': 'cubana' }, 
            'gl': { 'male': 'cubano', 'female': 'cubana' }, 
        },
        'Cypriot': {
            'ca': { 'male': 'xipriota', 'female': 'xipriota' },
            'en': { 'male': 'Cypriot', 'female': 'Cypriot' }, 
            'es': { 'male': 'chipriota', 'female': 'chipriota' }, 
            'gl': { 'male': 'chipriota', 'female': 'chipriota' }, 
        },
        'Czech': {
            'ca': { 'male': 'txec', 'female': 'txeca' },
            'en': { 'male': 'Czech', 'female': 'Czech' }, 
            'es': { 'male': 'checo', 'female': 'checa' }, 
            'gl': { 'male': 'checo', 'female': 'checa' }, 
        },
        'Danish': {
            'ca': { 'male': 'danès', 'female': 'danesa' },
            'en': { 'male': 'Danish', 'female': 'Danish' }, 
            'es': { 'male': 'danés', 'female': 'danesa' }, 
            'gl': { 'male': 'danés', 'female': 'danesa' }, 
        },
        'Djiboutian': {
            'ca': { 'male': 'djiboutià', 'female': 'djiboutiana' },
            'en': { 'male': 'Djiboutian', 'female': 'Djiboutian' }, 
            'es': { 'male': 'yibutiano', 'female': 'yibutiana' }, 
            'gl': { 'male': 'xibutiano', 'female': 'xibutiana' }, 
        },
        'Ecuadorian': {
            'ca': { 'male': 'equatorià', 'female': 'equatoriana' },
            'en': { 'male': 'Ecuadorian', 'female': 'Ecuadorian' }, 
            'es': { 'male': 'ecuatoriano', 'female': 'ecuatoriana' }, 
            'gl': { 'male': 'ecuatoriano', 'female': 'ecuatoriana' }, 
        },
        'Egyptian': {
            'ca': { 'male': 'egipci', 'female': 'egípcia' },
            'en': { 'male': 'Egyptian', 'female': 'Egyptian' }, 
            'es': { 'male': 'egipcio', 'female': 'egipcia' }, 
            'gl': { 'male': 'exipcio', 'female': 'exipcia' }, 
        },
        'Equatoguinean': {
            'ca': { 'male': 'equatoguineà', 'female': 'equatoguineana' },
            'en': { 'male': 'Equatoguinean', 'female': 'Equatoguinean' }, 
            'es': { 'male': 'ecuatoguineano', 'female': 'ecuatoguineana' }, 
            'gl': { 'male': 'ecuatoguineano', 'female': 'ecuatoguineana' }, 
        },
        'Equatorial Guinean': {
            'ca': { 'male': 'equatoguineà', 'female': 'equatoguineana' },
            'en': { 'male': 'Equatorial Guinean', 'female': 'Equatorial Guinean' }, 
            'es': { 'male': 'ecuatoguineano', 'female': 'ecuatoguineana' }, 
            'gl': { 'male': 'ecuatoguineano', 'female': 'ecuatoguineana' }, 
        },
        'Eritrean': {
            'ca': { 'male': 'eritreu', 'female': 'eritrea' },
            'en': { 'male': 'Eritrean', 'female': 'Eritrean' }, 
            'es': { 'male': 'eritreo', 'female': 'eritrea' }, 
            'gl': { 'male': 'eritreo', 'female': 'eritrea' }, 
        },
        'Estonian': {
            'ca': { 'male': 'estonià', 'female': 'estoniana' },
            'en': { 'male': 'Estonian', 'female': 'Estonian' }, 
            'es': { 'male': 'estonio', 'female': 'estonia' }, 
            'gl': { 'male': 'estoniano', 'female': 'estoniana' }, 
        },
        'Ethiopian': {
            'ca': { 'male': 'etiòpic', 'female': 'etiòpica' },
            'en': { 'male': 'Ethiopian', 'female': 'Ethiopian' }, 
            'es': { 'male': 'etíope', 'female': 'etíope' }, 
            'gl': { 'male': 'etíope', 'female': 'etíope' }, 
        },
        'Fijian': {
            'ca': { 'male': 'fijià', 'female': 'fijiana' },
            'en': { 'male': 'Fijian', 'female': 'Fijian' }, 
            'es': { 'male': 'fiyiano', 'female': 'fiyiana' }, 
            'gl': { 'male': 'fidxiano', 'female': 'fidxiana' }, 
        },
        'Finnish': {
            'ca': { 'male': 'finlandès', 'female': 'finlandesa' },
            'en': { 'male': 'Finnish', 'female': 'Finnish' }, 
            'es': { 'male': 'finlandés', 'female': 'finlandesa' }, 
            'gl': { 'male': 'finlandés', 'female': 'finlandesa' }, 
        },
        'French': {
            'ca': { 'male': 'francès', 'female': 'francesa' },
            'en': { 'male': 'French', 'female': 'French' }, 
            'es': { 'male': 'francés', 'female': 'francesa' }, 
            'gl': { 'male': 'francés', 'female': 'francesa' }, 
        },
        'Gabonese': {
            'ca': { 'male': 'gabonès', 'female': 'gabonesa' },
            'en': { 'male': 'Gabonese', 'female': 'Gabonese' }, 
            'es': { 'male': 'gabonés', 'female': 'gabonesa' }, 
            'gl': { 'male': 'gabonés', 'female': 'gabonesa' }, 
        },
        'Gambian': {
            'ca': { 'male': 'gambià', 'female': 'gambiana' },
            'en': { 'male': 'Gambian', 'female': 'Gambian' }, 
            'es': { 'male': 'gambiano', 'female': 'gambiana' }, 
            'gl': { 'male': 'gambiano', 'female': 'gambiana' }, 
        },
        'Georgian': {
            'ca': { 'male': 'georgià', 'female': 'georgiana' },
            'en': { 'male': 'Georgian', 'female': 'Georgian' }, 
            'es': { 'male': 'georgiano', 'female': 'georgiana' }, 
            'gl': { 'male': 'xeorxiano', 'female': 'xeorxiana' }, 
        },
        'German': {
            'ca': { 'male': 'alemany', 'female': 'alemanya' },
            'en': { 'male': 'German', 'female': 'German' }, 
            'es': { 'male': 'alemán', 'female': 'alemana' }, 
            'gl': { 'male': 'alemán', 'female': 'alemá' }, 
        },
        'Ghanaian': {
            'ca': { 'male': 'ghanès', 'female': 'ghanesa' },
            'en': { 'male': 'Ghanaian', 'female': 'Ghanaian' }, 
            'es': { 'male': 'ghanés', 'female': 'ghanesa' }, 
            'gl': { 'male': 'ghanés', 'female': 'ghanesa' }, 
        },
        'Greek': {
            'ca': { 'male': 'grec', 'female': 'grega' },
            'en': { 'male': 'Greek', 'female': 'Greek' }, 
            'es': { 'male': 'griego', 'female': 'griega' }, 
            'gl': { 'male': 'grego', 'female': 'grega' }, 
        },
        'Greenlandic': {
            'ca': { 'male': 'groenlandès', 'female': 'groenlandesa' },
            'en': { 'male': 'Greenlandic', 'female': 'Greenlandic' }, 
            'es': { 'male': 'groenlandés', 'female': 'groenlandesa' }, 
            'gl': { 'male': 'groenlandés', 'female': 'groenlandesa' }, 
        },
        'Grenadian': {
            'ca': { 'male': 'grenadí', 'female': 'grenadina' },
            'en': { 'male': 'Grenadian', 'female': 'Grenadian' }, 
            'es': { 'male': 'granadino', 'female': 'granadina' }, 
            'gl': { 'male': 'granadino', 'female': 'granadina' }, 
        },
        'Guatemalan': {
            'ca': { 'male': 'guatemalenc', 'female': 'guatemalenca' },
            'en': { 'male': 'Guatemalan', 'female': 'Guatemalan' }, 
            'es': { 'male': 'guatemalteco', 'female': 'guatemalteca' }, 
            'gl': { 'male': 'guatemalteco', 'female': 'guatemalteca' }, 
        },
        'Guinean': {
            'ca': { 'male': 'guineà', 'female': 'guineana' },
            'en': { 'male': 'Guinean', 'female': 'Guinean' }, 
            'es': { 'male': 'guineano', 'female': 'guineana' }, 
            'gl': { 'male': 'guineano', 'female': 'guineana' }, 
        },
        'Guyanese': {
            'ca': { 'male': 'guyanès', 'female': 'guyanesa' },
            'en': { 'male': 'Guyanese', 'female': 'Guyanese' }, 
            'es': { 'male': 'guyanés', 'female': 'guyanesa' }, 
            'gl': { 'male': 'güianés', 'female': 'güianesa' }, 
        },
        'Haitian': {
            'ca': { 'male': 'haitià', 'female': 'haitiana' },
            'en': { 'male': 'Haitian', 'female': 'Haitian' }, 
            'es': { 'male': 'haitiano', 'female': 'haitiana' }, 
            'gl': { 'male': 'haitiano', 'female': 'haitiana' }, 
        },
        'Herzegovinian': {
            'ca': { 'male': 'hercegoví', 'female': 'hercegovina' },
            'en': { 'male': 'Herzegovinian', 'female': 'Herzegovinian' }, 
            'es': { 'male': 'herzegovino', 'female': 'herzegovina' }, 
            'gl': { 'male': 'hercegovino', 'female': 'hercegovina' }, 
        },
        'Honduran': {
            'ca': { 'male': 'hondureny', 'female': 'hondurenya' },
            'en': { 'male': 'Honduran', 'female': 'Honduran' }, 
            'es': { 'male': 'hondureño', 'female': 'hondureña' }, 
            'gl': { 'male': 'hondureño', 'female': 'hondureña' }, 
        },
        'Hungarian': {
            'ca': { 'male': 'hongarès', 'female': 'hongaresa' },
            'en': { 'male': 'Hungarian', 'female': 'Hungarian' }, 
            'es': { 'male': 'húngaro', 'female': 'húngara' }, 
            'gl': { 'male': 'húngaro', 'female': 'húngara' }, 
        },
        'Icelandic': {
            'ca': { 'male': 'islandès', 'female': 'islandesa' },
            'en': { 'male': 'Icelandic', 'female': 'Icelandic' }, 
            'es': { 'male': 'islandés', 'female': 'islandesa' }, 
            'gl': { 'male': 'islandés', 'female': 'islandesa' }, 
        },
        'Indian': {
            'ca': { 'male': 'indi', 'female': 'índia' },
            'en': { 'male': 'Indian', 'female': 'Indian' }, 
            'es': { 'male': 'indio', 'female': 'india' }, 
            'gl': { 'male': 'indio', 'female': 'india' }, 
        },
        'Indonesian': {
            'ca': { 'male': 'indonesi', 'female': 'indonèsia' },
            'en': { 'male': 'Indonesian', 'female': 'Indonesian' }, 
            'es': { 'male': 'indonesio', 'female': 'indonesia' }, 
            'gl': { 'male': 'indonesio', 'female': 'indonesia' }, 
        },
        'Iranian': {
            'ca': { 'male': 'iranià', 'female': 'iraniana' },
            'en': { 'male': 'Iranian', 'female': 'Iranian' }, 
            'es': { 'male': 'iraní', 'female': 'iraní' }, 
            'gl': { 'male': 'iraniano', 'female': 'iraniana' }, 
        },
        'Iraqi': {
            'ca': { 'male': 'iraquià', 'female': 'iraquiana' },
            'en': { 'male': 'Iraqi', 'female': 'Iraqi' }, 
            'es': { 'male': 'iraquí', 'female': 'iraquí' }, 
            'gl': { 'male': 'iraquí', 'female': 'iraquí' }, 
        },
        'Irish': {
            'ca': { 'male': 'irlandès', 'female': 'irlandesa' },
            'en': { 'male': 'Irish', 'female': 'Irish' }, 
            'es': { 'male': 'irlandés', 'female': 'irlandesa' }, 
            'gl': { 'male': 'irlandés', 'female': 'irlandesa' }, 
        },
        'Israeli': {
            'ca': { 'male': 'israelià', 'female': 'israeliana' },
            'en': { 'male': 'Israeli', 'female': 'Israeli' }, 
            'es': { 'male': 'israelí', 'female': 'israelí' }, 
            'gl': { 'male': 'israelí', 'female': 'israelí' }, 
        },
        'Italian': {
            'ca': { 'male': 'italià', 'female': 'italiana' }, 
            'en': { 'male': 'Italian ', 'female': 'Italian' }, 
            'es': { 'male': 'italiano', 'female': 'italiana' }, 
            'gl': { 'male': 'italiano', 'female': 'italiana' }, 
        }, 
        'Ivorian': {
            'ca': { 'male': 'ivorià', 'female': 'ivoriana' }, 
            'en': { 'male': 'Ivorian ', 'female': 'Ivorian' }, 
            'es': { 'male': 'marfileño', 'female': 'marfileña' }, 
            'gl': { 'male': 'marfilés', 'female': 'marfilesa' }, 
        }, 
        'Portuguese': {
            'ca': { 'male': 'portuguès', 'female': 'portuguesa' }, 
            'en': { 'male': 'Portuguese', 'female': 'Portuguese' }, 
            'es': { 'male': 'portugués', 'female': 'portuguesa' }, 
            'gl': { 'male': 'portugués', 'female': 'portuguesa' }, 
        }, 
        'Russian': {
            'ca': { 'male': 'rus', 'female': 'russa' }, 
            'en': { 'male': 'Russian', 'female': 'Russian' }, 
            'es': { 'male': 'ruso', 'female': 'rusa' }, 
            'gl': { 'male': 'ruso', 'female': 'rusa' }, 
        }, 
        'Salvadoran': {
            'ca': { 'male': 'salvadorenc', 'female': 'salvadorenca' }, 
            'en': { 'male': 'Salvadoran', 'female': 'Salvadoran' }, 
            'es': { 'male': 'salvadoreño', 'female': 'salvadoreña' }, 
            'gl': { 'male': 'salvadoreño', 'female': 'salvadoreña' }, 
        }, 
        'Spanish': {
            'ca': { 'male': 'espanyol', 'female': 'espanyola' }, 
            'en': { 'male': 'Spanish', 'female': 'Spanish' }, 
            'es': { 'male': 'español', 'female': 'española' }, 
            'gl': { 'male': 'español', 'female': 'española' }, 
        }, 
    }
    #more occupations https://query.wikidata.org/#SELECT%20%3Foccupation%20%28COUNT%28%3Fitem%29%20AS%20%3Fcount%29%0AWHERE%20%7B%0A%09%3Fitem%20wdt%3AP31%20wd%3AQ5.%0A%20%20%20%20%3Fitem%20wdt%3AP27%20wd%3AQ142.%0A%20%20%20%20%3Fitem%20wdt%3AP106%20%3Foccupation.%0A%20%20%20%20%23SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22%20.%20%7D%0A%7D%0AGROUP%20by%20%3Foccupation%0AORDER%20BY%20DESC%28%3Fcount%29
    #translations https://query.wikidata.org/#SELECT%20%3FitemDescription%20%28COUNT%28%3Fitem%29%20AS%20%3Fcount%29%0AWHERE%20%7B%0A%09%3Fitem%20wdt%3AP31%20wd%3AQ5.%0A%20%20%20%20%3Fitem%20wdt%3AP106%20wd%3AQ28389.%0A%20%20%20%20OPTIONAL%20%7B%20%3Fitem%20schema%3Adescription%20%3FitemDescription.%20FILTER%28LANG%28%3FitemDescription%29%20%3D%20%22gl%22%29.%20%20%7D%0A%09FILTER%20%28BOUND%28%3FitemDescription%29%29%0A%7D%0AGROUP%20BY%20%3FitemDescription%0AORDER%20BY%20DESC%28%3Fcount%29
    translationsOccupations = {
        '~ actor': {
            'ca': { 'male': 'actor ~', 'female': 'actriu ~' }, 
            'en': { 'male': '~ actor', 'female': '~ actress' }, 
            'es': { 'male': 'actor ~', 'female': 'actriz ~' }, 
            'gl': { 'male': 'actor ~', 'female': 'actriz ~' }, 
        }, 
        '~ association football player': {
            'ca': { 'male': 'futbolista ~', 'female': 'futbolista ~' }, 
            'en': { 'male': '~ association football player', 'female': '~ association football player' }, 
            'es': { 'male': 'futbolista ~', 'female': 'futbolista ~' }, 
            'gl': { 'male': 'futbolista ~', 'female': 'futbolista ~' }, 
        }, 
        '~ composer': {
            'ca': { 'male': 'compositor ~', 'female': 'compositora ~' }, 
            'en': { 'male': '~ composer', 'female': '~ composer' }, 
            'es': { 'male': 'compositor ~', 'female': 'compositora ~' }, 
            'gl': { 'male': 'compositor ~', 'female': 'compositora ~' }, 
        }, 
        '~ footballer': {
            'ca': { 'male': 'futbolista ~', 'female': 'futbolista ~' }, 
            'en': { 'male': '~ footballer', 'female': '~ footballer' }, 
            'es': { 'male': 'futbolista ~', 'female': 'futbolista ~' }, 
            'gl': { 'male': 'futbolista ~', 'female': 'futbolista ~' }, 
        }, 
        '~ historian': {
            'ca': { 'male': 'historiador ~', 'female': 'historiadora ~' }, 
            'en': { 'male': '~ historian', 'female': '~ historian' }, 
            'es': { 'male': 'historiador ~', 'female': 'historiadora ~' }, 
            'gl': { 'male': 'historiador ~', 'female': 'historiadora ~' }, 
        }, 
        '~ journalist': {
            'ca': { 'male': 'periodista ~', 'female': 'periodista ~' }, 
            'en': { 'male': '~ journalist', 'female': '~ journalist' }, 
            'es': { 'male': 'periodista ~', 'female': 'periodista ~' }, 
            'gl': { 'male': 'xornalista ~', 'female': 'xornalista ~' }, 
        }, 
        '~ painter': {
            'ca': { 'male': 'pintor ~', 'female': 'pintora ~' }, 
            'en': { 'male': '~ painter', 'female': '~ painter' }, 
            'es': { 'male': 'pintor ~', 'female': 'pintora ~' }, 
            'gl': { 'male': 'pintor ~', 'female': 'pintora ~' }, 
        }, 
        '~ poet': {
            'ca': { 'male': 'poeta ~', 'female': 'poetessa ~' }, 
            'en': { 'male': '~ poet', 'female': '~ poet' }, 
            'es': { 'male': 'poeta ~', 'female': 'poetisa ~' }, 
            'gl': { 'male': 'poeta ~', 'female': 'poetisa ~' }, 
        }, 
        '~ politician': {
            'ca': { 'male': 'polític ~', 'female': 'política ~' }, 
            'en': { 'male': '~ politician', 'female': '~ politician' }, 
            'es': { 'male': 'político ~', 'female': 'política ~' }, 
            'gl': { 'male': 'político ~', 'female': 'política ~' }, 
        }, 
        '~ screenwriter': {
            'ca': { 'male': 'guionista ~', 'female': 'guionista ~' }, 
            'en': { 'male': '~ screenwriter', 'female': '~ screenwriter' }, 
            'es': { 'male': 'guionista ~', 'female': 'guionista ~' }, 
            'gl': { 'male': 'guionista ~', 'female': 'guionista ~' }, 
        }, 
        '~ soldier': {
            'ca': { 'male': 'militar ~', 'female': 'militar ~' }, 
            'en': { 'male': '~ soldier', 'female': '~ soldier' }, 
            'es': { 'male': 'militar ~', 'female': 'militar ~' }, 
            'gl': { 'male': 'militar ~', 'female': 'militar ~' }, 
        }, 
        '~ tennis player': {
            'ca': { 'male': 'tennista professional ~', 'female': 'tennista professional ~' }, 
            'en': { 'male': '~ tennis player', 'female': '~ tennis player' }, 
            'es': { 'male': 'tenista profesional ~', 'female': 'tenista profesional ~' }, 
            'gl': { 'male': 'tenista profesional ~', 'female': 'tenista profesional ~' }, 
        }, 
        '~ writer': {
            'ca': { 'male': 'escriptor ~', 'female': 'escriptora ~' }, 
            'en': { 'male': '~ writer', 'female': '~ writer' }, 
            'es': { 'male': 'escritor ~', 'female': 'escritora ~' }, 
            'gl': { 'male': 'escritor ~', 'female': 'escritora ~' }, 
        }, 
    }
    translations = {}
    for occupkey, occupdic in translationsOccupations.items():
        for natkey, natdic in translationsNationalities.items():
            translations[re.sub('~', natkey, occupkey)] = {}
            for translang in occupdic.keys():
                translations[re.sub('~', natkey, occupkey)][translang] = {
                    'male': re.sub('~', natdic[translang]['male'], occupdic[translang]['male']), 
                    'female': re.sub('~', natdic[translang]['female'], occupdic[translang]['female']), 
                }
    c2 = 1
    total2 = 0
    for targetlang in targetlangs:
        for genderq, genderlabel in genders.items():
            for translation in translations.keys():
                url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=SELECT%20%3Fitem%0AWHERE%20%7B%0A%20%20%20%20%3Fitem%20wdt%3AP31%20wd%3AQ5%20.%20%23instanceof%0A%20%20%20%20%3Fitem%20wdt%3AP21%20wd%3A'+genderq+'%20.%20%23gender%0A%20%20%20%20%3Fitem%20schema%3Adescription%20%22'+re.sub(' ', '%20', translation)+'%22%40en.%20%23description%0A%20%20%20%20OPTIONAL%20%7B%20%3Fitem%20schema%3Adescription%20%3FitemDescription.%20FILTER(LANG(%3FitemDescription)%20%3D%20%22'+targetlang+'%22).%20%20%7D%0A%20%20%20%20FILTER%20(!BOUND(%3FitemDescription))%0A%7D'
                url = '%s&format=json' % (url)
                sparql = getURL(url=url)
                json1 = loadSPARQL(sparql=sparql)
                total = len(json1['results']['bindings'])
                total2 += total
                c = 1
                for result in json1['results']['bindings']:
                    q = 'item' in result and result['item']['value'].split('/entity/')[1] or ''
                    print('\n== %s (%d/%d; %s; %s; %d/%d) ==' % (q, c, total, translation, genderlabel, c2, total2))
                    c += 1
                    c2 += 1
                    item = pywikibot.ItemPage(repo, q)
                    item.get()
                    descriptions = item.descriptions
                    addedlangs = []
                    for lang in translations[translation].keys():
                        if not lang in descriptions.keys():
                            descriptions[lang] = translations[translation][lang][genderlabel]
                            addedlangs.append(lang)
                    data = { 'descriptions': descriptions }
                    addedlangs.sort()
                    if addedlangs:
                        summary = 'BOT - Adding descriptions (%s languages): %s' % (len(addedlangs), ', '.join(addedlangs))
                        print(summary)
                        try:
                            item.editEntity(data, summary=summary)
                        except:
                            print('Error while saving')
                            continue

if __name__ == "__main__":
    main()