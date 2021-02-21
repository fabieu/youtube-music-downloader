import pytube
import os
import sys
import re
import shutil
import logging
import contextlib
import atexit
import ffmpeg

# Default configuration if -target or -temp is not specified
temp_dir = "temp"
target_dir = "downloads"

# Default logging Configuration
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s %(levelname)s %(message)s'
)


# Main function for handling command line arguments and program sequence
def main():
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    if "--version" in opts:
        print("Youtube Music Downloader v1.0.0\n\u00a9 2021 - Fabian Eulitz")

    if "-target" in opts:
        global target_dir
        target_dir = os.path.abspath(args[opts.index("-target")])

    if "-playlist" in opts and "-video" not in opts:
        download_playlist(args[opts.index("-playlist")])
    elif "-video" in opts and "-playlist" not in opts:
        download_video(args[opts.index("-video")])
    else:
        raise SystemExit(f'Usage: {sys.argv[0]} (-playlist | -video) <URL> [-target <"path">] [--version] ')

    cleanup()


# Function for downloading and converting a single Youtube video
def download_video(video_url):
    try:
        pytube_video = pytube.YouTube(video_url)

        stream = pytube_video.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
        video_filename = stream.default_filename
        audio_filename = re.search('(.*).mp4', stream.default_filename).group(1) + '.mp3'

        # Download and convert youtube video if it doesnt already exists
        if not file_exists(audio_filename):
            logging.info('Downloading and converting: ' + pytube_video.title)

            stream.download(temp_dir)
            create_dir(target_dir)

            input = ffmpeg.input(os.path.abspath(os.path.join(temp_dir, video_filename)))
            output = ffmpeg.output(input.audio, os.path.abspath(os.path.join(target_dir, audio_filename)))
            output.run(quiet=True)
        else:
            logging.warning(f"{audio_filename} already exists - will be skipped.")

    except pytube.exceptions.VideoPrivate:
        logging.warning(f'"{video_url}" is private - will be skipped.')

    except pytube.exceptions.RegexMatchError:
        logging.error(f'"Video-URL: {video_url}" is invalid!')


# Check if audio file is already present in target_dir
def file_exists(audio_filename):
    fname = os.path.abspath(os.path.join(target_dir, audio_filename))
    return os.path.isfile(fname)


# Creates target_dir if it doesnt exist
def create_dir(target_dir):
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)


# Helper function for downloading entire Youtube playlists
def download_playlist(playlist_url):
    try:
        pytube_playlist = pytube.Playlist(playlist_url)

        # Suppress output of pytube playlist generator
        with contextlib.redirect_stdout(None):
            playlist_size = sum(1 for _ in pytube_playlist.video_urls)

        if playlist_size > 0:
            for video_url in pytube_playlist.video_urls:
                download_video(video_url)
        else:
            logging.warning('No videos detected in "' + pytube_playlist.title + '"')

    except pytube.exceptions.RegexMatchError:
        logging.error(f'"Playlist-URL: {playlist_url}" is invalid!')


# Removes temporary directory
@atexit.register
def cleanup():
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
