import threading, time, pafy, vlc, urllib.request, re

playlist = []
global_checker = 0

def get_sec(time_str):
    h, m, s= time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def youtube_search(search):
    c_result = search.replace(" ", "+")
    get_url = "https://www.youtube.com/results?search_query=" + c_result
    get_html = urllib.request.urlopen(get_url)
    video_ids = re.findall(r"watch\?v=(\S{11})", get_html.read().decode())
    result = pafy.new("https://www.youtube.com/watch?v=" + video_ids[0])
    return result


def insert():
    while True:
        playlist.append(input("Search Music:"))

def start():
    global playlist

    if len(playlist) == 0:
        playlist.append(input("Search Music:"))
        start()
    
    while True:
        for x in playlist:
            music = youtube_search(x)
            s_duration = get_sec(music.duration)
            audio = music.getbestaudio()
            audio_url = audio.url
            player = vlc.MediaPlayer(audio_url)
            player.audio_set_volume(40)
            player.play()
            t1 = threading.Thread(target=insert)
            t1.start()
            time.sleep(s_duration)
            playlist.pop(0)

start()
