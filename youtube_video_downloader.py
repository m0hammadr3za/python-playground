import re
from pytube import YouTube

link = input("Enter you video link: ")
yt = YouTube(link)

video_with_audio = []
audio_only = []

for stream in yt.streams.filter(adaptive=True, type="video"):
    video = {}
    video['itag'] = stream.itag
    video['mime_type'] = stream.mime_type
    video['resolution'] = stream.resolution
    video['fps'] = stream.fps
    video['codecs'] = stream.codecs

    video_with_audio.append(video)

for stream in yt.streams.filter(adaptive=True, type="audio"):
    audio = {}
    audio['itag'] = stream.itag
    audio['mime_type'] = stream.mime_type
    audio['abr'] = stream.abr
    audio['codecs'] = stream.codecs

    audio_only.append(audio)

print()
print(f"Video title: \"{yt.title}\"")
print("What do you want to do with this video?", end="\n\n")

print("Download video with audio: ")
for i in range(len(video_with_audio)):
    video = video_with_audio[i]
    print(f'[ {i} ] {video["mime_type"]} {video["resolution"]}p {video["fps"]}fps {video["codecs"]}')
print()

print("Download audio only: ")
next_index = len(video_with_audio)
for i in range(len(audio_only)):
    audio = audio_only[i]
    print(f'[ {next_index + i} ] {audio["mime_type"]} {audio["abr"]} {video["codecs"]}')
print()

next_index = len(video_with_audio) + len(audio_only)
print(f"[ {next_index} ] Download thumbnail", end="\n")