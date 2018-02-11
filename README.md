# HBP2018

The main intention of this project was to familiarize myself with Spotify's api (never again), learning about 
dynamically updating GUI libraries (expeciall Kivy. God I love that markdown support) in Python, and use them
to develop revamp the full screen mode in the Spotify desktop app. Rather than just filling the space, I wanted
to highlight what I can about seeing, real time lyrics and a major focus on album art, which the mobile apps do
fanastically.


Do to the lack of Spotify api support in python, and more importantly desktop. this solution is less than idael.
Additional api (most noteably Last.fm) had to be used to get much of the information, but due to throttling of my 
api usage, I had to cut back on querying it. Fewer queries and the focus on real time lyrics lead to the loss of 
the app detecting changes in the user's music, so all control of Spotify must go through the app if you want the 
lyrics to do anything. If spotify allows me to see progress in a song in the future I would love to be able to 
change everything I did here.
