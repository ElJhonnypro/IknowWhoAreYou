# Importar módulos necesarios
import os
import sys
import subprocess
import time
import re
from colorama import Fore, init, Style

# Limpiar la pantalla en varias plataformas
os.system('clear')

# Verificar si el script se está ejecutando como root
try:
    result = subprocess.run(['whoami'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    username = result.stdout.strip() if result.stdout else ''
except subprocess.CalledProcessError:
    print(f'{Fore.RED}Error al ejecutar el comando whoami')
    sys.exit(1)

if username != 'root':
    print(f'{Fore.RED}ERROR: ¡Este script debe ejecutarse como root!')
    sys.exit(1)

# Definir una clase para las opciones del menú
class Option:
    def __init__(self, numberoption, helptext):
        self.number = numberoption
        self.help = helptext
    
    def its_selected(self, question):
        return question == self.number

# Crear instancias de la clase Option
option1 = Option(1, 'Modo normal: ver IP, sistema operativo, versión de Windows, etc.')

# Inicializar colorama para la salida coloreada
init(autoreset=True)

# Función para verificar si un puerto está abierto en una dirección IP dada
def check_port(port: str, ip_address: str):
    try:
        subprocess.run(['nc', '-zvw', '2', ip_address, port], text=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f'{Fore.GREEN}Puerto {port} abierto en {ip_address}.')
        return True
    except subprocess.CalledProcessError as e:
        if 'Connection timed out' in e.stderr or 'Connection refused' in e.stderr:
            print(f'{Fore.RED}{Style.BRIGHT}Puerto {port} no abierto en {ip_address}.')
            print(f'{Fore.RESET}')
            return False

def check_system(ttl: int, ip_address: str):
    print(f'{Fore.RED}TTL: {Fore.BLUE} {ttl}{Fore.RESET}')
    command_crack = subprocess.run(['crackmapexec','smb', ip_address], text=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
    print(command_crack)
    if command_crack:
        version_name = re.search(r'Windows\s+(\S+)', command_crack)
        if version_name:
            print(f'{Fore.GREEN}Versión de smb (Windows): {version_name.group(0)}')
        else:
            print(f'{Fore.RED}No se pudo determinar la versión de smb (Windows)')
    else:
        print(f'{Fore.RED}La IP {ip_address} no tiene smb :(')

# Función para manejar el menú para la opción 1
def option1_menu():
    puertos_encontrados = []  # Lista para almacenar puertos encontrados
    os.system('clear')
    print(f'{Fore.BLUE}Modo normal activado...')
    
    while True:
        ip_address = input(f'{Fore.RED}{Style.BRIGHT}MODO NORMAL: Ingrese la IP de destino>{Fore.YELLOW} ')
        if ip_address:
            break
        else:
            print('Error: Por favor, ingrese una dirección IP válida.')

    try:
        ttl_output = int(subprocess.run(['ping', '-c', '1', ip_address], text=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=True).stdout.split('ttl=')[1].split()[0])
        check_system(ttl_output, ip_address)
    except subprocess.CalledProcessError as e:
        print('La página web o dispositivo no existe o hay un error al ejecutarlo')
        sys.exit(1)

    # Verificar si los puertos comunes (80, 443) están abiertos y agregarlos a la lista
    if check_port('80', ip_address):
        print(f'{Fore.YELLOW}Ingrese al servidor HTTP en: http://{ip_address}/')
        puertos_encontrados.append(80)

    if check_port('443', ip_address):
        print(f'{Fore.YELLOW}Ingrese al servidor HTTPS en: https://{ip_address}/')
        puertos_encontrados.append(443)

    print('Detectando puertos...')
    
    while True:
        try:
            rango_puertos = int(input('Rango de puertos> '))
            break
        except ValueError:
            print('Error: Por favor, ingrese un número entero válido.')

    # Iterar a través del rango de puertos, verificando y agregando puertos abiertos a la lista
    for i in range(rango_puertos + 1):
        # No verificar los puertos 80 o 443
        if i == 80 or i == 443:
            check_port(str(i), ip_address)
        else:
            if check_port(str(i), ip_address):
                puertos_encontrados.append(i)
                print(f'{Fore.BLUE}¡Puerto encontrado!')

    # Imprimir los puertos encontrados
    for puerto in puertos_encontrados:
        print(f'Puerto encontrado: {puerto}')

# Función para inicializar el menú principal
def init_menu():
    print(
        f"""
        {Fore.RED}{Style.BRIGHT}========================== ¡Hola! Bienvenido a IkWhoAreYou =======================

        {Fore.BLUE}[1]:{Fore.YELLOW} Modo normal (ver IP, Linux/Mac o Windows, versión de Windows, etc)

        {Fore.RED}
        ================================================================================
        """
    )

    while True:
        try:
            # Conseguimos la opción elegida
            opcion = int(input(f'{Fore.BLUE}Seleccione una opción:>{Fore.YELLOW} '))
            if option1.its_selected(opcion):
                option1_menu()
            else:
                print('Error: Por favor, ingrese una opción válida.')
        except ValueError:
            print('Error: Por favor, ingrese un número entero válido.')
        except KeyboardInterrupt:
            print(f'{Fore.YELLOW}Adiós. Gracias por usar esta herramienta.')
            os.system('clear')
            sys.exit(0)

# Ejecución principal: inicializar el menú principal y manejar interrupciones de teclado
if __name__ == '__main__':
    init_menu()
