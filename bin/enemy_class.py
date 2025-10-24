from pgzero.actor import Actor
from pgzero.animation import animate
import random
from config import *
from pygame import Rect
from audio_manager import AudioManager
class Enemy(Actor):
    def __init__(self, start_image, x, y, walk_frames, idle_frames, tile_size, game_map, patrol_distance=3,game_manager=None):
        super().__init__(start_image, (x, y))
        self.walk_frames = walk_frames
        self.idle_frames = idle_frames
        self.current_frames = idle_frames
        self.tile_size = tile_size
        self.game_map = game_map
        self.game_manager = game_manager    
        self.grid_x = int(x // tile_size)
        self.grid_y = int(y // tile_size)
        self.x = self.grid_x * self.tile_size + self.tile_size // 2
        self.y = self.grid_y * self.tile_size + self.tile_size // 2
        self.is_moving = False
        self.frame_index = 0
        self.target_x = self.x
        self.target_y = self.y
        self.animation_speed = 0.2
        self.frame_timer = 0
        self.patrol_distance = patrol_distance
        self.start_grid_x = self.grid_x
        self.start_grid_y = self.grid_y
        self.patrol_direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        self.patrol_timer = 0
        self.patrol_cooldown = 1.0
    def can_move_to(self, grid_x, grid_y):
        grid_x = int(grid_x)
        grid_y = int(grid_y)
        
        if grid_x < 0 or grid_x >= len(self.game_map[0]) or grid_y < 0 or grid_y >= len(self.game_map):
            return False
        
        tile_value = self.game_map[grid_y][grid_x]
        return tile_value not in SOLID_TILES

    def update(self, dt, player):
        self.patrol_timer += dt
        
        if not self.is_moving and self.patrol_timer >= self.patrol_cooldown:
            self.try_patrol_move()
        
        self.animate(dt)
 
    def try_patrol_move(self):
        dx, dy = self.patrol_direction
        
        new_grid_x = self.grid_x + dx
        new_grid_y = self.grid_y + dy
        
        if (self.can_move_to(new_grid_x, new_grid_y) and 
            abs(new_grid_x - self.start_grid_x) <= self.patrol_distance and 
            abs(new_grid_y - self.start_grid_y) <= self.patrol_distance):
            
            self.move_to(new_grid_x, new_grid_y)
        else:
            directions = [(1,0), (-1,0), (0,1), (0,-1)]
            random.shuffle(directions)
            
            for new_dx, new_dy in directions:
                new_grid_x = self.grid_x + new_dx
                new_grid_y = self.grid_y + new_dy
                
                if (self.can_move_to(new_grid_x, new_grid_y) and 
                    abs(new_grid_x - self.start_grid_x) <= self.patrol_distance and 
                    abs(new_grid_y - self.start_grid_y) <= self.patrol_distance):
                    
                    self.patrol_direction = (new_dx, new_dy)
                    self.move_to(new_grid_x, new_grid_y)
                    break
            
            self.patrol_timer = 0

    def move_to(self, grid_x, grid_y):
        self.target_x = grid_x * self.tile_size + self.tile_size // 2
        self.target_y = grid_y * self.tile_size + self.tile_size // 2
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.is_moving = True
        
        animate(
            self, 
            duration=0.3, 
            x=self.target_x, 
            y=self.target_y, 
            on_finished=self.stop_move
        )

    def stop_move(self):
        self.is_moving = False
        self.x = self.target_x
        self.y = self.target_y
        self.patrol_timer = 0

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

    def collides_with(self, player):
        enemy_rect = Rect(self.x - 10, self.y - 10, 20, 20)
        player_rect = Rect(player.x - 10, player.y - 10, 20, 20)
        return enemy_rect.colliderect(player_rect)
    def play_enemy_sound(self, sfx_name):
        audio_manager = AudioManager.get_instance()
        audio_manager.play_sfx(sfx_name)