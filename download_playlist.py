#!/usr/bin/env python
"""Place this file in an empty folder"""
import os
import argparse
import youtube_dl


def clean_title(video) -> str:
    """Given a video object

    Return a well formed string for the song title"""
    title = video["title"]
    if "(" in title and ")" in title:  # remove unnecessary elements, such as "(lyrics)"
        opening_parenthesis_index = title.index("(")
        closing_parenthesis_index = title.index(")")
        title = title[:opening_parenthesis_index] + title[closing_parenthesis_index+1:]
    if " - " not in title:  # add an 'artist' if no author in initial title
        if len(video["artist"]) > 0:
            title = video["artist"] + " - " + title
        else:
            title = video["channel"] + " - " + title # if it's youtube that automatically add 
            # video then the "uploader" countains "[...] - Topic" so we try to use "channel"
    return title


def videos_id(playlist_link: str, ydl: youtube_dl.YoutubeDL, playlist_name=None, delete_files=True) -> (list, list, str):
    """Given a playlist link and a youtube_downloader,

    Return the list of youtube ids in the playlist, a list of the titles, and the playlist name"""
    list_ids = []
    list_titles = []
    result = ydl.extract_info(playlist_link,
                              download=False)  # We just want to extract the info

    if 'entries' in result:
        if playlist_name is None:
            playlist_name = result["playlist_name"]
        # Can be a playlist or a list of videos
        video = result['entries']

        # loops entries to grab each video_url
        for i, _ in enumerate(video):
            video = result['entries'][i]
            list_ids.append(video["id"])
            if not delete_files:
                list_titles.append(clean_title(video))
    return list_ids, list_titles, playlist_name


def merge_audio_files(ordered_list: list, output_file_name: str) -> None:
    """Given a list of ordered audio files, concatenate them using FFMPEG"""
    ffmpeg_arguments = ' -i "concat:'  # we concatenate all the provided files
    for audio in ordered_list:
        assert os.path.exists(
            audio+".mp3"), "Error, an audio file doesn't exist"
        ffmpeg_arguments += audio+'.mp3|'
    ffmpeg_arguments = ffmpeg_arguments[:-1]  # remove unecessary | symbol
    ffmpeg_arguments += '"'
    os.system('ffmpeg {0} "{1}.mp3"'.format(
        ffmpeg_arguments, output_file_name))


def download_playlist():
    """Main function"""
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

    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="playlist link")
    parser.add_argument("--playlist_name", help="Force name for the final playlist \
            or the directory in which files will be moved")
    parser.add_argument(
        "--delete_files", help="Delete downloaded audio files at the end of the program.\
        If left at default, will rename the files")
    args = parser.parse_args()
    playlist_url = args.url
    playlist_name = args.playlist_name
    if args.delete_files is None or args.delete_files in ('false', 'False', '0'):
        delete_files = False
    elif args.delete_files in ('true', 'True', '1'):
        delete_files = True
    else:
        raise TypeError("Couldn't convert delete_files value '{0}' to boolean".format(
            args.delete_files))

    # First, we create a list of IDs of video, so that if there is an issue with FFMPEG
    # we don't have to download everything again.
    video_ids_to_download, video_titles, playlist_name = videos_id(
        playlist_url, youtube_downloader, playlist_name, delete_files)

    # download audio here
    youtube_downloader.download(video_ids_to_download)

    # merge all audio files
    merge_audio_files(video_ids_to_download, playlist_name)

    if delete_files:
        for video_id in video_ids_to_download:
            os.system("rm {0}.mp3".format(video_id))
    else:  # rename
        os.makedirs(playlist_name)
        for i, video_id in enumerate(video_ids_to_download):
            os.system('mv {0}.mp3 "{1}/{2}.mp3"'.format(video_id, playlist_name, video_titles[i]))


if __name__ == '__main__':
    download_playlist()
