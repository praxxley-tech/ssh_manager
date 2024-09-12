![Code Coverage](https://img.shields.io/badge/coverage-passed-brightgreen)  <!-- Badge für Code Coverage -->

# SSH-Verbindungsskript

## Überblick

Dieses Python-Skript liest eine CSV-Datei mit Hostinformationen, erlaubt dem Benutzer, einen Host aus einer Liste auszuwählen, und stellt dann eine SSH-Verbindung zu dem ausgewählten Host her. Das Skript startet den SSH-Agenten, ermöglicht die Auswahl eines privaten SSH-Schlüssels und führt den SSH-Befehl aus.

## Voraussetzungen

1. **Python**: Python muss auf deinem System installiert sein. Stelle sicher, dass du Python 3.x installiert hast.

2. **PowerShell**: Das Skript wird in PowerShell ausgeführt.

3. **SSH-Agent**: Du benötigst den SSH-Agenten, der auf deinem System konfiguriert sein muss. Für Windows kann dies durch ein Batch-Skript wie `start-ssh-agent.cmd` erfolgen.

4. **Python-Pakete**:
   - `prettytable`: Wird benötigt, um die Tabelle anzuzeigen. Installiere es mit `pip install prettytable`.

## Vorbereitungen

1. **Installiere Python und benötigte Pakete**:

   ```sh
   pip install prettytable

## CSV-Datei muss wie folgt aussehen:
hostname1,username1,description1
hostname2,username2,description2
