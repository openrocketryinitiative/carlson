## Get the library
`git clone https://github.com/richardghirst/PiBits.git`

## Install the servoblaster stuff
```
cd PiBits/ServoBlaster/user
sudo make install
```

## Launch the servoblaster script
`sudo ./servod --p1pins="11,13,15"`

Servos should be connected to pins 11, 13, 15 (which correspond to GPIO 17, 27, 22)

## set the servos
```
echo 0=1500us > /dev/servoblaster
echo 1=1500us > /dev/servoblaster
echo 2=1500us > /dev/servoblaster
```
