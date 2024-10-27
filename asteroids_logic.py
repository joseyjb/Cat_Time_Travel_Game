import random, enum
from pygame import mixer

import pygame

from game_logic import GameLogic

class AsteroidsLogic(GameLogic):
    @property
    def title(self):
        return "The Future"

    # Enumerator for different game states
    class _GameStates(enum.Enum):
        PLAYING = enum.auto()
        LOST = enum.auto()
    
    # Weird hack to init *after* PyGame
    _has_completed_init = False
    @staticmethod
    def _init_helper() -> None:
        if AsteroidsLogic._has_completed_init: return

        AsteroidsLogic._has_completed_init = True

        #background
        AsteroidsLogic._bg_surface = pygame.image.load('images/space_background.png').convert()

        #cat in spaceship
        AsteroidsLogic._cat_spaceship = pygame.image.load("images/cat_spaceship.png").convert_alpha()
        #Set new size for cat in space space
        AsteroidsLogic._cat_spaceship = pygame.transform.scale_by(AsteroidsLogic._cat_spaceship, 3)
        AsteroidsLogic._cat_spaceship_rect = AsteroidsLogic._cat_spaceship.get_rect(center = (220,240))

        # asteroid
        AsteroidsLogic._asteroid_surface = pygame.image.load("images/Asteroid.png").convert_alpha()
        # New size of asteroid 
        AsteroidsLogic._asteroid_surface = pygame.transform.scale_by(AsteroidsLogic._asteroid_surface, 0.4)

        AsteroidsLogic._game_font = pygame.font.Font('pixel_font.ttf',40)

    # Static Game Variables
    _gravity = 0.125
    _asteroid_height = [100, 150, 200, 250, 300, 350]

    _bg_surface: pygame.Surface
    _cat_spaceship: pygame.Surface
    _cat_spaceship_rect: pygame.Rect
    _asteroid_surface: pygame.Surface
    _game_font: pygame.font.Font

    _is_game_requesting_stop: bool = False

    def __init__(self, screen):
        super().__init__(screen)
        self._init_helper()

        # Instance Game Variables
        self._cat_movement = 0
        self._score = 0
        self._high_score = 0
        self._game_state = self._GameStates.PLAYING

        self._asteroid_list: pygame.Rect = []

        self._SPAWN_ASTEROID = pygame.event.custom_type()
        pygame.time.set_timer(self._SPAWN_ASTEROID, 1200)
        
    def _create_asteroid(self):
        random_asteroid_pos = random.choice(self._asteroid_height)
        new_asteroid = self._asteroid_surface.get_rect(midtop = (600, random_asteroid_pos))
        self._asteroid_list.append(new_asteroid)
        if len(self._asteroid_list) > 25: self._asteroid_list.pop(0)

    def _move_asteroids(self):
        for asteroid in self._asteroid_list:
             asteroid.centerx -= 5

    def _draw_asteroids(self):
         for asteroid in self._asteroid_list:
              self._screen.blit(self._asteroid_surface, asteroid)

    def _check_collision(self):
        for asteroid in self._asteroid_list:
           if self._cat_spaceship_rect.colliderect(asteroid):
            return False
        if self._cat_spaceship_rect.bottom <= 0 or self._cat_spaceship_rect.top >= self._screen.get_size()[1]:
            return False
        return True

    def _reset_asteroids(self):
        self._asteroid_list = []

    def _score_display(self):
        score_surface = self._game_font.render(str(int(self._score)), True,(255, 255, 255))
        score_rect = score_surface.get_rect(center = (320, 100))
        self._screen.blit(score_surface, score_rect)

    def _high_score_display(self) -> None:
        score_surface = self._game_font.render(f'Score: {(int(self._score))}\nPress R to restart\nPress ESC to quit', True,(255, 255, 255))
        score_rect = score_surface.get_rect(center = (320, 100))
        self._screen.blit(score_surface, score_rect)
        high_score_surface = self._game_font.render(f'High score: {(int(self._high_score))}', True,(255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (320, 400))
        self._screen.blit(high_score_surface, high_score_rect)

    def _update_high_score(self) -> None:
        if self._score > self._high_score:
             self._high_score = self._score

    def process_events(self, event: pygame.event.Event):
        super().process_events(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and (self._game_state == self._GameStates.PLAYING):
                self._cat_movement = -6

            if event.key == pygame.K_r and (self._game_state == self._GameStates.LOST):
                self._reset_game()

            if event.key == pygame.K_ESCAPE:
                self._is_game_requesting_stop = True

        if event.type == self._SPAWN_ASTEROID:
            self._create_asteroid()

    def draw_frame(self, delta_t):
        super().draw_frame(delta_t)

        self._screen.blit(self._bg_surface, (0, 0))

        match self._game_state:
            case self._GameStates.PLAYING:
                #cat
                self._cat_movement += self._gravity
                self._cat_spaceship_rect.centery += self._cat_movement
                self._screen.blit(self._cat_spaceship, self._cat_spaceship_rect)
                
                if not self._check_collision():
                    self._game_state = self._GameStates.LOST
                
                #asteroids
                self._move_asteroids()
                self._draw_asteroids()

                #score
                self._score += 0.005
                self._score_display()

            case self._GameStates.LOST:
                self._update_high_score()
                self._high_score_display()
                
    @property
    def is_game_requesting_stop(self):
        return self._is_game_requesting_stop
    
    def _reset_game(self) -> None:
        self._game_state = self._GameStates.PLAYING
        self._reset_asteroids()
        self._cat_spaceship_rect.centery = 240
        self._cat_movement = -6
        self._score = 0
        self._is_game_requesting_stop = False

    def start_game(self) -> None:
        super().start_game()
        self._reset_game()
        mixer.music.load("audio/andromeda.opus")
        mixer.music.set_volume(0.7)
        mixer.music.play(-1)
    
    def stop_game(self):
        super().stop_game()
        mixer.music.stop()
    