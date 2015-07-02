---
title: Projektdokumentation Drei
author: Stephanie Ehrenberg, Markus Hornung, Simon Jahreiß, Luis Morales, Maximilian Pachl
geometry: margin=1in
abstract: Viele Studenten haben ein Anliegen an die Fachschaft unserer Faktultät. Damit die überarbeiteten, verkaterten Studenten nicht umsonst in die Fachschaft laufen und feststellen müssen, dass niemand da ist, soll die Präsenz der Fachschaftsmitglieder in Echtzeit auf einer Webseite und durch Leuchtsignale visualisiert werden. So ist eine effektivere Zeitplanung möglich und die Noten werden automatisch besser.
---


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

\pagebreak

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
	
Glücklicherweise kann iwevent auch als **unprevilegierter Benutzer** verwendet werden, somit ist es nicht nötig dieses Teil der Anwendung mit Root Rechten laufen zu lassen.

\pagebreak

### Statusanzeige GPIO

Zur Anzeige des Systemstatuses wurden zwei LEDs an das GPIO Interface des Raspberry Pis angeschlossen. Eine der beiden Leds zeigt den Start des Managers an. Sie erlischt beim Beenden des Managers.
Die zweite LED visualisiert den Zustand des Wifi Crawlers. Zusätzlich blinkt die LED kurz, wenn ein User sich ins WLAN eingeloggt oder es verlassen hat.

Um zu vermeiden, dass die einzelnen Dienste mit Rootrechten laufen müssen, wurde zur Ansteuerung der GPIOs das **sysfs** Interface verwendet. Dank des Filesystem Mappings ist es möglich, über simple Dateisystemberechtigungen auch unprivilegierten  Nutzern die Verwendung der GPIOs zu erlauben.


### Manager

### Datenbank: SQlite

### Webserver: Flask

Der Webserver wurde mit Hilfe von Flask implementiert. Er ist für die Bereitstellung des Webinterfaces, der REST-Schnittstellen und Websockets verantwortlich. Der Webserver ist standardmäßig unter der Adresse **http://localhost:8080** verfügbar.

Zur Kommunikation mit dem Manager wurden zwei Pipes eingerichtet. Eine Pipe dient zur Nachrichtenübermittlung an den Manager und eine zum Nachrichtenempfang vom Manager. Erstere dient zur Umstellung der über den Websocket empfangenen Lichtfarbe. Diese wird vom Webserver über den Websocket empfangen und an den Manager weitergeleitet, der daraufhin das Licht in der entsprechenden Farbe anschaltet. Die Pipe zum Nachrichtenempfang vom Manager wird genutzt, um Änderungen an den aktiven Benutzern zu empfangen. Als Datenquelle verwendet der Webserver direkt die SQLite Datenbank mit Hilfe des **SQLiteWrapper**s, welcher bereits zuvor vorgestellt wurde.

Die Bereitstellung der Dateien des Webinterfaces wird durch den in Flask intergrierten Webserver übernommen. Dieser stellt alle Dateien unter **static** zur Verfügung. Details zum Webinterface können dem nachfolgenden Punkt entnommen werden.

Die REST-Schnittstelle wurde mit Hilfe der Standardfunktionalität von Flask umgesetzt. Nachfolgende REST-Endpunkte existieren:

URL des Endpunkts				HTTP-Methode	Beschreibung
---------------------------   	------------	----------------
/api/users						GET 			Gibt eine Liste aller Benutzer zurück
/api/Sounds						GET 			Liefert eine Liste aller verfügbaren Sounds zurück
/api/users 						POST 			Legt den als Parameter übergebenen Benutzer an
/api/users/\<string:user_id\>	PUT 			Aktualisiert den Benutzer mit der
												User-Id **\<string:user_id\>**
/api/users/\<string:user_id\>	DELETE			Löscht den Benutzer mit der User-Id
												**\<string:user_id\>**
---------------------------   	------------	----------------

Der zur Verfügung gestellte Websocket-Endpunkt wurde mit der Flask-Erweiterung **flask.ext.socketio** implementiert. Sobald ein Client die Verbindung zu diesem Websocket aufbaut, wird ein Event namens **Connected** ausgelöst. Der Client kann daraufhin folgende zwei Events an den Server senden.

Event 				Beschreibung
----------			----------------
GetActiveUsersEvent	Liefert eine Liste aller aktiven Benutzer zurück
LatencyColorEvent	Nimmt eine Farbe entgegen und setzt reicht diese an den Manager weiter,
					damit dieser ein Licht mit der entsprechenden Farbe anschaltet. Des
					weiteren sendet der Server bei jeder Änderung der Liste mit aktiven
					Usern ein Event namens **ActiveUsersNotification**, welches zusätzlich
					eine Liste der aktiven User enthält. Sobald sich also ein Benutzer
					in das WiFi einloggt oder das WiFi verlässt, wird dieses Event vom
					Server an alle Clients gebroadcasted.


### Webinterface: AngularJS

Das Webinterface wird über den Webserver bereitgestellt und kann unter **http://localhost:8080/static/drei.html** abgerufen werden. Es handelt sich dabei um eine mit AngularJS entwickelte JavaScript-App, welche die zuvor vorgestellten REST- und Websocket-Endpunkte nutzt.

Die Entwicklung des Webinterfaces geschieht mit der von **yo-angular** bereitsgestellten Build-Umgebung in einem Verzeichnis außerhalb des Python-Entwicklungspfads. Nachdem ein Entwicklungspunkt erreicht wurde, welcher auf dem Webserver bereitgestellt werden soll, so muss zunächst das Verzeichnis **static** im Python-Entwicklungspfad geleert werden. Daraufhin wird im Pfad der Webapp mit **grunt build** der Build gestartet, welcher die Webapp wiederum in das **static** Verzeichnis baut. Daraufhin kann das aktualisierte Webinterface vom Server abgerufen werden.

Die Webapp enthält mehrere Services. Der **DataService** ist verantwortlich für die Kommunikation mit der REST-Schnittstelle des Servers. Dafür werden für die benötigten Endpunkte Methoden zur Verfügung gestellt. Dort auftretende Fehler werden durch den **ErrorHandler** behandelt, welcher Fehler in einem Fehlerdialog darstellt. Zusätzlich steht ein **WebsocketService** zur Verfügung, welcher für die Websocket-Kommunikation mit dem Server verantwortlich ist. Dieser bietet für die vom Server unterstützten Events entsprechende Methoden. Sobald Events empfangen werden, werden diese vom **WebsocketService** in die App gebroadcasted und an entsprechender Stelle in den Controllern behandelt.

Zusätzlich wurden mehrere Controller umgesetzt. Der **DashboardCtrl** ist für das Dashboard verantwortlich und lauscht auf den Broadcast des **WebsocketService**s, um die Liste der aktiven Nutzer aktuell zu halten. Bei der Initialisierung wird zudem ein **GetActiveUsersEvent** an den Server geschickt, damit nicht erst auf eine Änderung gewartet werden muss, um die aktiven Benutzer anzeigen zu können. Der **UsersCtrl** ist verantwortlich für die Ansicht zur Benutzerverwaltung. Er kommuniziert mit Hilfe des **DataServices** mit dem Webserver und empfängt, updated und löscht mit diesem System-User. Ein weiterer Controller ist der **LatencyCtrl**, dieser ist verantwortlich für die Testseite, auf der ein Latenz- und ein Last-Test durchgeführt werden können. Dieser kommuniziert mit dem **WebsocketService** um die entsprechenden Befehle an den Server zu übermitteln. Zusätzlich existieren noch ein **CreateCtrl** und ein **UpdateCtrl**, welche für das Anlegen bzw. Aktualisieren eines Users verantwortlich sind. Hierfür nutzen sie den **DataService**. Der **ErrorCtrl** dient zur Darstellung eines Fehlers.


### Peripheriesteuerung

#### SoundController

#### DMXController