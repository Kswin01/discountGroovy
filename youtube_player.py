import vlc
import pafy

url = "https://www.youtube.com/watch?v=CKZvWhCqx1s"

video = pafy.new(url)
best = video.getbest()
playurl = best.url

media = vlc.MediaPlayer(playurl)
media.play