# Playlist Downloader

## Dependencies

- [`youtube_dl`](https://pypi.org/project/youtube_dl/) python package is required. In a virtual environment, `pip install youtube_dl`.

- Optionnal: `ffmpeg` if you want to merge the audio files. On ArchLinux, use
```sudo-bash
# pacman -S ffmpeg
```

## Usage

```bash
./download_playlist.py https://youtube_playlist_link --playlist_name "name_to_save_the_playlist_to" --delete_files=False
```

- `playlist_name`: By default, the playlist name will be the same as the one on Youtube.
It will also be the name ofthe folder in which audio files will be kept if `delete_files=False`

- `delete_files`: By default, will keep downloaded audio files.
If set to `True`, will merge all songs into one using ffmpeg and delete the downloaded files.
