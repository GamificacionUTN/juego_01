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
import serial.tools.list_ports
import random
import os
from subrutinas import print_at, marco, mapa as cargar_mapa, valida, enviarArduino
import time


# Retrieves the gamer name
gamer = input("Digite el nombre del jugador: ")


# Execute an external instruction from operative system to clean screen,
# cls is a Windows instruction, if you work on Linux you must use
# instruction clear
os.system("cls" if os.name == "nt" else "clear")


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
mapa = cargar_mapa()


def colocar_monedas_aleatorias(cantidad=6):
    alcanzables = set()
    por_visitar = [(maty, matx)]

    while por_visitar:
        fila, columna = por_visitar.pop()
        if (fila, columna) in alcanzables:
            continue
        if fila < 0 or fila >= len(mapa):
            continue
        if columna < 0 or columna >= len(mapa[fila]):
            continue
        if mapa[fila][columna] not in (' ', '*'):
            continue

        alcanzables.add((fila, columna))

        por_visitar.extend([
            (fila - 1, columna),
            (fila + 1, columna),
            (fila, columna - 1),
            (fila, columna + 1),
        ])

    posiciones_premio = [
        posicion for posicion in alcanzables
        if mapa[posicion[0]][posicion[1]] == ' '
        and posicion != (maty, matx)
    ]

    random.shuffle(posiciones_premio)
    for fila, columna in posiciones_premio[:cantidad]:
        mapa[fila][columna] = '$'


matx = 0
maty = 1
colocar_monedas_aleatorias()


# Print the game map
print(Fore.GREEN)
posx = 2
posy = 6
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

# Search for an Arduino UNO serial port
PORT_SERIAL = None
for puerto in serial.tools.list_ports.comports():
    descripcion = (puerto.description or '').lower()
    hardware = (puerto.hwid or '').lower()
    if 'arduino' in descripcion or '2341:' in hardware or '1a86:' in hardware:
        PORT_SERIAL = puerto.device
        break

if PORT_SERIAL is None:
    PORT_SERIAL = 'COM3'

try:
    a1r3 = serial.Serial(PORT_SERIAL, 9600, timeout=0.1)
    time.sleep(2)
    print_at(20, 2, 'Arduino conectado en ' + PORT_SERIAL)
    enviarArduino('O', a1r3)
    time.sleep(2)
except serial.SerialException as error:
    a1r3 = None
    print_at(20, 2, 'Arduino no disponible en ' + PORT_SERIAL + ': ' + str(error))


vidas = 3
choquesPared = 0
paredUltima = None
puntos = 0
oro = 0
posicionInicialX = 0
posicionInicialY = 1
ultimoMovimiento = 0
RETRASO_MOVIMIENTO = 0.18


def limpiar_buffer_serial():
    if a1r3 is not None and a1r3.is_open:
        try:
            a1r3.reset_input_buffer()
        except serial.SerialException:
            return


def actualizar_hud(mensaje=''):
    corazones = '♥' * vidas + '♡' * (3 - vidas)
    linea_stats = (
        f"JUGADOR: {gamer}  |  VIDAS: {corazones}  |  ORO: {oro}  |  "
        f"PUNTOS: {puntos}  |  POSICION: (Fila {maty + 1}, Col {matx + 1})"
    )
    # .ljust(75) borra residuos de textos anteriores más largos
    print_at(18, 2, linea_stats.ljust(76))
    print_at(19, 2, ('MENSAJE: ' + mensaje).ljust(76))
    print_at(20, 2, 'CONTROL: utiliza el joystick para moverte'.ljust(76))



def reiniciar_posicion():
    global matx, maty, posx, posy
    print_at(posy, posx, ' ')
    matx = posicionInicialX
    maty = posicionInicialY
    posx = matx + 2
    posy = maty + 6
    print_at(posy, posx, avatar)


def choque_pared(direccion):
    global vidas, choquesPared, paredUltima
    choqueActual = (matx, maty, direccion)

    if choqueActual != paredUltima:
        choquesPared = 1
        paredUltima = choqueActual
    else:
        choquesPared += 1

    if choquesPared == 1:
        enviarArduino('R', a1r3)
        actualizar_hud('¡Atencion! No puedes atravesar la pared.')
        return

    enviarArduino('R', a1r3)
    vidas -= 1
    choquesPared = 0
    paredUltima = None

    if vidas <= 0:
        vidas = 0
        actualizar_hud('¡Sin vidas! El juego ha terminado.')
        enviarArduino('L', a1r3)
        time.sleep(2.5)
        limpiar_buffer_serial()
        enviarArduino('O', a1r3)
        return False

    reiniciar_posicion()
    choquesPared = 0
    paredUltima = None
    actualizar_hud('¡Choque grave! Perdiste una vida y vuelves al inicio.')
    return True


def intentar_movimiento(dx, dy, direccion):
    global matx, maty, posx, posy, choquesPared, paredUltima

    if valida(mapa, matx + dx, maty + dy):
        print_at(posy, posx, ' ')
        matx += dx
        maty += dy
        posx = matx + 2
        posy = maty + 6
        print_at(posy, posx, avatar)
        choquesPared = 0
        paredUltima = None
        return True

    resultado = choque_pared(direccion)
    return resultado if resultado is False else None


def celebrar_victoria():
    enviarArduino('V', a1r3)
    time.sleep(4)
    limpiar_buffer_serial()
    enviarArduino('O', a1r3)


actualizar_hud('Explora la mazmorra.')
try:
    while True:
        time.sleep(0.02)

        xVal = 512
        yVal = 512
        if a1r3 is not None:
            try:
                while a1r3.in_waiting > 0:
                    linea = a1r3.readline().decode('ascii', errors='ignore').strip()
                    partes = linea.split(';')
                    if len(partes) == 2:
                        try:
                            xVal = int(partes[0].strip())
                            yVal = int(partes[1].strip())
                        except ValueError:
                            continue
            except serial.SerialException as error:
                print_at(20, 2, ('Error de lectura: ' + str(error)).ljust(76))

        ahora = time.monotonic()
        movimientoRealizado = False

        if ahora - ultimoMovimiento >= RETRASO_MOVIMIENTO:
            direccion = None
            dx = dy = 0

            if yVal < 150:
                direccion = 'derecha'
                dx = 1
            elif yVal > 850:
                direccion = 'izquierda'
                dx = -1
            elif xVal < 150:
                direccion = 'arriba'
                dy = -1
            elif xVal > 850:
                direccion = 'abajo'
                dy = 1

            if direccion is not None:
                resultadoMovimiento = intentar_movimiento(dx, dy, direccion)
                if resultadoMovimiento is False:
                    break
                movimientoRealizado = resultadoMovimiento is True
                ultimoMovimiento = ahora

        if movimientoRealizado:
            simbolo = mapa[maty][matx]
            evento_mensaje = 'Explora la mazmorra.'

            if simbolo == '$':
                mapa[maty][matx] = ' '
                print_at(posy, posx, avatar)
                oro += 1
                puntos += 25
                enviarArduino('G', a1r3)
                evento_mensaje = '¡Encontraste una moneda!'
            elif simbolo == 'K':
                mapa[maty][matx] = ' '
                print_at(posy, posx, avatar)
                puntos += 50
                enviarArduino('Y', a1r3)
                evento_mensaje = '¡Encontraste una llave!'
            elif simbolo == '^':
                enviarArduino('R', a1r3)
                evento_mensaje = '¡Cuidado! Hay una trampa.'
            elif simbolo == '*':
                puntos += 100
                actualizar_hud('¡Has encontrado la salida!')
                celebrar_victoria()
                break

            actualizar_hud(evento_mensaje)
except KeyboardInterrupt:
    print_at(18, 2, 'Juego terminado.')
finally:
    if a1r3 is not None and a1r3.is_open:
        enviarArduino('O', a1r3)
        a1r3.close()
