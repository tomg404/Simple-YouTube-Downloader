from __future__ import unicode_literals

"""
Main function of this project.
Code Style: Black (Please continue with Black if contributing)
(c) Tom Gaimann, 2020
"""
import os
import eel
import sys
import json
import datetime
import configparser
import urllib.request
import youtube_dl as yt
from pathlib import Path
from threading import Thread
from . import __version__ as VERSION
from distutils.version import LooseVersion

try:  # check if tkinter is present. if not print error
    from tkinter import Tk, filedialog
except ImportError:
    print("Error: tkinter not found")
    print("On linux you can install tkinter by executing:")
    print("sudo apt-get install python3-tk")

# basic logger
class MyLogger(object):
    def __init__(self):
        pass

    def debug(self, msg):
        # print(msg)
        pass

    def warning(self, msg):
        # print(msg)
        pass

    def error(self, msg):
        print(msg)


# setup eels root folder and config location
web_location = "web"
web_path = os.path.dirname(os.path.realpath(__file__)) + "/" + web_location
eel.init(web_path)

# setup config path
config_location = "config.ini"
config_path = os.path.dirname(os.path.realpath(__file__)) + "/" + config_location


# actual downloading function
@eel.expose
def download(url):
    # YouTube_dl options
    ydl_opts = {
        "verbose": "true",
        "noplaylist": "true",
        "format": "best",
        "outtmpl": get_save_path() + "/%(title)s.%(ext)s",
        "progress_hooks": [hook],
        "logger": MyLogger(),
    }

    try:
        with yt.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    except KeyboardInterrupt:
        print("KeyboardInterrupt. ❌")
        eel.update_status("KeyboardInterrupt. ❌")
        sys.exit(0)

    except yt.utils.DownloadError:
        print("Not a valid URL. ❌")
        eel.update_status("Not a valid URL. ❌")


# updates the progress bar as the download goes on
def hook(d):
    try:
        total_bytes = int(d["total_bytes"])
        downloaded_bytes = int(d["downloaded_bytes"])
        percentage = round((downloaded_bytes / total_bytes) * 100)
        eel.update_progressbar(percentage)

        eel.update_status("")

        if d["status"] == "downloading":
            try:
                filename = os.path.basename(d["filename"])
                speed = round(d["speed"] / 1000000, 2)  # speed in mb/s
                elapsed_time = datetime.timedelta(
                    seconds=round(d["elapsed"])
                )  # elapsed time
                estimated_time = datetime.timedelta(seconds=d["eta"])  # estimated time
            except TypeError:
                speed = 0  # backup values because the above ones sometimes fail
                elapsed_time = 0
                estimated_time = 0

            eel.update_status(
                "Downloading ...\nSpeed: {:.2f} mb/s | {} / {}".format(
                    speed, elapsed_time, estimated_time
                )
            )

        if d["status"] == "finished":
            eel.update_status("Download completed successfully ✔️")

    except KeyError:
        print("Video probably already exists. ❌")
        eel.update_status("Video probably already exists. ❌")


# opens a explorer window to select output directory
@eel.expose
def open_dir_browser():
    root = Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    folder = filedialog.askdirectory()  # open directory selector

    config = configparser.ConfigParser()  # write selected directory to config
    config.read(config_path)
    config["MAIN"]["save_path"] = folder
    with open(config_path, "w") as configfile:
        config.write(configfile)
    update_status_output()


# return the current output path
def get_save_path():
    config = configparser.ConfigParser()
    config.read(config_path)
    path = config["MAIN"]["save_path"]
    return path


# change output path on the status text field
@eel.expose
def update_status_output():
    eel.update_status("Output: " + get_save_path())


# updates version badge with current version (gets called in html body onload)
@eel.expose
def update_version_badge():
    eel.update_version_badge("v" + VERSION)


# checks if config file exists. if not creates it
def check_config():
    if not os.path.isfile(config_path):
        print("missing config.ini, creating new")
        with open(config_path, "a") as f:
            f.write("[MAIN]\nsave_path = \n")


# check if a new version of sytd is available on pypi
def check_for_update():
    current_version = VERSION
    latest_version = ""
    url = "https://pypi.org/pypi/sytd/json"  # pypi json url
    try:
        with urllib.request.urlopen(url) as request:
            latest_version = json.loads(request.read().decode())["info"]["version"]
    except:
        pass

    if LooseVersion(current_version) < LooseVersion(latest_version):
        print("Version {} of sytd is available!".format(latest_version))
        eel.show_update_available()


# close program when closing window
def close(path, sockets):
    print("Bye...")
    sys.exit(0)


# main function
def run():
    check_config()
    check_for_update()
    try:
        eel.start(
            "main.html", mode="chrome", port=0, size=(600, 840), close_callback=close
        )
    except (SystemExit, KeyboardInterrupt):
        pass
    except OSError:
        print(
            "Chrome is required to run this program. Install chrome here: "
            "https://www.google.com/chrome/"
        )


if __name__ == "__main__":
    run()
