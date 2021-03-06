# pywx
## An embarassingly simple Wunderground webcam image getter and uploader
Currently supports local USB webcams (via imagesnap) and [Wunderground](https://www.wunderground.com/webcams/signup.html) as an endpoint. Relatively easy to install using the OS X or Linux command line.

#### Requirements
  - [Python 2.7.11](https://www.python.org/downloads/release/python-2711/) or [Python 3.5.1](https://www.python.org/downloads/release/python-351/)
  - [pillow v3.2.0](https://pypi.python.org/pypi/Pillow/3.2.0)
    - `pip install pillow`
  - [six v1.10.0](https://pypi.python.org/pypi/six/1.10.0)
    - `pip install six`
  - [future v0.15.2](https://pypi.python.org/pypi/future/0.15.2)
    - `pip install future`
  - On Mac: [ImageSnap v0.2.5](http://iharder.sourceforge.net/current/macosx/imagesnap/)
    - Recommended install using [Homebrew](https://brew.sh)
  - On Linux: [fswebcam](https://www.sanslogic.co.uk/fswebcam/)
    - Available on Aptitude, the Linux package manager

#### Setup
  - **Download and unzip** ***pywx*** to the machine you intend to run on (a folder in your home directory `~/pywx` would be fine).
  - On Mac: **Install ImageSnap** using [Homebrew](https://brew.sh).
    - `brew install imagesnap`
  - On Linux: **Install fswebcam** using `apt-get`
    - `sudo apt-get install fswebcam`
  - **Install other requirements** using pip
    - `pip install pillow && pip install six && pip install future`
  - **Determine which camera to use**.
    - `imagesnap -l` lists camera choice options on Mac, and `lsusb` will list all connected USB devices on Linux. If your device does not show up by name, you can check the instructions [here](http://ask.xmodulo.com/install-usb-webcam-raspberry-pi.html) but you may need to buy something that is compatible.
    - If you're on a Mac, choose carefully so you don't end up with selfies of your desk chair on Wunderground from your backward-facing built-in iSight or FaceTime Camera. (If you're unsure which is the one you want, test each device with `imagesnap -d 'device name' ~/device_name_test.jpg`, then `open ~/device_name_test.jpg`.)
    - Copy the camera listing you want (without trailing whitespace) to the "device" definition in settings.json. The default is `"device": "USB2.0 PC CAMERA"` which is how my camera ended up showing up with `lsusb`, but you can change it to whichever connected device you want, eg. `"device": "iSight"`.
  - **Copy your Weather Underground webcam FTP credentials to settings.json**.
    - ***No, this is not secure.*** I recommend running `chmod 600 settings.json` (run as yourself, not root) so that only you can read and write to this file. I also recommend changing your Weather Underground password to something completely unique from all other passwords you use, so that a potential attacker who obtains this information is not able to use it for any other (potentially more important) locations than Wunderground. Sorry about that, you've been warned. **If you're really concerned about it, let me know and I will come up with a safer storage method.**
  - Optional: Set the `img_text` field in the json to a custom string that will display after date and time at the top of your image. Character limit depends on the xy size of your webcam image. (Using ImageSnap I can fit 43 characters to the right of a 20-character date/timestamp on a 640 x 480 image.) When using `fswebcam`, the character limit is different as the program gives you an option for a nice banner. The `img_text` field will automatically add text to the fswebcam banner if you're using Linux.
  - **Update your crontab to run pywx every x minutes**.
    - Run `crontab -e` as yourself (not root) which will open your cron scheduler in the vim editor (unless, like me, you've changed your default editor to nano)
    - Add the following line, replacing x with an integer >= 1 (your script will run every x minutes): `*/x * * * * ~/pywx/pywx_run cap.Actions.all 2>&1` (the `2>&1` bit tells the cron emailer not to email you the logs, which is nice considering it runs every minute.)
      - Obviously, if you don't unzip pywx to your home folder (`~/`), you'll need to replace the path with the location of the root pywx folder.
      - If you'd like a log to be kept, you can modify the cron job to append the print output of the program to a file like the following: `*/x * * * * ~/pywx/pywx_run cap.Actions.all >> ~/pywx/pywx.log 2>&1`
    - Save the crontab file and quit the editor.
  - Go to your Wunderground webcam page and after a few minutes check that everything has worked.
  - Report bugs!

#### Known bugs
  - If you are running OS X and have a homebrew-installed version of Python, you will need to change the shebang (look it up) at the beginning of both `pywx_run` and `pywx/cap.py` from `#!/usr/bin/python` to `#!/usr/local/bin/python`.
  - [ImageSnap sometimes likes to remain as a running process in the queue](http://iharder.sourceforge.net/current/macosx/imagesnap/#comment-509757035), taking up gobs of memory and process threads, and making `top -u` just look like a list of times pywx has called imagesnap. I'm not sure why this happens, but I've noticed that if left unchecked, it quickly prevents the cron job from starting at all. (No logs, no images, no upload.) My hacky fix for this would no doubt be frowned upon greatly by Apple, but it does the job. I created another cron job that runs on the same schedule as pywx that effectively kills the imagesnap instance a reasonable amount of time after it is called. It looks something like `*/x * * * * sleep 20 && killall -15 imagesnap` (you could also add these commands to the end of your first cron job using &&). Basically, it waits 20 seconds, then kills all imagesnap instances. Crude, possibly dangerous, discouraged by Apple, but it's all I've got right now. I welcome any more creative, safe input to resolve this issue. It's possible because it's on Imagesnap's end that a new release would fix it. I'm not holding my breath.

#### Future plans
  - Add security to login credentials.
  - Automate the finding of non-iSight and non-FaceTime cameras.
  - Add support for IP cameras.
  - Add automation to setup process.
