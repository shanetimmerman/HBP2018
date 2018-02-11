from time import sleep

from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'fullscreen', 1)


from kivy.core.window import Window

import win32api

import datetime

from kivy.app import App
from kivy.clock import Clock

from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty

from src.SpotipyTests import SpotifyStuff

from kivy.core.text import LabelBase

KIVY_FONTS = [
	{
		"name": "PT_Sans",
		"fn_regular": "font/PT_Sans-Caption-Web-Regular.ttf",
		"fn_bold": "font/PT_Sans-Caption-Web-Bold.ttf"
	}
]

for font in KIVY_FONTS:
	LabelBase.register(**font)

clock_interval = 0.50

kv = '''
AnchorLayout:
	
	Image:
		source: app.album_art
		allow_stretch: True 
		color: (.8, .8, .8, .3)
	BoxLayout:
		id: main_frame
		orientation: 'vertical'
		size_hint: (1, .8)
		BoxLayout:
			id: top_frame
			orientation: 'vertical'
			padding: (0, self.width / 6)
			spacing: 20
			Label: 
				id: lyric1
				text: app.lyric_text1
				text_size: app.lyric_font_size, None
				font_name: 'PT_Sans'
				halign: 'center'
				valign: 'center'
				color: (1, 1, 1, 0.3)
				font_size: 19
			Label:
				id: lyric2
				text: app.lyric_text2
				font_name: 'PT_Sans'
				text_size: app.lyric_font_size, None
				halign: 'center'
				valign: 'center'
				color: (1, 1, 1, 0.5)
				font_size: 22
			Label:
				id: lyric3
				text: app.lyric_text3
				text_size: app.lyric_font_size, None
				font_name: 'PT_Sans'
				halign: 'center'
				valign: 'center'
				color: (1, 1, 1, 1)
				font_size: 26
			Label:
				id: lyric4
				text: app.lyric_text4
				text_size: app.lyric_font_size, None
				font_name: 'PT_Sans'
				halign: 'center'
				valign: 'center'
				color: (1, 1, 1, 0.5)
				font_size: 22
			Label:
				id: lyric5 
				text: app.lyric_text5
				text_size: app.lyric_font_size, None
				font_name: 'PT_Sans'
				halign: 'center'
				valign: 'center'
				color: (1, 1, 1, 0.3)
				font_size: 19
		AnchorLayout:
			size_hint: (1, .2) 
			anchor_y: 'bottom'
			BoxLayout:
				id: bottom_frame
				orientation: 'vertical'
				anchor_y: 'bottom'
				padding: 20
				Label:
					id: song_title
					text: app.song_title
					text_size: app.title_font_size
					halign: 'center'
					valign: 'center'
					color: (1, 1, 1, 1)
					fount_size: '30sp'
					font_name: 'PT_Sans'
					bold: True
					
				Label:
					id: song_artist
					text: app.song_artist
					text_size: app.artist_font_size
					halign: 'center'
					valign: 'center'
					fount_size: '50sp'
					color: (1, 1, 1, 1)
					font_name: 'PT_Sans'
					bold: True
					
			AnchorLayout:
				size_hint: (1, .2) 
				anchor_y: 'bottom'
				ProgressBar:
					value: app.progress_value
						
'''

Media_Next = 0xB0
Media_Previous = 0xB1
Media_Pause = 0xB3  ##Play/Pause
Media_Mute = 0xAD

def hwcode(Media):
	hwcode = win32api.MapVirtualKey(Media, 0)
	return hwcode


def next_track():
	win32api.keybd_event(Media_Next, hwcode(Media_Next))


def previous_track():
	win32api.keybd_event(Media_Previous, hwcode(Media_Previous))


def pause_resume():
	win32api.keybd_event(Media_Pause, hwcode(Media_Pause))


class GUI(App):
	icon = 'C:\\User\\Shane\\Desktop\\icon.png'
	title = 'Making Bahar Proud?'

	song_artist = StringProperty()
	song_title = StringProperty()
	lyric_text1 = StringProperty()
	lyric_text2 = StringProperty()
	lyric_text3 = StringProperty()
	lyric_text4 = StringProperty()
	lyric_text5 = StringProperty()
	album_art = StringProperty()
	progress_value = NumericProperty()

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
		self.start_time = datetime.datetime.now()
		self.elapsed = 0

		self.spotify = SpotifyStuff()
		self.spotify.__int__()
		self.song_artist = 'artist'
		self.artist_font_size = (500, None)
		self.song_title = 'title'
		self.title_font_size = (500, None)

		self.current_lyric = 0

		previous_track()

		# pause_resume()

		self.paused = True
		self.duration = ''

		self.lyric_list = []
		self.lyric_text1 = 'text1'
		self.lyric_text2 = 'text2'
		self.lyric_text3 = 'text3'
		self.lyric_text4 = 'text4'
		self.lyric_text5 = 'text5'
		self.lyric_font_size = 800
		self.album_art = r'C:\Users\shane\Downloads\Bee+dad.jpg'
		self._keyboard.bind(on_key_down=self._on_keyboard_up)
		self.progress_value = 0

		self.currentSongDetails()

	def _on_keyboard_up(self, keyboard, keycode, text, modifiers):
		if keycode[1] == 'right':
			next_track()
			self.progress_value = 0
		if keycode[1] == 'left':
			previous_track()
			self.progress_value = 0
		if keycode[1] == '+':
			self.start_time -= datetime.timedelta(seconds=.5)
			self.refresh()
			return
		if keycode[1] == '-':
			self.start_time += datetime.timedelta(seconds=.5)
		if keycode[1] == 'spacebar':
			pause_resume()
			self.paused = not self.paused
		else:
			self.currentSongDetails()

	def _keyboard_closed(self):
		print('My keyboard have been closed!')
		self._keyboard.unbind(on_key_down=self._on_keyboard_up)
		self._keyboard = None

	def build(self):
		return Builder.load_string(kv)

	def run(self):
		super().run()

	def refresh(self):
		self.lyric_text1, self.lyric_text2, self.lyric_text3, self.lyric_text4, self.lyric_text5 = self.updateLyrics()
		if self.duration == '':
			self.progress_value = 0
		else:
			self.progress_value = self.elapsed * 100000 / int(self.duration)

	def updateLyrics(self):

		timedelta = datetime.datetime.now() - self.start_time

		if self.paused:
			elapsed = datetime.datetime.now() - self.start_time
			self.start_time += datetime.timedelta(seconds=elapsed.total_seconds() - self.elapsed + clock_interval)

		else:
			self.elapsed = timedelta.total_seconds()

		if len(self.duration) == 0 or self.elapsed > int(self.duration) / 1000:
			while not self.currentSongDetails():
				sleep(0.1)
		if len(self.lyric_list) == 0:
			return "", "", "", "", ""

		current = self.currentLyric()
		self.current_lyric = current
		print(self.lyric_list[current])
		lyric1 = ''
		lyric2 = ''
		lyric3 = self.lyric_list[current][1]
		lyric4 = ''
		lyric5 = ''

		if current > 0:
			lyric2 = self.lyric_list[current - 1][1]
		if current > 1:
			lyric1 = self.lyric_list[current - 2][1]

		total_amount = len(self.lyric_list)

		if current + 1 < total_amount:
			lyric4 = self.lyric_list[current + 1][1]
		if current + 2 < total_amount:
			lyric5 = self.lyric_list[current + 2][1]


		return lyric1, lyric2, lyric3, lyric4, lyric5

	def currentLyric(self):
		if len(self.lyric_list) == 0:
			return 0
		if self.lyric_list[self.current_lyric][0] < self.elapsed:
			count = self.current_lyric + 1
			while count < len(self.lyric_list):
				if self.lyric_list[count][0] > self.elapsed:
					return count
			return count - 1
		return self.current_lyric

	def currentSongDetails(self):
		change = self.spotify.check_change()
		if change:
			self.spotify.currentSong()
			updated = self.spotify.getCurrent()
			self.start_time = self.spotify.getSwitchTime()
			self.song_artist = updated['artist']
			self.song_title = updated['title']
			self.lyric_list = updated['lyrics']
			self.album_art = updated['album_art']
			self.duration = updated['duration']
			self.start_time = datetime.datetime.now()
			self.current_lyric = 0
		return change


def refresh(self):
	self.refresh()


if __name__ == '__main__':
	app = GUI()
	Clock.schedule_interval(lambda dt: refresh(app), clock_interval)
	app.build()
	app.run()  # your long-running job goes here...


