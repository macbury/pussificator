#### Requirements
OpenCV on Raspberry Pi

```bash
sudo apt-get install python2.7-dev python3-dev python3-pyqt5 libjasper-dev libatlas-base-dev

sudo pip3 install -r requirements.txt
```

## Example systemd service file

```bash
sudo cp systemd/*.service /lib/systemd/system/
sudo systemctl enable led
sudo systemctl start led

sudo systemctl enable servo
sudo systemctl start servo

sudo systemctl enable pussy
sudo systemctl start pussy
```

### References

* https://github.com/timatooth/catscanface
* https://learn.adafruit.com/adafruit-neopixel-uberguide/python-circuitpython
* https://gist.github.com/obfusk/208597ccc64bf9b436ed
* https://www.slideshare.net/seonghunchoe7/installing-tensorflow-object-detection-on-raspberry-pi