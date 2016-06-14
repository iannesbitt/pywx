# pywx
## An embarassingly simple Wunderground webcam image getter and uploader
Currently supports local USB webcams (via imagesnap) and [Wunderground](https://www.wunderground.com/webcams/signup.html) as an endpoint. Relatively easy to install using the OS X command line.

#### Requirements
  - [Python 2.7.11](https://www.python.org/downloads/release/python-2711/) or [Python 3.5.1](https://www.python.org/downloads/release/python-351/)
  - [ImageSnap v0.2.5](http://iharder.sourceforge.net/current/macosx/imagesnap/)
    - Recommended install using [Homebrew](https://brew.sh)
  - [six v1.10.0](https://pypi.python.org/pypi/six/1.10.0)
    - `pip install six`
  - [future v0.15.2](https://pypi.python.org/pypi/future/0.15.2)
    - `pip install future`

#### Setup
  - **Download and unzip** ***pywx*** to the machine you intend to run on (your home directory `~/` would be fine).
  - **Install ImageSnap** using [Homebrew](https://brew.sh).
    - `brew install imagesnap`
  - **Determine which camera to use**.
    - `imagesnap -l` lists camera choice options.
    - Choose carefully so you don't end up with selfies of your desk chair on Wunderground from your backward-facing built-in iSight or FaceTime Camera. (If you're unsure which is the one you want, test each device with `imagesnap -d 'device name' ~/device_name_test.jpg`, then `open ~/device_name_test.jpg`.)
    - Copy the camera listing you want (without trailing whitespace) to the "device" definition in settings.json. The default is `"device": "USB2.0 PC CAMERA"` but you can change it to whichever device you want, eg. `"device": "iSight"`.
  - **Copy your Weather Underground webcam FTP credentials to settings.json**.
    - ***No, this is not secure.*** I recommend running `chmod 600 settings.json` (run as yourself, not root) so that only you can read and write to this file. I also recommend changing your Weather Underground password to something completely unique from all other passwords you use, so that a potential attacker who obtains this information is not able to use it for any other (potentially more important) locations than Wunderground. Sorry about that, you've been warned. **If you're really concerned about it, let me know and I will come up with a safer storage method.**
  - **Update your crontab to run pywx every x minutes**.
    - Run `crontab -e` as yourself (not root) which will open your cron scheduler in the vim editor (unless, like me, you've changed your default editor to nano)
    - Add the following line, replacing x with an integer >= 1 (your script will run every x minutes): `*/x * * * * ~/pywx/pywx_run cap.Actions.all`
      - Obviously, if you don't unzip pywx to your home folder (`~/`), you'll need to replace the path with the location of the root pywx folder.
      - If you'd like a log to be kept, you can modify the cron job to append the print output of the program to a file like the following: `*/x * * * * ~/pywx/pywx_run cap.Actions.all >> ~/pywx/pywx.log` 
    - Save the crontab file and quit the editor.
  - Go to your Wunderground webcam page and check that everything has worked.
  - Report bugs!

#### Future plans
  - Add security to login credentials.
  - Automate the finding of non-iSight and non-FaceTime cameras.
  - Add support for IP cameras.
  - Add automation to setup process.
