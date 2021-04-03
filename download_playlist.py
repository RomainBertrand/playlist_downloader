#!/usr/bin/env python
"""Place this file in an empty folder"""
import os
import sys
import youtube_dl

def all_files(path: str) -> list:
    """Given a path, return all files found in folder"""
    # pre_processing
    if path[-1] == "/":
        path = path[:-1]
    return [path+"/"+f for f in  os.listdir(path)]

def videos_id(playlist_link: str, ydl: youtube_dl.YoutubeDL) -> list:
    """Given a playlist link and a youtube_downloader,

    Return the list of youtube ids in the playlist"""
    list_ids = []
    result = ydl.extract_info \
    (playlist_link,
    download=False) #We just want to extract the info

    if 'entries' in result:
        # Can be a playlist or a list of videos
        video = result['entries']

        #loops entries to grab each video_url
        for i, _ in enumerate(video):
            video = result['entries'][i]
            list_ids.append(video["id"])
    return list_ids

def merge_audio_files(ordered_list: list, output_file_name: str) -> None:
    """Given a list of ordered audio files, concatenate them using FFMPEG"""
    ffmpeg_arguments = ' -i "concat:'
    for audio in ordered_list:
        assert os.path.exists(audio+".mp3"), "Error, an audio file doesn't exist"
        ffmpeg_arguments += audio+'.mp3|'
    ffmpeg_arguments = ffmpeg_arguments[:-1]
    ffmpeg_arguments += '"'
    os.system('ffmpeg {0} "{1}.mp3"'.format(ffmpeg_arguments, output_file_name))

def main():
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(id)s.',
        'quiet': False
    }
    youtube_downloader = youtube_dl.YoutubeDL(ydl_opts)

    playlist_url = sys.argv[1]
    playlist_name = sys.argv[2]

    # First, we create a list of IDs of video, so that if there is an issue with FFMPEG
    # we don't have to download everything again.
    video_ids_to_download = videos_id(playlist_url, youtube_downloader)

    # download the files here
    youtube_downloader.download(video_ids_to_download)

    # finally, merge all video files
    merge_audio_files(video_ids_to_download, playlist_name)



if __name__ == '__main__':
    main()
