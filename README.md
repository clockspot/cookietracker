# cookietracker
Clocking coworker cookie consumption

## How to use
Buy a Raspberry Pi. Give it an internet connection and put Python on it.

Wire up a button to GPIO pin 22 (Broadcom definition) and an LED to pin 20.

Set up a Google Analytics property, duplicate settings-sample.py as settings.py, and enter the property settings there. You can use whatever category, action, and label you like (I'm pretty sure).

Run cookietracker.py on the Pi, perhaps via a launcher script like launcher-sample.sh.

Ask your coworkers to press the button once for every cookie they take from the jar.

## Disclaimer
If you found this, you are responsible entirely for its use and the results thereof.

## Oh god how did this get here
I am not good with github