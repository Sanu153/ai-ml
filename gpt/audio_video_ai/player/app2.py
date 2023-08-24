import vlc
import pafy
import time

url="https://www.youtube.com/watch?v=lS9U7GMbYZc"
video = pafy.new(url)
best = video.getbest()
playurl = best.url
instance = vlc.Instance()
player = instance.media_player_new()
media=instance.media_player_new(playurl)
media.get_mrl()
player.set_media(media)
player.play()
time.sleep(50)