import pygame
import sys
import threading
import multiprocessing
from rama_game_directory import rama_game
from project_food import food_game
import os


def __main__():

    base_path = os.path.dirname(os.path.abspath(__file__))

    def process_alive() -> bool:
        nonlocal processes
        for process in processes.values():
            if process is not None and process.is_alive():
                return True
        return False

    def play_audio(clip_path):
        pygame.mixer.music.load(clip_path)
        pygame.mixer.music.play()

    pygame.init()

    WIDTH = 1280
    HEIGHT = 720

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    processes = {
        'rama': None,
        'food': None,
    }

    error_audio_path = os.path.join(base_path, './main_assets/erro.mp3')

    bg_img = pygame.image.load(os.path.join(base_path, './main_assets/images/background.png'))
    bg_rect = bg_img.get_rect()

    ramayana_img = pygame.image.load(os.path.join(base_path, './main_assets/images/ramayana.png')).convert_alpha()
    ramayana_rect = ramayana_img.get_rect(midtop=(WIDTH / 2, 330))

    food_img = pygame.image.load(os.path.join(base_path, './main_assets/images/food.png')).convert_alpha()
    food_rect = food_img.get_rect(midtop=(WIDTH / 2, 530))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                for process in processes.values():
                    if process is not None and process.is_alive():
                        process.kill()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and ramayana_rect.collidepoint(pygame.mouse.get_pos()):
                pass
                if not process_alive():
                    processes['rama'] = multiprocessing.Process(target=rama_game.__main__)
                    processes['rama'].start()
                else:
                    error_thread = threading.Thread(target=play_audio, args=(error_audio_path,))
                    error_thread.start()
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and food_rect.collidepoint(pygame.mouse.get_pos()):
                pass
                if not process_alive():
                    processes['food'] = multiprocessing.Process(target=food_game.__main__)
                    processes['food'].start()
                else:
                    error_thread = threading.Thread(target=play_audio, args=(error_audio_path,))
                    error_thread.start()

        screen.fill((0, 0, 0))

        screen.blit(bg_img, bg_rect)
        screen.blit(ramayana_img, ramayana_rect)
        screen.blit(food_img, food_rect)

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    # Start the main process
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn')
    main_process = multiprocessing.Process(target=__main__)
    main_process.start()
    main_process.join()
