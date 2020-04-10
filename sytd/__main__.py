
import eel
from pathlib import Path
from tkinter import Tk, filedialog
import youtube_dl as yt
import configparser
from __init__ import __version__ as VERSION

# Variables
CONFIG_PATH = Path(__file__).cwd().joinpath('config.ini')
WEB_PATH = Path(__file__).cwd().joinpath('web')

eel.init(WEB_PATH)

@eel.expose
def download(url):
    try:
        ydl_opts = {'verbose': 'false',
                    'noplaylist': 'true',
                    'format': 'best',
                    'outtmpl': get_save_path() + '/%(title)s.%(ext)s',
                    'progress_hooks': [my_hook]
                    }
        with yt.YoutubeDL(ydl_opts) as ydl:
            eel.update_status('Downloading . . .')
            ydl.download([url])

        eel.update_status('Download completed successfully ✔️')

    except:
        print('An error occured! Please check your URL. ❌')
        eel.update_status('An error occured! Please check your URL. ❌')

# updates the progress bar as the download goes on
def my_hook(d):
    total_bytes = int(d['total_bytes'])
    downloaded_bytes = int(d['downloaded_bytes'])
    percentage = round((downloaded_bytes / total_bytes) * 100)
    eel.update_progressbar(percentage)

@eel.expose
def open_dir_browser():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    folder = filedialog.askdirectory().replace('\\', '/')  # open directory selector

    config = configparser.ConfigParser()    # write selected directory to config
    config.read(CONFIG_PATH)
    config['MAIN']['save_path'] = folder
    with open(CONFIG_PATH, 'w') as configfile:
        config.write(configfile)
    update_status_output()

# return the current output path
def get_save_path():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    path = config['MAIN']['save_path']
    return path

# change output path on the status text field
def update_status_output():
    eel.update_status('Output: ' + get_save_path())

# checks if config file exists. if not creates it
def check_config():
    if not CONFIG_PATH.exists():
        print('missing config.ini, creating new')
        with open(CONFIG_PATH, 'a') as f:
            f.write('[MAIN]\n')
            f.write('save_path = ')

def main():
    check_config()
    update_status_output()
    eel.update_version_badge(VERSION)
    try:
        eel.start('main.html', mode='chrome')
    except (SystemExit, KeyboardInterrupt):
        pass

if __name__ == '__main__':
    main()
