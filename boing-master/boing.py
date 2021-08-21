import pgzero, pgzrun, pygame
import math, sys, random
import print as print
from enum import Enum

# Verifique el número de versión de Python. sys.version_info da
# la versión como una tupla, p. ej. if (3,7,2, 'final', 0) para la versión 3.7.2.

# A diferencia de muchos lenguajes, Python puede comparar dos tuplas
# de la misma manera que puede comparar números.
from pgzero.actor import Actor

if sys.version_info < (1, 5):
    print("Este juego requiere al menos la versión 3.5 de Python. Descárguelo de www.python.org")
    sys.exit()

# Verifique la versión de Pygame Zero.
# Esto es un poco más complicado porque Pygame Zero
# solo nos permite obtener su número
# de versión como una cadena.
# Entonces tenemos que dividir la cadena en una lista,
# usando '.' como el personaje en el que se dividirá.
# Convertimos cada elemento del número de versión
# en un entero, pero solo si la cadena contiene números y nada más,
# porque es posible para un componente de la versión
# para contener letras y números (por ejemplo, '2.0.dev0')
# Estamos usando una función de Python
# llamada comprensión de listas;
# esto se explica en el capítulo Bubble Bobble / Cavern.

pgzero_version = [int(s) if s.isnumeric() else s for s in pgzero.__version__.split('.')]
if pgzero_version < [1, 2]:
    print("Este juego requiere al menos la versión 1.2 de Pygame Zero "
          "Tiene la versión {0}. Actualice con el comando"
          "'pip3 install --upgrade pgzero'"
          .format(pgzero.__version__))
    sys.exit()

# Set up constants
WIDTH = 800
HEIGHT = 480
TITLE = "Boing!"

HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

ANCHO_BATE = 18
ALTO_BATE = 128
MITAD_ALTO_BATE = ALTO_BATE // 2
ANCHO_BOLA = 48
DIST_BATE_FONDO = 40
POS_X_REBOTE = ((WIDTH - ANCHO_BATE - ANCHO_BOLA) // 2) - DIST_BATE_FONDO
MAX_DIF_X_AL_CENTRO = 220

PLAYER_SPEED = 10
MAX_AI_SPEED = 4


def normalised(x, y):
    # Devuelve un vector unitario
    # Obtener la longitud del vector (x, y) - math.hypot usa el teorema de Pitágoras
    # para obtener la longitud de la hipotenusa
    # de triángulo rectángulo con lados de longitud xey
    # todo note on safety
    length = math.hypot(x, y)
    return (x / length, y / length)


def sign(x):
    # Devuelve -1 o 1 dependiendo cuando el número es positivo o negativo
    return -1 if x < 0 else 1


class Impact(Actor):
    # Clase para una animación que se muestra brevemente
    # cada vez que la pelota rebota
    def __init__(self, pos):
        super().__init__("blank", pos)
        self.time = 0

    def update(self):
        # Hay 5 sprites de impacto numerados del 0 al 4.
        # Actualizamos a un nuevo sprite cada 2 fotogramas.
        self.image = "impact" + str(self.time // 2)

        # La clase Game mantiene una lista de instancias de Impact.
        # En Game.update, si el temporizador de un objeto
        # ha ido más allá de 10, el objeto se elimina de la lista.
        self.time += 1


class Ball(Actor):
    def __init__(self, dx):
        super().__init__("ball", (0, 0))

        self.x, self.y = HALF_WIDTH, HALF_HEIGHT

        # dx y dy juntos describen la dirección en la que se mueve la pelota.
        # Por ejemplo, si dx y dy son 1 y 0, la pelota se mueve hacia la derecha,
        # sin movimiento hacia arriba o hacia abajo.
        # Si ambos valores son negativos,la bola se mueve hacia la izquierda y hacia arriba,
        # con el ángulo dependiendo de los valores relativos de las dos variables.
        # Si estas familiarizado con los vectores, dx y dy representan un vector unitario.
        # Si no está familiarizado con los vectores, consulte la explicación en el libro.
        self.dx, self.dy = dx, 0

        self.speed = 5

    def update(self):
        # En cada cuadro, movemos la pelota en una serie de pequeños pasos;
        # el número de pasos se basa en su atributo de velocidad.
        for i in range(self.speed):
            # Guarda la posicion x previa
            original_x = self.x

            # Mueve la pelota en base a dx y dy
            self.x += self.dx
            self.y += self.dy

            # Verifique si la pelota necesita rebotar en un bate

            # Para determinar si la pelota puede chocar con un bate,
            # primero medimos la distancia horizontal desde la bola
            # al centro de la pantalla y verifique si su borde
            # ha ido más allá del borde del bate.
            # El centro de cada bate está a 40 píxeles del borde de la pantalla,
            # o para decirlo de otra manera, 360 píxeles desde el centro de la pantalla.
            # El bate tiene 18 píxeles de ancho y la bola tiene 14 píxeles de ancho.
            # Dado que estos los sprites están anclados desde sus centros, al determinar
            # si se superponen o se tocan, debemos mirar sus medias anchuras: 9 y 7.
            # Por lo tanto, si el centro de la bola está a 344 píxeles del centro de la
            # pantalla, puede rebotar en un bate (asumiendo que el bate está
            # en la posición correcta en el eje Y - marcado Poco después).
            # También comprobamos la posición X anterior
            # para asegurarnos de que este es el primer fotograma
            # en el que la pelota cruzó el umbral.

            if abs(self.x - HALF_WIDTH) >= POS_X_REBOTE and abs(original_x - HALF_WIDTH) < POS_X_REBOTE:

                # Ahora que sabemos que el borde de la pelota ha cruzado el umbral en el eje x,
                # debemos verificar si el bate en el lado relevante de la arena
                # está en una posición adecuada en el eje 'y' para la bola choca con el.

                if self.x < HALF_WIDTH:  # Si la pelota esta en el lado izdo.
                    new_dir_x = 1        # toma direccion positiva en x
                    bat = game.bats[0]   # ??
                else:                    # Si la pelota esta en el lado dcho.
                    new_dir_x = -1       # toma direccion negativa en x
                    bat = game.bats[1]   # ??

                difference_y = self.y - bat.y   # Obtiene la diferencia etre la 'Y' de la bola
                                                # y la 'Y' del bate

                if difference_y > - MITAD_ALTO_BATE  and difference_y < MITAD_ALTO_BATE:
                    # La bola ha chocado con el bate - calcular el nuevo vector de dirección

                    # Para comprender las matemáticas que se utilizan a continuación,
                    # primero debemos considerar qué sucedería con este tipo de
                    # colisión en el mundo real. La pelota rebota en una superficie
                    # perfectamente vertical. Esto lo convierte en un cálculo bastante simple.
                    # Tomemos una bola que viaja a 1 metro por segundo hacia la derecha,
                    # y 2 metros por segundo hacia abajo. Imagina que esto está sucediendo
                    # en el espacio, por lo que la gravedad no es un factor.
                    # Después de que la pelota golpee el bate, todavía se moverá a 2 m / s
                    # hacia abajo, pero ahora estara moviéndose 1 m / s hacia la izquierda
                    # en lugar de hacia la derecha. Entonces su velocidad en el eje y no ha
                    # cambiado, pero su dirección en el eje x se ha invertido.
                    # Esto es extremadamente fácil de codificar: "self.dx = -self.dx".
                    # Sin embargo, los juegos no tienen que reflejar perfectamente la realidad.
                    # En Pong, golpear la pelota con la parte superior o inferior del bate
                    # la haría rebotar en diagonalhacia arriba o hacia abajo respectivamente.
                    # Esto le da al jugador un grado de control sobre el lugar donde la va pelota
                    # Para hacer un juego más interesante, queremos usar la física realista
                    # como punto de partida, pero combine con esto la capacidad de influir en
                    # la dirección de la pelota. Cuando la pelota golpea el bate,
                    # vamos a desviar la pelota ligeramente hacia arriba o hacia abajo
                    # dependiendo de dónde golpeó el bate.
                    # Esto le da al jugador un poco de control sobre dónde va la pelota.

                    # Rebota en sentido contrario en el eje X
                    self.dx = -self.dx

                    # Desvía ligeramente hacia arriba o hacia abajo dependiendo
                    # de dónde golpeó la bola con el bate
                    self.dy += difference_y / ALTO_BATE

                    # Limita el componente Y del vector para que no entremos en una situación
                    # en la que la pelota esté rebotando sube y baja demasiado rápido
                    self.dy = min(max(self.dy, -1), 1)

                    # Asegúrese de que nuestro vector de dirección sea un vector unitario,
                    # es decir, que represente una distancia del equivalente de
                    # 1 píxel independientemente de su ángulo
                    self.dx, self.dy = normalised(self.dx, self.dy)

                    # Crea un efecto de impacto
                    #game.impacts.append(Impact((self.x - new_dir_x * 10, self.y)))
                    game.impacts.append(Impact(self.pos))
                    # Aumenta la velocidad con cada impacto
                    self.speed += 1

                    # Agrega un desplazamiento a la posición Y objetivo del jugador AI,
                    # por lo que no apuntara a golpear la pelota exactamente
                    # en el centro del bate
                    game.ai_offset = random.randint(-10, 10)

                    # Bate brilla durante 10 cuadros
                    bat.timer = 15

                    # Reproduce sonidos de golpe, con efectos de sonido más intensos a medida
                    # que la pelota se vuelve más rápida.
                    game.play_sound("hit", 5)  # play every time in addition to:
                    if self.speed <= 10:
                        game.play_sound("hit_slow", 1)
                    elif self.speed <= 12:
                        game.play_sound("hit_medium", 1)
                    elif self.speed <= 16:
                        game.play_sound("hit_fast", 1)
                    else:
                        game.play_sound("hit_veryfast", 1)

            # La parte superior e inferior de la arena están a 220 píxeles del centro
            if abs(self.y - HALF_HEIGHT) > MAX_DIF_X_AL_CENTRO:
                # Invierta la dirección vertical y aplique un nuevo dy ay para que la bola
                # ya no se superponga con el borde de la arena
                self.dy = -self.dy
                self.y += self.dy

                # Crea un efecto de impacto
                game.impacts.append(Impact(self.pos))

                # Efecto de sonido
                game.play_sound("bounce", 5)
                game.play_sound("bounce_synth", 1)

    def out(self):
        # ¿La bola se ha salido del borde izquierdo o derecho de la pantalla?
        return self.x < 0 or self.x > WIDTH


class Bat(Actor):
    def __init__(self, player, move_func=None):
        x = 40 if player == 0 else 760
        y = HALF_HEIGHT
        super().__init__("blank", (x, y))

        self.player = player
        self.score = 0

        # move_func es una función que puede o no haber sido pasada por el codigo
        # que creó este objeto. Si este bate está destinado a ser controlado por el jugador,
        # move_func será una función que, cuando se llama, devuelve un número que indica
        # la dirección y velocidad en la que debe moverse el bate, según las teclas
        # que el jugador está presionando actualmente.
        # Si move_func es None, indica que este bate debería ser controlado por el método AI.
        if move_func != None:
            self.move_func = move_func
        else:
            self.move_func = self.ai

        # Cada bate tiene un temporizador que comienza en cero y cuenta hacia atrás
        # de uno en uno en cada cuadro. Cuando un jugador concede un punto,
        # su temporizador está configurado en 20, lo que hace que el bate
        # muestre un cuadro de animación diferente. También se utiliza para
        # decidir cuándo crear una nueva bola en el centro de la pantalla;
        # consulte los comentarios en Game.update para obtener más información al respecto.
        # Finalmente, se usa en Game.draw para determinar cuándo mostrar un efecto visual
        # en la parte superior del fondo
        self.timer = 0

    def update(self):
        self.timer -= 1

        # Nuestra función de movimiento nos dice cuánto movernos en el eje Y
        y_movement = self.move_func()

        # Aplique y_movement en la posición y, asegurándose de que el bate
        # no atraviese las paredes laterales
        self.y = min(400, max(80, self.y + y_movement))

        # Elige el objeto apropiado. Hay 3 sprites por jugador,
        # p. Ej. bat00 es el jugador zurdo sprite de bate estándar,
        # bat01 es el sprite que se usa cuando la pelota acaba de rebotar en el bate,
        # y bat02 es el objeto que se usa cuando el bate acaba de fallar la pelota
        # y la pelota se sale de los límites.
        # bat10, 11 y 12 son los equivalentes para el jugador derecho
        frame = 0
        if self.timer > 0:
            if game.ball.out():
                frame = 2
            else:
                frame = 1

        self.image = "bat" + str(self.player) + str(frame)

    def ai(self):
        # Returns a number indicating how the computer player will move - e.g. 4 means it will move 4 pixels down
        # the screen.

        # To decide where we want to go, we first check to see how far we are from the ball.
        x_distance = abs(game.ball.x - self.x)

        # If the ball is far away, we move towards the centre of the screen (HALF_HEIGHT), on the basis that we don't
        # yet know whether the ball will be in the top or bottom half of the screen when it reaches our position on
        # the X axis. By waiting at a central position, we're as ready as it's possible to be for all eventualities.
        target_y_1 = HALF_HEIGHT

        # If the ball is close, we want to move towards its position on the Y axis. We also apply a small offset which
        # is randomly generated each time the ball bounces. This is to make the computer player slightly less robotic
        # - a human player wouldn't be able to hit the ball right in the centre of the bat each time.
        target_y_2 = game.ball.y + game.ai_offset

        # The final step is to work out the actual Y position we want to move towards. We use what's called a weighted
        # average - taking the average of the two target Y positions we've previously calculated, but shifting the
        # balance towards one or the other depending on how far away the ball is. If the ball is more than 400 pixels
        # (half the screen width) away on the X axis, our target will be half the screen height (target_y_1). If the
        # ball is at the same position as us on the X axis, our target will be target_y_2. If it's 200 pixels away,
        # we'll aim for halfway between target_y_1 and target_y_2. This reflects the idea that as the ball gets closer,
        # we have a better idea of where it's going to end up.
        weight1 = min(1, x_distance / HALF_WIDTH)
        weight2 = 1 - weight1

        target_y = (weight1 * target_y_1) + (weight2 * target_y_2)

        # Subtract target_y from our current Y position, then make sure we can't move any further than MAX_AI_SPEED
        # each frame
        return min(MAX_AI_SPEED, max(-MAX_AI_SPEED, target_y - self.y))


class Game:
    def __init__(self, controls=(None, None)):
        # Create a list of two bats, giving each a player number and a function to use to receive
        # control inputs (or the value None if this is intended to be an AI player)
        self.bats = [Bat(0, controls[0]), Bat(1, controls[1])]

        # Create a ball object
        self.ball = Ball(-1)

        # Create an empty list which will later store the details of currently playing impact
        # animations - these are displayed for a short time every time the ball bounces
        self.impacts = []

        # Add an offset to the AI player's target Y position, so it won't aim to hit the ball exactly
        # in the centre of the bat
        self.ai_offset = 0

    def update(self):
        # Actualiza todos los objetos activos
        for obj in self.bats + [self.ball] + self.impacts:
            obj.update()

            # Elimine los efectos de impacto vencidos de la lista.
            # Repasamos la lista al revés, comenzando desde el último
            # elemento, y elimine cualquier elemento cuyo atributo
            # de tiempo haya llegado a 10.
            # Vamos hacia atrás a través de la lista.
            # en lugar de reenviar para evitar una serie de problemas
            # que ocurren en ese escenario.
            # En el próximo capítulo busque una técnica alternativa
            # para eliminar elementos de una lista, utilizando
            # listas por comprensión.

            for i in range(len(self.impacts) - 1, -1, -1):
                if self.impacts[i].time >= 10:
                    del self.impacts[i]

        # Has ball gone off the left or right edge of the screen?
        if self.ball.out():
            # Work out which player gained a point, based on whether the ball
            # was on the left or right-hand side of the screen
            scoring_player = 1 if self.ball.x < WIDTH // 2 else 0
            losing_player = 1 - scoring_player

            # We use the timer of the player who has just conceded a point to decide when to create a new ball in the
            # centre of the level. This timer starts at zero at the beginning of the game and counts down by one every
            # frame. Therefore, on the frame where the ball first goes off the screen, the timer will be less than zero.
            # We set it to 20, which means that this player's bat will display a different animation frame for 20
            # frames, and a new ball will be created after 20 frames
            if self.bats[losing_player].timer < 0:
                self.bats[scoring_player].score += 1

                game.play_sound("score_goal", 1)

                self.bats[losing_player].timer = 20

            elif self.bats[losing_player].timer == 0:
                # After 20 frames, create a new ball, heading in the direction of the player who just missed the ball
                direction = -1 if losing_player == 0 else 1
                self.ball = Ball(direction)

    def draw(self):
        # Draw background
        screen.blit("table", (0, 0))

        # Draw 'just scored' effects, if required
        for p in (0, 1):
            if self.bats[p].timer > 0 and game.ball.out():
                screen.blit("effect" + str(p), (0, 0))

        # Draw bats, ball and impact effects - in that order. Square brackets are needed around the ball because
        # it's just an object, whereas the other two are lists - and you can't directly join an object onto a
        # list without first putting it in a list
        for obj in self.bats + [self.ball] + self.impacts:
            obj.draw()

        # Display scores - outer loop goes through each player
        for p in (0, 1):
            # Convert score into a string of 2 digits (e.g. "05") so we can later get the individual digits
            score = "{0:02d}".format(self.bats[p].score)
            # Inner loop goes through each digit
            for i in (0, 1):
                # Digit sprites are numbered 00 to 29, where the first digit is the colour (0 = grey,
                # 1 = blue, 2 = green) and the second digit is the digit itself
                # Colour is usually grey but turns red or green (depending on player number) when a
                # point has just been scored
                colour = "0"
                other_p = 1 - p
                if self.bats[other_p].timer > 0 and game.ball.out():
                    colour = "2" if p == 0 else "1"
                image = "digit" + colour + str(score[i])
                screen.blit(image, (255 + (160 * p) + (i * 55), 46))

    def play_sound(self, name, count=1):
        # Some sounds have multiple varieties. If count > 1, we'll randomly choose one from those
        # We don't play any in-game sound effects if player 0 is an AI player - as this means we're on the menu
        if self.bats[0].move_func != self.bats[0].ai:
            # Pygame Zero allows you to write things like 'sounds.explosion.play()'
            # This automatically loads and plays a file named 'explosion.wav' (or .ogg) from the sounds folder (if
            # such a file exists)
            # But what if you have files named 'explosion0.ogg' to 'explosion5.ogg' and want to randomly choose
            # one of them to play? You can generate a string such as 'explosion3', but to use such a string
            # to access an attribute of Pygame Zero's sounds object, we must use Python's built-in function getattr
            try:
                getattr(sounds, name + str(random.randint(0, count - 1))).play()
            except:
                pass


def p1_controls():
    move = 0
    if keyboard.z or keyboard.down:
        move = PLAYER_SPEED
    elif keyboard.a or keyboard.up:
        move = -PLAYER_SPEED
    return move


def p2_controls():
    move = 0
    if keyboard.m:
        move = PLAYER_SPEED
    elif keyboard.k:
        move = -PLAYER_SPEED
    return move


class State(Enum):
    MENU = 1
    PLAY = 2
    GAME_OVER = 3


num_players = 1

# Is space currently being held down?
space_down = False


# Pygame Zero calls the update and draw functions each frame

def update():
    global state, game, num_players, space_down

    # Work out whether the space key has just been pressed - i.e. in the previous frame it wasn't down,
    # and in this frame it is.
    space_pressed = False
    if keyboard.space and not space_down:
        space_pressed = True
    space_down = keyboard.space

    if state == State.MENU:
        if space_pressed:
            # Switch to play state, and create a new Game object, passing it the controls function for
            # player 1, and if we're in 2 player mode, the controls function for player 2 (otherwise the
            # 'None' value indicating this player should be computer-controlled)
            state = State.PLAY
            controls = [p1_controls]
            controls.append(p2_controls if num_players == 2 else None)
            game = Game(controls)
        else:
            # Detect up/down keys
            if num_players == 2 and keyboard.up:
                sounds.up.play()
                num_players = 1
            elif num_players == 1 and keyboard.down:
                sounds.down.play()
                num_players = 2

            # Update the 'attract mode' game in the background (two AIs playing each other)
            game.update()

    elif state == State.PLAY:
        # Has anyone won?
        if max(game.bats[0].score, game.bats[1].score) > 9:
            state = State.GAME_OVER
        else:
            game.update()

    elif state == State.GAME_OVER:
        if space_pressed:
            # Reset to menu state
            state = State.MENU
            num_players = 1

            # Create a new Game object, without any players
            game = Game()


def draw():
    game.draw()

    if state == State.MENU:
        menu_image = "menu" + str(num_players - 1)
        screen.blit(menu_image, (0, 0))

    elif state == State.GAME_OVER:
        screen.blit("over", (0, 0))


# The mixer allows us to play sounds and music
try:
    pygame.mixer.quit()
    pygame.mixer.init(44100, -16, 2, 1024)

    music.play("theme")
    music.set_volume(0.3)
except:
    # If an error occurs (e.g. no sound device), just ignore it
    pass

# Set the initial game state
state = State.MENU

# Create a new Game object, without any players
game = Game()

# Tell Pygame Zero to start - this line is only required when running the game from an IDE such as IDLE or PyCharm
pgzrun.go()
