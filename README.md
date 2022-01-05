# pyvctrl
Python package to communicate with Viessmann heatings via the optolink serial interface. It is basically a simple wrapper for vcontrold/vclient.


## Auf Satellite

Mini-PC

    sudo apt-get install cmake git libc-dev-bin libc6-dev
    sudo apt-get install libxml2-dev python-docutils

    mkdir build
    cd build
    cmake ..
    make

Der USB-Adapter verbindet sich beim Einstecken (`dmesg | less`) direkt mit `/dev/ttyUSB0` (Treiber für CH341-UART Konverter ist bereits im Kernel installiert).
Dies sollte im finalen Aufbau mit dem RaspberryPi genauso sein.

Durch ein

    sudo make install

wird der vcontrold im System installiert:

    /usr/local/sbin/vcontrold
    /usr/local/bin/vclient

Dann die Konfigdateien

    /etc/vcontrold/vcontrold.xml
    /etc/vcontrold/vito.xml

mit den eigenen Dateien/Konfigs überschreiben. Gegebenenfalls die alte
Version vorher wegretten...

    sudo mkdir /etc/vcontrold
    sudo cp local_vcontrold.xml /etc/vcontrold/vcontrold.xml
    sudo cp local_vito.xml /etc/vcontrold/vito.xml

## Debug mode

Starte den vcontrold als

    vcontrold -g -v -n

für einen ersten Check ob die Konfigdateien auch wirklich gefunden werden.


## Erste Tests

Der vcontrold wurde mit Root-Rechten gestartet

    sudo vcontrold -v -n

da ansonsten der Zugriff auf `/dev/ttyUSB0` nicht gewährt wird.
Anschließend wurde in einem zweiten Terminal der Befehl

    vclient -c getVitoBetriebsart

ausprobiert, was mit dem Fehler

    SRV ERR: <RECV: read timeout
    ... (weitere 5 Zeilen)

quittiert wurde. Das scheint erstmal normal, wir haben uns ja noch gar nicht mit
dem Interface an der Vitodens verbunden.


## Vclient Befehle

Beispiele für `vclient` Befehle:

    root@heizung:~# vclient -c "setBetriebPartyM1 0"
    setBetriebPartyM1 0:
    OK
    root@heizung:~# vclient -c getBetriebPartyM1
    getBetriebPartyM1:
    0
    root@heizung:~# vclient -c "setBetriebPartyM1 1"
    setBetriebPartyM1 1:
    OK
    root@heizung:~# vclient -c getBetriebPartyM1
    getBetriebPartyM1:
    1

