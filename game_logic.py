import pygame
from abc import ABCMeta, abstractmethod

class GameLogic(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, screen: pygame.Surface):
        self._screen = screen

    @abstractmethod
    def process_events(self, event: pygame.event.Event) -> None:
        pass

    @abstractmethod
    def draw_frame(self, delta_t: float) -> None:
        pass
    
    @property
    @abstractmethod
    def is_game_requesting_stop(self) -> bool:
        pass

    @abstractmethod
    def start_game(self) -> None:
        pass

    @abstractmethod
    def stop_game(self) -> None:
        pass

    @property
    @abstractmethod
    def title(self) -> str:
        pass