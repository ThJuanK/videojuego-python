import pygame
from random import randint
import math
from pygame import mixer


# inicializa pygame
pygame.init()

fondo = pygame.image.load("media/Fondo.jpg")

# crea la pantalla con la resolución definida en una tupla.
pantalla = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Invasión espacial")

icono = pygame.image.load("media/ovni-volando.png")

pygame.display.set_icon(icono)

# Agregar musica
'''mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)'''

# Jugador
img_jugador = pygame.image.load("media/nave-espacial.png")
jugador_x = 384
jugador_y = 568
jugador_x_cambioder = 0
jugador_x_cambioizq = 0
jugador_y_cambio = 0


def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# Enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 7


for x in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("media/monstruo.png"))
    enemigo_x.append(randint(0, 736))
    enemigo_y.append(randint(50, 200))
    enemigo_x_cambio.append(0.1)
    enemigo_y_cambio.append(100)

def enemigo(x, y, i):
    pantalla.blit(img_enemigo[i], (x, y))


# Balas
img_bala = pygame.image.load("media/bola-de-fuego.png")
bala_x = 0
bala_y = 568
bala_x_cambio = 0
bala_y_cambio = 0.4
visibilidad_bala = False

def disparar_bala(x, y):
    global visibilidad_bala
    visibilidad_bala = True
    pantalla.blit(img_bala, (x + 9, y + 16))


def detectar_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1, 2)+math.pow(y_2 - y_1, 2))
    if distancia < 15:
        return True
    else:
        return False


# Puntaje
puntaje = 0
fuente = pygame.font.Font('media/28 Days Later.ttf', 26)
texto_x = 10
texto_y = 10

def mostrar_puntaje(x,y):
    texto = fuente.render(f"Puntos {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# GAME OVER
fuentemuerte = pygame.font.Font('media/28 Days Later.ttf', 62)

def texto_final():
    text = fuentemuerte.render(f"FIN DEL JUEGO", True, (255, 255, 255))
    pantalla.blit(text, (210, 260))


se_ejecuta = True
while se_ejecuta:
    # Cambiando la imagen de fondo
    pantalla.blit(fondo, (0, 0))  # se puede usar un valor en una tupla o en formato RGB con .fill(

    # Iteración de los eventos
    for evento in pygame.event.get():  # Pygame.event.get: Función que obtiene el evento actual.
        if evento.type == pygame.QUIT:  # pygame.QUIT: evento del botón de cerrar,
            se_ejecuta = False

        # evento teclas presionadas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:
                jugador_x_cambioizq = 0.15

            if evento.key == pygame.K_d:
                jugador_x_cambioder = 0.15

            if evento.key == pygame.K_SPACE:
                sonido_disparo = mixer.Sound("media/disparo.mp3")

                if not visibilidad_bala:
                    sonido_disparo.play()
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)


        # evento teclas soltadas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_a:
                jugador_x_cambioizq = 0

            if evento.key == pygame.K_d:
                jugador_x_cambioder = 0

    # reaparicion del personaje
    if jugador_x >= pantalla.get_width() + 1:
        jugador_x = -32
    if jugador_x < -32:
        jugador_x = pantalla.get_width()

    # Mantener al enemigo dentro de los bordes y manejar el acercamiento al personaje principal
    for i in range(cantidad_enemigos):
        if enemigo_x[i] <= 0:
            enemigo_x_cambio[i] = 0.1
            enemigo_y[i] += enemigo_y_cambio[i]

        if enemigo_x[i] >= (pantalla.get_width() - 24):
            enemigo_x_cambio[i] = -0.1
            enemigo_y[i] += enemigo_y_cambio[i]

        if enemigo_y[i] >= (pantalla.get_height() - 32):
            for j in range(cantidad_enemigos):
                enemigo_y[j] = pantalla.get_height() - 100
            texto_final()
            break

        # colisión
        colision = detectar_colision(enemigo_x[i], enemigo_y[i], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound("media/Golpe.mp3")
            sonido_colision.play()
            bala_y = 568
            visibilidad_bala = False
            puntaje += 1
            enemigo_x[i] = randint(0, 736)
            enemigo_y[i] = randint(50, 200)


    # movimiento de la bala
    if bala_y <= -32:
        visibilidad_bala = False
        bala_y = pantalla.get_height() - 32

    if visibilidad_bala:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    # Cambios con respecto al movimiento y su debida funcion
    jugador_x += jugador_x_cambioder
    jugador_x -= jugador_x_cambioizq

    for i in range(cantidad_enemigos):
        enemigo_x[i] += enemigo_x_cambio[i]
        enemigo(enemigo_x[i], enemigo_y[i], i)

    jugador(jugador_x, jugador_y)
    mostrar_puntaje(texto_x, texto_y)

    # función para actualizar la pantalla.
    pygame.display.update()
