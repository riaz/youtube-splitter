# youtube-splitter
A cli app to split youtube video into audio and video


### Pre-req when runnign on macosx

    brew install fprobe
    brew install ffmpeg


### Running this program

    git clone git@github.com:riaz/youtube-splitter.git
    poetry install
    (In vscode) point the interpreter to the environment that poetry creates so that the dev and package env in sync
    python main.py <your_youtube_video_of_choice>
