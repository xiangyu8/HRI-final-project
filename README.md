Paper link: https://dl.acm.org/doi/abs/10.1145/3371382.3378355

## Installation
### 1. Install Cozmo SDK: (official instruction can be found here http://cozmosdk.anki.com/docs/install-macos.html)
```
pip3 install --user 'cozmo[camera]'
```
### 2. Install Speech Recognition: (instruction: https://forums.anki.com/t/controlling-cozmo-via-voice-commands/1183)
```
pip3 install --global-option='build_ext' --global-option='-I/usr/local/include' --global-option='-L/usr/local/lib' pyaudio
pip3 install pyaudio
pip3 install SpeechRecognition
```
### 3. Install Face Recognition: (https://github.com/ageitgey/face_recognition)
1) install dlib:(https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf)
```
git clone https://github.com/davisking/dlib.git
cd dlib
mkdir build; cd build; cmake ..; cmake --build .
cd ..
python3 setup.py install
```
2) install face_recognition:
```
pip3 install face_recognition
```

### 4. Android Debug Bridge:(http://cozmosdk.anki.com/docs/adb.html)
```
brew tap caskroom/cask
brew cask install android-platform-tools
```

### 5. Final Installation: (http://cozmosdk.anki.com/docs/adb.html#final-installation-all-platforms)
1)Enable USB Debugging on your phone.
***Tap seven (7) times on the Build Number listed under Settings -> About Phone.
***Then, under Settings -> Developer Options, enable USB debugging.
2)Confirm devices connected:
```
adb devices
```

## Get started with Cozmo(http://cozmosdk.anki.com/docs/getstarted.html)
1) Plug the mobile device containing the Cozmo app into your computer.
2) Open the Cozmo app on the phone. Make sure Cozmo is on and connected to the app via WiFi.
3) Tap on the gear icon at the top right corner to open the Settings menu.
4) Swipe left to show the Cozmo SDK option and tap the Enable SDK button.
5) Download this .py file.
6) Execute this .py file on your terminal.
```
python3 faceScaffolding.py
```
