# Playlist Downloader

## Dependencies

- `ffmpeg` is required to merge the audio files. On ArchLinux, use 
```bash
# pacman -S ffmpeg
```

- `youtube_dl` python package is required. In a virtual environment, `pip install youtube_dl`.


## Usage

```bash
./download_playlist.py https://youtube_playlist_link "name_to_save_the_playlist_to"
```
