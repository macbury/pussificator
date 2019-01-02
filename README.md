#### Requirements
OpenCV on Raspberry Pi

```bash
sudo apt-get install python2.7-dev python3-dev python3-opencv python3-pyqt5 libjasper-dev libatlas-base-dev libhdf5-dev libhdf5-serial-dev libqtgui4 libgomp1 libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libatlas-base-dev gfortran libqt4-test libatlas3-base libsz2 libharfbuzz0b libtiff5 libjasper1 libilmbase12 libopenexr22 libilmbase12 libgstreamer1.0-0 libavcodec57 libavformat57 libavutil55 libswscale4 libqtgui4 libqt4-test libqtcore4

sudo pip3 install -r requirements.txt

https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalcatface_extended.xml
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