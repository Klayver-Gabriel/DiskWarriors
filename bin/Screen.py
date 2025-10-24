import pgzrun
import math
import random
from player_class import Player
from enemy_class import Enemy
from pgzero.keyboard import keys
from pgzero import music
from config import *
from pygame import Rect
from audio_manager import AudioManager

TITLE = "DiskWarriors"
PLAYER_WALK_FRAMES = ['player0','player1','player2']
PLAYER_IDLE_FRAMES = ['player0']
ENEMY_WALK_FRAMES = ['player0','player1']
ENEMY_IDLE_FRAMES = ['player1']

def play_sfx(sfx_name):
    if game_manager.music_active:
        try:
            sound = getattr(sounds, sfx_name, None)
            if sound:
                sound.play()
        except AttributeError:
            print(f" '{sfx_name}' não encontrado.")    
def generate_map():
    map_data = []    
    for y in range(MAP_HEIGHT):
        row = []
        for x in range(MAP_WIDTH):
            if x == 0 or y == 0 or x == MAP_WIDTH-1 or y == MAP_HEIGHT-1:
                row.append(1)
            elif 5 <= x <= 24 and 5 <= y <= 24:
                rand = random.random()
                if rand < 0.6:
                    row.append(0) 
                elif rand < 0.8:
                    row.append(2) 
                else:
                    row.append(3) 
            else:
                rand = random.random()
                if rand < 0.5:
                    row.append(0)  
                elif rand < 0.75:
                    row.append(2) 
                else:
                    row.append(3)
        map_data.append(row)
    return map_data
game_map = generate_map()

class GameStateManager:
    def __init__(self):
        self.state = "MENU"
        self.selected_state = 1
        self.max_states = 3
        self.game_over_selected = 1
        self.music_active = True

    def set_state(self, new_state):
        self.state = new_state
    
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
            "Sair",
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
                if game_manager.music_active:
                    audio_manager.play_music()

game_manager = GameStateManager()
audio_manager = AudioManager.get_instance()
audio_manager.initialize(sounds)
audio_manager.music_active = game_manager.music_active

player = Player('player0',
                WIDTH/4, HEIGHT/2,
                PLAYER_WALK_FRAMES,
                PLAYER_IDLE_FRAMES,
                TILE_SIZE,game_map,game_manager=game_manager)
enemies = []
def create_enemies():
    enemy_positions = []
    for _ in range(5):  # Create 5 enemies
        for attempt in range(20):  # Try 20 times to find valid position
            x = random.randint(3, MAP_WIDTH-4)
            y = random.randint(3, MAP_HEIGHT-4)
            if (game_map[y][x] == TILE_GROUND and 
                abs(x - player.grid_x) > 5 and 
                abs(y - player.grid_y) > 5 and
                (x, y) not in enemy_positions):
                
                enemy = Enemy('player0', x * TILE_SIZE, y * TILE_SIZE, 
                            ENEMY_WALK_FRAMES, ENEMY_IDLE_FRAMES, 
                            TILE_SIZE, game_map, patrol_distance=4)
                enemies.append(enemy)
                enemy_positions.append((x, y))
                break

create_enemies()


def draw():
    if game_manager.state == "MENU":
        game_manager.draw_menu()
    elif game_manager.state == "JOGANDO":
        screen.clear()
        
        TILE_ASSETS = {
            0: 'grass',
            1: 'grass',
            2: 'grass2', 
            3: 'grass3'
        }        

        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                tile_value = game_map[y][x]
                asset_name = TILE_ASSETS[tile_value]
                screen.blit(asset_name, (x * TILE_SIZE, y * TILE_SIZE))
        
        for enemy in enemies:
            enemy.draw()
        if enemy.collides_with(player):
            raise
        player.draw()
    elif game_manager.state == "GAME_OVER":
        screen.clear()
        screen.draw.text(
            "Game Over", 
            center=(WIDTH/2, HEIGHT / 2), 
            fontsize=70, 
            color="red"
        )
def update(dt):
    if game_manager.state != "JOGANDO":
        return
    player.movement_logic(dt,WIDTH,HEIGHT)  
       
    for enemy in enemies:
        enemy.update(dt, player)
        if enemy.collides_with(player):
            game_manager.set_state("GAME_OVER")
            music.stop()
    pass

def on_key_down(key):

    if game_manager.state == "MENU":
        game_manager.handle_menu_input(key)



pgzrun.go()