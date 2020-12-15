import json
import requests
from bs4 import BeautifulSoup

ARTISTS = [
  {'name': 'Kanye', 'genius_id': 72}
]
# longest matching bigram
# most similar documents

def get_songs(artist):
  API = 'https://genius.com/api/artists/{}/songs?page={}&sort=popularity'

  genius_id = artist.get('genius_id')
  page = 1
  all_songs = []

  while True:
    print('grabbing {}'.format(page))
    req = requests.get(API.format(genius_id, page))
    res = json.loads(req.text)
    songs = res['response']['songs']
    all_songs += songs
    page = res['response']['next_page']
    if page is None: break

  return all_songs


def get_lyrics(url):
  req = requests.get(url)
  soup = BeautifulSoup(req.text)
  lyrics_div = soup.find('div', {'class': 'lyrics'})
  raw_lyrics_list = lyrics_div.get_text().split('\n')
  lyrics = []
  section = None
  i = 0
  for l in raw_lyrics_list:
    if not l: continue
    if l.startswith('['):
      section = l[1:].split(':')[0].lower()
    else:
      clean_lyric = l.replace('(','').replace(')','')
      lyrics.append((clean_lyric, section, i))
      i += 1

  return lyrics

def main():
  all_kanye_songs = get_songs(ARTISTS[0])
