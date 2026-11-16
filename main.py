"""================================================================================================
Institute...: Universidad Técnica Nacional
Campus......: Pacífico
Career......: Tecnologías de Información
Period......: 3-2026
Document....: main.py
Goals.......: Play the dungeon game.
Professor...: Jorge Ruiz (york)
Student.....:
================================================================================================"""
from colorama import init, Fore, Back
import serial
import subprocess
from subrutinas import print_at, marco, mapa, valida
import time


# Retrieves the gamer name
gamer = input("Digite el nombre del jugador: ")


# Execute an external instruction from operative system to clean screen,
# cls is a Windows instruction, if you work on Linux you must use
# instruction clear
subprocess.call("cls", shell=True)


# initialize color management
init()


# Call the marco function to draw Game title
print(Fore.LIGHTBLUE_EX)
marco(1, 1, 80, 4)


# Print text, using the position on screen  function
print_at(2, 27, Fore.YELLOW + 'MAZMORRA PERDIDA DE LA UTN')
print_at(3, 31, Fore.YELLOW + 'Sede del Pacífico')
print(Back.BLACK)


# Call the marco function to draw main frame
print(Fore.LIGHTBLUE_EX)
marco(1, 5, 80, 17)


# Retrieves the game map
mapa = mapa()


# Print the game map
posx = 2
posy = 6
print(Fore.GREEN)
for fila in mapa:
    for valor in fila:
        print_at(posy, posx, valor)
        posx += 1
    posy += 1
    posx = 2

# Print avatar @
posx = 2
posy = 7
avatar = '@'
print(Fore.WHITE)
print_at(posy, posx, avatar)

print_at(18, 2, '')

# Read the serial port from Arduino UNO
a1r3 = serial.Serial('COM5', 9600)


matx = 0
maty = 1
while True:
    time.sleep(1/100)
    dato = a1r3.readline().decode('utf-8').rstrip()
    print_at(20,2,dato)
    try:
        dato2 = a1r3.readline().decode('utf-8').rstrip()
        xVal = dato.split(';')[0]
        yVal = dato.split(';')[1]
    except:
        xVal = '504'
        yVal = '497'
    if yVal == '0':
        if valida(mapa, matx + 1, maty):
            print_at(posy, posx, ' ')
            posx += 1
            matx += 1
            print_at(posy, posx, avatar)
    elif yVal == '1023':
        if valida(mapa, matx - 1, maty):
            print_at(posy, posx, ' ')
            posx -= 1
            matx -= 1
            print_at(posy, posx, avatar)
    if xVal == '0':
        if valida(mapa, matx, maty - 1):
            print_at(posy, posx, ' ')
            posy -= 1
            maty -= 1
            print_at(posy, posx, avatar)
    elif xVal == '1023':
        if valida(mapa, matx, maty + 1):
            print_at(posy, posx, ' ')
            posy += 1
            maty += 1
            print_at(posy, posx, avatar)
