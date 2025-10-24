from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from pgzero.animation import animate
import pgzrun
from config import *
from audio_manager import AudioManager

class Player(Actor):
    def __init__(self, start_image, x, y, walk_frames, idle_frames, tile_size, game_map,game_manager=None):
        super().__init__(start_image, (x, y))
        self.walk_frames = walk_frames
        self.idle_frames = idle_frames
        self.speed = 2
        self.current_frames = idle_frames
        self.tile_size = tile_size
        self.game_map = game_map

        self.grid_x = int(x // self.tile_size)
        self.grid_y = int(y // self.tile_size)
        self.game_manager = game_manager
        self.x = self.grid_x * self.tile_size + self.tile_size // 2
        self.y = self.grid_y * self.tile_size + self.tile_size // 2
        self.is_moving = False
        self.frame_index = 0
        self.target_x = self.x
        self.target_y = self.y
        self.animation_speed = 0.2
        self.frame_timer = 0
    def can_move_to(self, grid_x, grid_y):
        grid_x = int(grid_x)
        grid_y = int(grid_y)
    
        if grid_x < 0 or grid_x >= len(self.game_map[0]) or grid_y < 0 or grid_y >= len(self.game_map):
            return False
    
        tile_value = self.game_map[grid_y][grid_x]
        return tile_value not in SOLID_TILES  
    def movement_logic(self, dt, WIDTH, HEIGHT):
        if self.is_moving:
            self.animate(dt)
            return
        
        dx, dy = 0, 0
        if keyboard.LEFT or keyboard.A:
            dx = -1
        elif keyboard.RIGHT or keyboard.D:
            dx = 1
        if keyboard.UP or keyboard.W:
            dy = -1
        if keyboard.DOWN or keyboard.S:
            dy = 1
        
        if dx != 0 or dy != 0:
            new_grid_x = self.grid_x + dx
            new_grid_y = self.grid_y + dy
            
            if self.can_move_to(new_grid_x, new_grid_y):

                self.target_x = new_grid_x * self.tile_size + self.tile_size // 2
                self.target_y = new_grid_y * self.tile_size + self.tile_size // 2
                self.grid_x = new_grid_x
                self.grid_y = new_grid_y
                self.is_moving = True

                animate(
                    self, 
                    duration=0.2, 
                    x=self.target_x, 
                    y=self.target_y, 
                    on_finished=self.stop_move
                )
                self.play_footstep_sound()
        self.animate(dt)

    def stop_move(self):
        self.is_moving = False
        self.x = self.target_x
        self.y = self.target_y
        
    def animate(self, dt):
        if self.is_moving:
            frames = self.walk_frames
        else:
            frames = self.idle_frames
        
        if frames != self.current_frames:
            self.current_frames = frames
            self.frame_index = 0
            
        self.frame_timer += dt 
        
        if self.frame_timer >= self.animation_speed:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.current_frames)
            self.image = self.current_frames[self.frame_index]

  
    def start_move(self, dx, dy, collision=False):
        if self.is_moving:
            return

        new_grid_x = self.grid_x + dx
        new_grid_y = self.grid_y + dy

        if self.can_move_to(new_grid_x, new_grid_y):
            self.grid_x = new_grid_x
            self.grid_y = new_grid_y
            self.target_x = self.grid_x * self.tile_size + self.tile_size // 2
            self.target_y = self.grid_y * self.tile_size + self.tile_size // 2
            self.is_moving = True
            
            
            animate(self, duration=0.15, x=self.target_x, y=self.target_y, on_finished=self.stop_move)
        
    def play_footstep_sound(self):
            audio_manager = AudioManager.get_instance()
            if self.game_manager.music_active:
                audio_manager.play_sfx("footstep00")
