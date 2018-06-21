import urllib
from urllib import request

import datetime
import urllib.request
from bs4 import BeautifulSoup

from spotipy.oauth2 import SpotifyClientCredentials
from src.Client import Spotify

import pylast

## Currently not functional as the following information/variables are not defined
last_API_KEY = '???'  # this is a sample key
last_API_SECRET = '???'

# In order to perform a write operation you need to authenticate yourself
last_username = "???"
last_password_hash = pylast.md5("???")

spotify_client_id = '???'
spotify_client_secret = '???'

spotify_username = '???'

def getLyrics(song_info):
	print(song_info)

	page = urllib.request.urlopen(
		r'http://www.rentanadviser.com/en/subtitles/getsubtitle.aspx?artist=%s&song=%s' %
		(song_info.get_artist(), song_info.get_title()))

	soup = BeautifulSoup(page, 'html.parser')


	lyrics = soup.body.find('span', attrs={'id': 'ctl00_ContentPlaceHolder1_lblSubtitle'})
	for br in lyrics.find_all('br'):
		br.replace_with('\n')
	print(lyrics.text.strip())

	as_string = lyrics.text.strip()

	by_line = as_string.split("\n\n")

	by_line = by_line[:-2]

	by_more = []

	for element in by_line:
		element_split = element.split("\n")
		element_split = element_split[1:]
		rejoin_lyrics = element_split[1]
		for part in element_split[2:]:
			rejoin_lyrics += " " + part
		end_time = element_split[0].split(" --> ")[1]

		by_colon = end_time.split(":")
		sec_split = by_colon[2].split(",")
		seconds = int(sec_split[0])
		milli = int(sec_split[1])/1000
		end_time_int = int(by_colon[1]) * 60 + seconds + milli
		by_more.append((end_time_int, rejoin_lyrics.capitalize()))

	return by_more

	# Used for local testing and displaying
	# Because I could not track song progress with the spotify api on windows,
	# I was forced to track it myself, and webscraping was too slow

	# if not os.path.exists('C:\\Lyrics\\' + song_info + ".txt"):
	# 	if not os.path.exists('C:\\Lyrics\\' + song_info + ".srt"):
	# 		return ()
	#
	# 	f = open('C:\\Lyrics\\' + song_info + ".srt", "r")
	# 	as_string = f.read()
	#
	# 	by_line = as_string.split("\n\n")
	#
	# 	by_line = by_line[:-2]
	#
	# 	by_more = []
	#
	# 	for element in by_line:
	# 		element_split = element.split("\n")
	# 		element_split = element_split[1:]
	# 		rejoin_lyrics = element_split[1]
	# 		for part in element_split[2:]:
	# 			rejoin_lyrics += " " + part
	# 		end_time = element_split[0].split(" --> ")[1]
	#
	# 		by_colon = end_time.split(":")
	# 		sec_split = by_colon[2].split(",")
	# 		seconds = int(sec_split[0])
	# 		milli = int(sec_split[1])/1000
	# 		end_time_int = int(by_colon[1]) * 60 + seconds + milli
	# 		by_more.append((end_time_int, rejoin_lyrics.capitalize()))
	# 	f.close()
	#
	# 	prod = open('C:\\Lyrics\\' + song_info + ".txt", "w")
	# 	prod.write(str(tuple(by_more)))
	#
	# 	prod.close()
	#
	# 	return by_more
	# else:
	# 	f = open('C:\\Lyrics\\' + song_info + ".txt")
	# 	as_string = f.read()
	# 	f.close()
	# 	evalled = ast.literal_eval(as_string)
	# 	return evalled


class SpotifyStuff:
	def __int__(self):
		self.last_network = pylast.LastFMNetwork(api_key=last_API_KEY, api_secret=last_API_SECRET,
		                                         username=last_username, password_hash=last_password_hash)
		self.dic = dict(title="", artist="", album_title="", album_art="", duration="",
		                lyrics="")
		self.last_user = self.last_network.get_user("shanetimmerman")
		client_credentials_manager = SpotifyClientCredentials(client_id=spotify_client_id,
		                                                      client_secret=spotify_client_secret)
		self.sp = Spotify(client_credentials_manager=client_credentials_manager)
		self.switch = False
		self.last_call = datetime.datetime.now()
		self.last_played = None

	def currentSong(self):
		self.last_call = datetime.datetime.now()

		song_info = self.last_played
		try:
			artist = song_info.get_artist()

			title = song_info.get_title()

			album = song_info.get_album()

			album_title = album.get_title()

			url = album.get_cover_image()

			request.urlretrieve(url, 'C:\\AlbumArt\\Raw.jpg')

			duration = song_info.get_duration()
			album_art = self.crop_image()
			lyrics = getLyrics(song_info)
			self.dic['title'] = str(title)
			self.dic['artist'] = str(artist)
			self.dic['album_title'] = str(album_title)
			self.dic['album_art'] = album_art
			self.dic['duration'] = str(duration)
			self.dic['lyrics'] = lyrics
		except AttributeError:
			pass

	def getCurrent(self):
		return self.dic

	def crop_image(self):
		import cv2

		image = cv2.imread(r'C:\AlbumArt\raw.jpg')

		width = 300
		height = 300
		optimal_height = width * 10 // 16

		cropped = image[5 * (height - optimal_height)//8: 5 * (height + optimal_height)//8, 0:width]

		blur = cv2.blur(cropped, (5, 5))

		#  Alternates what it writes to, or else the image cannot be overridden
		self.switch = not self.switch

		cv2.imwrite(r"C:\AlbumArt\Background" + str(self.switch) + ".jpg", blur)
		return r"C:\AlbumArt\Background" + str(self.switch) + ".jpg"

	def getSwitchTime(self):
		return self.last_call

	def check_change(self):
		current = self.last_user.get_now_playing()
		if self.last_played != current:
			self.last_played = current
			self.last_call = datetime.datetime.now()
			return True
		return False


