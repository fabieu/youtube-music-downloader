# Youtube Music Downloader

The Youtube Music Downloader is a simple Command Line Interface written in Python to download YouTube videos and playlists and convert them into audio files (.mp3).

## Requirements

- Python 3.9 or higher

## Installation

Clone this repository to your machine

```bash
git clone https://github.com/fabieu/youtube-music-downloader
```

Move into the cloned repository

```bash
cd ./youtube-music-downloader
```

Installing required dependencies in a virtual environment:

```bash
python -m pip install pipenv
pipenv install
pipenv shell
```

## Usage

Run the Python script with

```bash
python main.py <arguments>
```

Argument List:

|        Argument        |           required/optional            | Description                              |
| :--------------------: | :------------------------------------: | ---------------------------------------- |
|    -playlist \<URL>    |  required if -video is not specified   | YouTube Playlist URL to download         |
|     -video \<URL>      | required if -playlist is not specified | YouTube Video URL to download            |
| -target \<output path> |                optional                | Directory for outputting converted files |
|       --version        |                optional                | Display version information              |

> Note: Escape all paths with quotes to prevent errors

### Example:

Downloading a playlist:

```bash
python main.py -playlist https://www.youtube.com/playlist?list=PLVRMKQHY0icxzX_WkE-s8_-YF_JAo_h92
```

Downloading a video to C:\temp\downloads

```bash
python main.py -video https://www.youtube.com/watch?v=HluANRwPyNo -target "C:\temp\downloads"
```
