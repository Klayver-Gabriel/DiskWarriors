import pgzrun
import math
import random
from player_class import Player
from pgzero.keyboard import keys
from pgzero import music
from pgzero.rect import Rect

TITLE_SIZE = 16
WIDTH = 30 * TITLE_SIZE
HEIGHT = 30 * TITLE_SIZE
TITLE = "DiskWarriors"
PLAYER_WALK_FRAMES = ['player0','player1','player2']
PLAYER_IDLE_FRAMES = ['player0']

# Constantes para o mapa
TILE_WALL = 1
TILE_GROUND = 0
MAP_WIDTH = 30
MAP_HEIGHT = 30

def generate_map():
    map_data = []
    for y in range(MAP_HEIGHT):
        row = []
        for x in range(MAP_WIDTH):
            # Cria bordas como paredes
            if x == 0 or y == 0 or x == MAP_WIDTH-1 or y == MAP_HEIGHT-1:
                row.append(TILE_WALL)
            # Área central maior e mais aberta
            elif 3 <= x <= 26 and 3 <= y <= 26:
                # Menos paredes internas para melhor navegação
                if random.random() < 0.15:  # Reduzido para menos obstáculos
                    row.append(TILE_WALL)
                else:
                    row.append(TILE_GROUND)
            else:
                row.append(TILE_GROUND)
        map_data.append(row)
    
    # Garantir que a área inicial do player esteja livre
    start_x, start_y = 15, 15
    for y in range(start_y-2, start_y+3):
        for x in range(start_x-2, start_x+3):
            if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                map_data[y][x] = TILE_GROUND
    
    return map_data

# Gera o mapa
game_map = generate_map()

class GameStateManager:
    def __init__(self):
        self.state = "MENU"
        self.selected_state = 1
        self.max_states = 3
        self.music_active = True

    def set_state(self, new_state):
        self.state = new_state
        print(f"O jogo está no modo {new_state}")

    def draw_menu(self):
        screen.clear()

        screen.draw.text(
            "DiskWarriors", 
            center=(WIDTH/2, HEIGHT / 10), 
            fontsize=70, 
            color="white"
        )
        color_play = "Yellow" if self.selected_state == 1 else "white"
        screen.draw.text(
            "Começar o Jogo",
            center=(WIDTH/2,HEIGHT/5),
            fontsize= 30,
            color=color_play
        )
        color_music = "Yellow" if self.selected_state == 2 else "white"
        music_state = "Música e sons ligados" if self.music_active == True else "Música e sons desligados"
        screen.draw.text(
            music_state,
            center=(WIDTH/2,HEIGHT/4),
            fontsize=30,
            color=color_music
        )
        color_exit = "Yellow" if self.selected_state == 3 else "white"
        screen.draw.text(
            "Saída",
            center=(WIDTH/2,HEIGHT/3),
            fontsize=30,
            color=color_exit
        )
    
    def handle_menu_input(self, key):
        if key == keys.DOWN:
            self.selected_state = (self.selected_state % self.max_states) + 1
        elif key == keys.UP:
            if self.selected_state == 1:
                self.selected_state = 3
            else:
                self.selected_state -= 1
        elif key == keys.E:
            if self.selected_state == 3:
                raise SystemExit
            elif self.selected_state == 2:
                self.music_active = not self.music_active
            elif self.selected_state == 1:
                self.set_state("JOGANDO")
                background_music()

game_manager = GameStateManager()

player = Player('player0',
                WIDTH/4, HEIGHT/2,
                PLAYER_WALK_FRAMES,
                PLAYER_IDLE_FRAMES,
                TITLE_SIZE,game_map)

def draw():
    if game_manager.state == "MENU":
        game_manager.draw_menu()
    elif game_manager.state == "JOGANDO":
        screen.clear()
        screen.fill((255,255,255))
        
        # Desenhar o mapa
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                tile_type = game_map[y][x]
                if tile_type == TILE_WALL:
                    color = (100, 100, 150)  
                else:
                    color = (200, 200, 200)  
                
                screen.draw.filled_rect(
                    Rect(x * TITLE_SIZE, y * TITLE_SIZE, TITLE_SIZE, TITLE_SIZE),
                    color
                )
        
        player.draw()        

def update(dt):
    if game_manager.state != "JOGANDO":
        return
    player.movement_logic(dt,WIDTH,HEIGHT)  
       
   
    pass

def on_key_down(key):

    if game_manager.state == "MENU":
        game_manager.handle_menu_input(key)

def background_music():
    music.play("soundtrack")
def stop_background_music():
    music.stop()

def play_sfx(self, sfx_name):
        if self.music_active:
            try:
                sound = getattr(sounds, sfx_name, None)
                if sound:
                    sound.play()
            except AttributeError:
                 print(f"ERRO: Som '{sfx_name}' não encontrado.")
pgzrun.go()