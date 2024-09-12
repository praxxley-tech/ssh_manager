import subprocess
import os
import csv
from prettytable import PrettyTable

def get_user_input(prompt):
    return input(prompt)

def start_ssh_agent():
    try:
        subprocess.run('start-ssh-agent.cmd', shell=True, check=True)
        print("SSH-Agent erfolgreich gestartet.")
    except subprocess.CalledProcessError:
        print("Fehler beim Starten des SSH-Agents.")
        return False
    return True

def add_ssh_key():
    ssh_dir = os.path.expanduser("~/.ssh")

    ssh_keys = [f for f in os.listdir(ssh_dir) if f.endswith('.pub') == False]

    if not ssh_keys:
        print("Es wurden keine SSH-Schlüssel gefunden.")
        return None

    print("Verfügbare SSH-Schlüssel:")
    for i, key in enumerate(ssh_keys, start=1):
        print(f"{i}: {key}")

    while True:
        try:
            selection = int(get_user_input("Wähle den Index eines SSH-Schlüssels: "))
            if 1 <= selection <= len(ssh_keys):
                selected_key = ssh_keys[selection - 1]
                key_path = os.path.join(ssh_dir, selected_key)
                break
            else:
                print("Ungültige Auswahl. Bitte versuche es erneut.")
        except ValueError:
            print("Bitte gib eine gültige Zahl ein.")

    try:
        subprocess.run(f'ssh-add {key_path}', shell=True, check=True)
        print(f"SSH-Schlüssel {selected_key} erfolgreich hinzugefügt.")
    except subprocess.CalledProcessError:
        print(f"Fehler beim Hinzufügen des SSH-Schlüssels {selected_key}.")
        return None

    return selected_key

def main_script():
    x = PrettyTable()
    x.field_names = ["Index", "Hostname", "Username", "Description"]

    hosts = []
    with open('hosts.csv') as f:
        reader = csv.reader(f)
        for index, row in enumerate(reader, start=1):
            if len(row) == 3: 
                x.add_row([index] + row)
                hosts.append(row) 
            else:
                print(f"Warnung: Zeile {index} hat nicht genau 3 Spalten und wird ignoriert.")
    print(x)

    while True:
        try:
            selection = int(get_user_input("Wähle den Index eines Hosts: "))
            if 1 <= selection <= len(hosts):
                selected_host = hosts[selection - 1]  
                hostname = selected_host[0]  
                username = selected_host[1] 
                description = selected_host[2] 
                
                if hostname and username:
                    print(f"Ausgewählter Hostname: {hostname}, Username: {username}")
                    break
                else:
                    print(f"Fehler: Hostname oder Username in Zeile {selection} ist leer.")
            else:
                print("Ungültige Auswahl. Bitte versuche es erneut.")
        except ValueError:
            print("Bitte gib eine gültige Zahl ein.")

    if start_ssh_agent():
        ssh_key = add_ssh_key()
        if ssh_key:
            command = f'ssh {username}@{hostname}'

            print(f"Auszuführender Befehl: {command}")

            try:
                subprocess.run(command, shell=True)
            except Exception as e:
                print(f"Fehler bei der Ausführung des Befehls: {e}")

if __name__ == '__main__':
    main_script()