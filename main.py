import enum

import pygame.examples
import pygame, pygame_gui

from game_logic import GameLogic
from doodle_logic import DoodleLogic
from asteroids_logic import AsteroidsLogic
from comics_logic import ComicsLogic



GAME_MODE_CLASSES = [
    ComicsLogic,
    DoodleLogic,
    AsteroidsLogic,
]

SCREEN_SIZE = (640, 480)

class MajorModes(enum.Enum):
    TITLE_SCREEN = enum.auto()
    GAME_RUNNING = enum.auto()

def main():
    pygame.init()
    pygame.display.set_caption('Cat Traveler')
    pygame.font.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager(SCREEN_SIZE, 'themes.json')
    title_background = pygame.image.load('images/title-background.png').convert()

    game_modes: list[GameLogic] = [mode_class(screen) for mode_class in GAME_MODE_CLASSES]

    major_mode = MajorModes.TITLE_SCREEN
    active_game_logic: GameLogic
    
    game_buttons: list[pygame_gui.elements.UIButton] = []
    for n, game_logic in enumerate(game_modes):
        # Callback generator to enter the new game mode on title button press
        def make_button_pressed_callback(game_logic):
            def _button_cb_inner():
                nonlocal major_mode, active_game_logic

                major_mode = MajorModes.GAME_RUNNING
                active_game_logic = game_logic
                active_game_logic.start_game()
            
            return _button_cb_inner

        # List of buttons, configured and spaced as needed.
        # Not sure if the list is required but I am still a little
        # creeped out by the various whims of the garbage collector 
        game_buttons.append(pygame_gui.elements.UIButton(
            pygame.Rect(SCREEN_SIZE[0]*1/6, 
                        SCREEN_SIZE[1]/2/len(game_modes)*n + SCREEN_SIZE[1]/4 + 2, 
                        SCREEN_SIZE[0]*4/6, 
                        SCREEN_SIZE[1]/2/len(game_modes) - 4),
            game_logic.title,
            command=make_button_pressed_callback(game_logic),
            manager=manager,
        ))

        pygame_gui.elements.UITextBox(
            'Cat Traveler', 
            pygame.Rect(
                SCREEN_SIZE[0]*1/6,
                0,
                SCREEN_SIZE[0]*4/6,
                SCREEN_SIZE[1]/4
            ))

    while True:
        # Update timing stuff
        time_delta = clock.tick(120)/1000.0

        # Make sure the quit button hasn't been pressed
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        match major_mode:
            # Normal game activities
            case MajorModes.GAME_RUNNING:
                for event in events:
                    active_game_logic.process_events(event)

                if active_game_logic.is_game_requesting_stop:
                    active_game_logic.stop_game()
                    major_mode = MajorModes.TITLE_SCREEN
                
                active_game_logic.draw_frame(time_delta)

            # The title screen
            case MajorModes.TITLE_SCREEN:
                for event in events:
                    # Callbacks are already set, not much to do here
                    manager.process_events(event)

                manager.update(time_delta)

                screen.blit(title_background, (0, 0))
                manager.draw_ui(screen)

        pygame.display.update()

if __name__ == '__main__':
    main()