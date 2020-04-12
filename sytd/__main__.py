import os
import eel
from pathlib import Path
from tkinter import Tk, filedialog
import youtube_dl as yt
import configparser
from threading import Thread
from sytd import __version__ as version

# setup eels root folder and config location
web_location = 'web'
web_path = os.path.dirname(os.path.realpath(__file__)) + '/' + web_location
eel.init(web_path)

config_location = 'config.ini'
config_path = os.path.dirname(os.path.realpath(__file__)) + '/' + config_location

# starts the download function in a thread
@eel.expose
def download(url):
    t = Thread(target=download_thread, args=(url,))
    t.start()

# actual downloading function
def download_thread(url):
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

# opens a explorer window to select output directory
@eel.expose
def open_dir_browser():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    folder = filedialog.askdirectory()  # open directory selector

    config = configparser.ConfigParser()    # write selected directory to config
    config.read(config_path)
    config['MAIN']['save_path'] = folder
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    update_status_output()

# return the current output path
def get_save_path():
    config = configparser.ConfigParser()
    config.read(config_path)
    path = config['MAIN']['save_path']
    return path

# change output path on the status text field
@eel.expose
def update_status_output():
    eel.update_status('Output: ' + get_save_path())

@eel.expose
def update_version_badge():
    eel.update_version_badge('v' + version)

# checks if config file exists. if not creates it
def check_config():
    if not os.path.isfile(config_path):
        print('missing config.ini, creating new')
        with open(config_path, 'a') as f:
            f.write('[MAIN]\nsave_path = \n')

def run():
    check_config()
    try:
        eel.start('main.html', mode='chrome', port=0, size=(600, 800))
    except (SystemExit, KeyboardInterrupt):
        pass

if __name__ == '__main__':
    run()
