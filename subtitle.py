#! /usr/bin/env python3
# vim: fenc=utf-8 ts=4 et sw=4 sts=4

# This file is part of Subtitle.
#
# Subtitle is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Subtitle is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import requests
from bs4 import BeautifulSoup

Site_Domain = "https://subscene.com"
Search_Url = "{0}/subtitles/release?q={1}"

subtitles = []


# Models
class Subtitle:
    def __init__(self, release, link, lang, owner, rated, commant):
        self.link = link
        self.release = release
        self.lang = lang
        self.owner = owner
        self.rated = rated
        self.commant = commant
        self._direct = None

    def __str__(self):
        return self.release

    @property
    def direct_zip(self):
        if self._direct: return self._direct
        soup = soup_page(self.link)
        link = Site_Domain + soup.find('a', {"id": "downloadButton"}).get('href')
        self._direct = link
        return link


# Utils
def soup_page(url):
    return BeautifulSoup(requests.get(url).text, "html.parser")


def search(query, langage=None):
    soup = soup_page(Search_Url.format(Site_Domain, query))
    table = soup.find('tbody')
    global subtitles
    for row in table.findAll('tr'):
        spans = row.findAll('span')
        link = Site_Domain + row.find('a').get('href')
        lang = spans[0].get_text().strip().lower()
        release = spans[1].get_text().strip()
        owner = row.find("td", {"class": "a5"}).get_text().strip()
        commant = row.find("td", {"class": "a6"}).get_text().strip()
        rated = "Bad" if ("neutral-icon" in spans[0].get('class')) else "Good"

        if langage is None or lang in langage.lower():
            subtitles.append(Subtitle(release, link, lang, owner, rated, commant))
    return subtitles


def first_subtitle(lang):
    return next(sub for sub in subtitles if sub.lang in lang)
