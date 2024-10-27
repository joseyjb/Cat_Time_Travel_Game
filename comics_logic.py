import pygame

from game_logic import GameLogic

class ComicsLogic(GameLogic):
    _comics_surface: pygame.surface.Surface

    _has_completed_init = False
    @staticmethod
    def _init_helper() -> None:
        if ComicsLogic._has_completed_init: return

        ComicsLogic._has_completed_init = True

        ComicsLogic._comics_surface = pygame.image.load('images/comics.png')

    def __init__(self, screen):
        super().__init__(screen)
        self._init_helper()
        self._is_game_requesting_stop = False

    def process_events(self, event) -> None:
        super().process_events(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._is_game_requesting_stop = True

    def draw_frame(self, delta_t):
        super().draw_frame(delta_t)

        self._screen.fill('#000000')
        self._screen.blit(self._comics_surface, ((self._screen.width - self._comics_surface.width)/2, 0))
    
    @property
    def is_game_requesting_stop(self) -> bool:
        return self._is_game_requesting_stop
    
    @property
    def title(self) -> str:
        return "Story"
    
    def start_game(self) -> None:
        self._is_game_requesting_stop = False
        super().start_game()
    
    def stop_game(self) -> None:
        super().stop_game()