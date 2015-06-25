#Projektdokumentation: Drei

Advanced Embedded Software Project    
Stephanie Ehrenberg, Markus Hornung, Simon Jahreiß, Luis Morales, Maximilian Pachl


## Motivation

Viele Studenten haben ein Anliegen an die Fachschaft unserer Faktultät. Damit die überarbeiteten, verkaterten Studenten nicht umsonst in die Fachschaft laufen und feststellen müssen, dass niemand da ist, soll die Präsenz der Fachschaftsmitglieder in Echtzeit auf einer Webseite und durch Leuchtsignale visualisiert werden. So ist eine effektivere Zeitplanung möglich und die Noten werden automatisch besser.


## Anforderungen

* Automatische Präsenzerkennung (ohne Interaktion von Fachschaftsmitglied)
* Keine zusätzliche Software/Hardware für Fachschaftler von Nöten
* Webinterface zur Verwaltung
* Zeitnahe Visualisierung der Präsenz (Webseite wie Leuchtsignale)
* individuelle Willkommensmelodie
* Audio-Visuelle Eindeutigkeit der Fachschaftler (Farbe der Leuchtsignale, Melodie beim Eintritt)
* Systemstatus von Außen ersichtlich


## Idee

Da eigentlich jedes Mitglied der Fachschaft ein Smartphone hat, soll die Präsenzerkennung über die Wifi Schnitstelle realisiert werden. Dazu wird ein dedizierter Hotspot, der nur die Fachschaftsräume abdeckt, installiert. Um zu vermeiden, dass auf den Smartphones zusätzliche Software installiert werden muss, soll anhand der MAC-Adresse erkannt werden, ob das Telefon in das spezielle Wifi eingebucht ist und somit der Fachschaftler präsent ist.

Sobald ein Telefon sich ins Wifi einbucht, soll über die in den Fachschaftsräumen installierte Tonanlage die Willkommenmelodie des jeweiligen Telefoninhabers/Fachschaftlers abgespielt werden.

Zusätzlich wird neben der Fachschaftstür ein Leuchtsignal (PixelTube, ein Pixel) mit der vom User spezifizierten Farbe eingeschaltet. Beim Verlassen der Fachschaftsräume soll dieses Signal ausgeschaltet werden.

Durch eine Websocketverbindung auf der Fachschaftswebseite kann nahezu in Echtzeit die Präsenz der Mitglieder von überall eingesehen werden.


## Hardware Komponenten

* Raspberry Pi 2
* WLAN Stick für Hotspotfunktionalität
* ENTTEC DMX USB Pro (DMX Interface)
* Eurolite PixelTube 16 (Leuchtsignal)
* Laustprecher / Kopfhörer
* LEDs zur Visualisierung des Systemstatuses


## Software Design

Um möglichst effiziente Softwareentwicklungszyklen zu realisieren, wurde großer Wert auf eine maximal modulare Entwicklung der einzelnen Komponenten gelegt.
Die folgende Grafik veranschaulicht den Architekturentwurf:

![System Overview](overview.png)

Der **Webserver**, der **Manager** und der **Wifi Crawler** kommunizieren mittels bi- und unidirektionaler **Pipes**.
Die **Peripherie-Steuerung wurde als Library** ausgelegt und wird direkt vom Manager verwendet.
Zwischen Client und Webserver besteht eine bidirektionale Websocketverbindung, damit Präsenzänderungen in Fast-Echtzeit auf der Webseite der Fachschaft angezeigt werden können.
Zusätzlich verwendet das **Verwaltungsinterface eine REST-Schnittstelle**, um User hinzufügen und abändern zu können.
Zugriffe auf die **Datenbank wurden ebenfalls über eine Library gekapselt**.


### Wifi Crawler

#### Hotspot
Die Hotspotfunktionalität wird mit dem Tool **hostapd** und einem zweiten WLAN Stick realisiert. Zusätzlich wurde ein DHCP Server auf dem RaspbberyPi installiert, der den Clients eigene IP Adressen gibt.

	# Installation der benötigten Tools
	$: apt-get install hostapd dhcpd
	
	# Konfiguration von hostapd
	$: cat /etc/hostapd/hostapd.conf
	interface=wlan1
	driver=rtl871xdrv
	ssid=Horst    
	hw_mode=g
	channel=6
	macaddr_acl=0
	auth_algs=1
	ignore_broadcast_ssid=0
	wpa=2
	wpa_passphrase=goto_fail
	wpa_key_mgmt=WPA-PSK
	wpa_pairwise=TKIP
	rsn_pairwise=CCMP
	
Mit der oben angegebenen Konfiguration stellt das RaspberryPi einen Hotspot mit der SSID "Horst" und dem WPA2 Passphrase "goto_fail" zur Verfügung.
	
Im Produktivsystem müsste noch eine **Netzwerkbrücke** zwischen dem Wifi- und dem Ethernetinterface erstellt werden, damit Geräte, die mit dem Raspberry Hotspot verbunden sind, auch weiterhin Internetzugriff haben.
	
#### Crawler

Um zu erkennen, welcher User sich verbunden hat, kommt das Tool **iwevent** zum Einsatz. Dieses Tool zeigt alle Ereignisse, die im Hotspot passieren auf der Kommandozeile an. Diese Ausgaben werden von einem Python Programm **geparsed** und an den Manager weiter gegeben. Beispielhafte Ausgabe von iwevent:

	pi@192.168.188.26$: iwevent
	Waiting for Wireless Events from interfaces...
	07:33:44.994303   wlan1    Registered node:8C:3A:E3:17:DF:6C
	07:33:48.866077   wlan1    Expired node:8C:3A:E3:17:DF:6C
	
Glücklicherweise kann iwevent auch als unprevilegierter Benutzer verwendet werden, somit ist es nicht nötig dieses Teil der Anwendung mit Root Rechten laufen zu lassen.


### Statusanzeige GPIO

Zur Anzeige des Systemstatuses wurden zwei LEDs an das GPIO Interface des Raspberry Pis angeschlossen. Eine der beiden Leds zeigt den Start des Managers an. Sie erlischt beim Beenden des Managers.
Die zweite LED visualisiert den Zustand des Wifi Crawlers. Zusätzlich blinkt die LED kurz, wenn ein User sich ins WLAN eingeloggt oder es verlassen hat.

Um zu vermeiden, dass die einzelnen Dienste mit Rootrechten laufen müssen, wurde zur Ansteuerung der GPIOs das **sysfs** Interface verwendet. Dank des Filesystem Mappings ist es möglich, über simple Dateisystemberechtigungen auch unprivilegierten  Nutzern die Verwendung der GPIOs zu erlauben.


### Manager

### Datenbank: SQlite

### Webserver: Flask

### Webinterface: AngularJS

### Peripheriesteuerung

#### SoundController

#### DMXController