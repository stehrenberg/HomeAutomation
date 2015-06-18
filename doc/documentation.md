#Projektdokumentation: Drei

Advanced Embedded Software Project    
Stephanie Ehrenberg, Markus Hornung, Simon Jahreiß, Luis Morales, Maximilian Pachl


## Motivation

Viele Studenten haben ein Anleigen an die Fachschaft unserer Faktultät. Damit die überarbrbeiteten, verkarterten Studenten nicht umsonst in die Fachschaft laufen und festestellen müssen, dass niemand da ist, soll die Präsenz der Fachschaftsmitglieder in Echtzeit auf einer Webseite und durch Leuchtsignale visualisiert werden. So ist eine effektiviere Zeitplanung möglich und die Noten werden automatisch besser.


## Anforderungen

* Automatische Präsenzerkennung (ohne Interaktion von Fachschaftsmitglied)
* Keine zusätzliche Software/Hardware für Fachschaftler von Nöten
* Webinterface zur Verwaltung
* Zeitnahe Visualisierung der Präsenz (Webseite wie Leuchtisgnale)
* Willkommensmelodie
* Audio-Visuelle Eindeutigkeit der Fachschaftler (Farbe der Leuchtsignale, Melodie beim Eintritt)
* Systemstatus von Außen ersichtlich


## Idee

Da eigentlich jedes Mitglied (höhö) der Fachschaft ein Smartphone hat, soll die Präsenzerkennung über die Wifi Schnitstelle realisiert werden. Dazu wird ein dedizierter Hotspot, der nur die Fachschaftsräume abdeckt, installiert. Um zu vermeiden das auf den Smartphones zusätzliche Software installiert werden muss, soll anhand der MAC-Adresse erkannt werden, ob das Telefon in das spezielle Wifi eingebucht ist und somit der Fachschaftler präsent ist.

Sobald ein Telefon sich ins Wifi einbucht, soll über die in den Fachschaftsräumen installierte Tonanlage die Willkommenmelodie des jeweiligen Telefoninhabers/Fachschaftlers abgespielt werden.

Zusätzlich wird neben der Fachschaftstür ein Leuchtsignal (PixelTube, ein Pixel) mit der vom User spezifizierten Farbe eingeschaltet. Beim Verlassen der Fachschaftsräume soll dieses Signal ausgeschaltet werden.

Durch eine Websocketverbindung auf der Fachschaftswebseite kann in fast Echtzeit die Präsenz der Mitglieder von überall eingesehen werden.


## Hardware Komponenten

* Raspberry Pi 2
* WLAN Stick für Hotspotfunktionalität
* ENTTEC DMX USB Pro (DMX Interface)
* Eurolite PixelTube 16 (Leuchtsignal)
* Laustprecher / Kopfhörer
* LEDs zur Visualisierung des Systemstatuses


## Software Design

Um möglichst effiziente Softwareentiwcklungszyklen zu realisieren wurde großen Wert drauf gelegt die einzelnen Komponenten soweit wie möglich von einander zu trennen.
Zum besseren Verständnis wurde die Architektur der Software in einer Grafik zusammen gefasst:

![System Overview](overview.png)

Der **Webserver**, der **Manager** und der **Wifi Crawler** kommunizieren mittels bi- und unidirektionaler **Pipes**.
Die **Peripheriesterung wurde als Library** ausgelegt und wir direkt vom Manager verwendet.     
Zwischen Client und Webserver besteht eine bidirektionale Websocketverbindung, damit Präsenzänderungen in fast-echtzeit auf der Fachschaftswebseite angezeigt werden können. Zusätzlich verwendet das **Verwaltungsinterface eine REST-Schnittstelle** um User hinzuzufügen und abzuändern.    
Zugriffe auf die **Datenbank wurden ebenfalls über eine Library gekapselt**.


### Wifi Crawler

#### Hotspot
Die Hotspotfunktionalität wir mit dem Tool **hostapd** und einem zweiten WLAN Stick realisiert. Zusätzlich wurde ein DHCP Server auf dem RaspbberyPi installiert der den Clients eigene IP Adressen gibt.

	$: apt-get install hostapd dhcpd
	
	
#### Cralwer

Um zu erkennen welcher User sich verbund hat, kommt das Tool **iwevent** zu einsatz. Dieses Tool zeigt alle Ereignisse, die im Hotspot passieren auf der Kommandozeile an. Diese Ausgaben werden von einem Python Programm geparsed und an den Manager weiter gegeben. Beispielhafte Ausgabe von iwevent:

	pi@192.168.188.26$: iwevent
	Waiting for wireless events...
	

### Manager

### Datenbank: SQlite

### Webserver: Flask

### Webinterface: AngularJS

### Peripheriesteuerung

#### SoundController

#### DMXController