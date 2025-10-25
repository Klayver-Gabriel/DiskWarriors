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
        self.button_rects = []  
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
        
        self.button_rects = []
        
        button1_rect = Rect(WIDTH/2 - 150, HEIGHT/5 - 20, 300, 40)
        self.button_rects.append(button1_rect)
        color_play = "Yellow" if self.selected_state == 1 else "white"
        screen.draw.text(
            "Começar o Jogo",
            center=(WIDTH/2, HEIGHT/5),
            fontsize=30,
            color=color_play
        )
        
        button2_rect = Rect(WIDTH/2 - 200, HEIGHT/4 - 20, 400, 40)
        self.button_rects.append(button2_rect)
        color_music = "Yellow" if self.selected_state == 2 else "white"
        music_state = "Música e sons ligados" if self.music_active == True else "Música e sons desligados"
        screen.draw.text(
            music_state,
            center=(WIDTH/2, HEIGHT/4),
            fontsize=30,
            color=color_music
        )
        button3_rect = Rect(WIDTH/2 - 80, HEIGHT/3 - 20, 160, 40)
        self.button_rects.append(button3_rect)
        color_exit = "Yellow" if self.selected_state == 3 else "white"
        screen.draw.text(
            "Sair",
            center=(WIDTH/2, HEIGHT/3),
            fontsize=30,
            color=color_exit
        )
    def handle_menu_selection(self):
        if self.selected_state == 3:
            raise SystemExit
        elif self.selected_state == 2:
            self.music_active = not self.music_active
        elif self.selected_state == 1:
            self.set_state("JOGANDO")
            if game_manager.music_active:
                audio_manager.play_music()
    
    def handle_menu_input(self, key):
        if key == keys.DOWN or key == keys.S:
            self.selected_state = (self.selected_state % self.max_states) + 1
            play_sfx("menu_move")
        elif key == keys.UP or key == keys.W:
            if self.selected_state == 1:
                self.selected_state = 3
                play_sfx("menu_move")
            else:
                self.selected_state = self.selected_state - 1
                play_sfx("menu_move")
        elif key == keys.E or key == keys.RETURN:
            self.handle_menu_selection()

    def handle_menu_click(self, pos):
        x, y = pos
        for i, rect in enumerate(self.button_rects):
            if rect.collidepoint(x, y):
                self.selected_state = i + 1
                self.handle_menu_selection()

game_manager = GameStateManager()
audio_manager = AudioManager.get_instance()
audio_manager.initialize(sounds)
audio_manager.music_active = game_manager.music_active

player = Player(WIDTH/4, HEIGHT/2,
                TILE_SIZE,game_map,game_manager)
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
                
                enemy = Enemy('slimeidle', x * TILE_SIZE, y * TILE_SIZE, 
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
    player.movement_logic(dt)  
       
    for enemy in enemies:
        enemy.update(dt)
        if enemy.collides_with(player):
            game_manager.set_state("GAME_OVER")
            music.stop()
            if game_manager.music_active:
                music.play("gameover")
    pass

def on_key_down(key):

    if game_manager.state == "MENU":
        game_manager.handle_menu_input(key)
def on_mouse_down(pos):
    if game_manager.state == "MENU":
        if game_manager.music_active:
            play_sfx("menu_move")
        game_manager.handle_menu_click(pos)
        


pgzrun.go()