import pygame
import sys

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Коллекционная карточная игра")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (169, 169, 169)
# Шрифты
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 2) 
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event.pos):
                    game_screen()
                if decks_button.is_clicked(event.pos):
                    decks_screen()
                if quit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()
        
        screen.fill(BLACK)
        
        button_width = 200
        button_height = 50
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        
        start_button = Button(center_x, 150, button_width, button_height, "СТАРТ", WHITE, WHITE)
        decks_button = Button(center_x, 250, button_width, button_height, "Колоды", WHITE, WHITE)
        quit_button = Button(center_x, 350, button_width, button_height, "ВЫХОД", WHITE, WHITE)
        
        start_button.draw(screen)
        decks_button.draw(screen)
        quit_button.draw(screen)
        
        pygame.display.flip()

def decks_screen(): # !!!!!!!!!!!!!! найти инфу на буд как раб система колода код сервер код колода (когда код нужен или не нужен) возможно это псиоп ветреная мельница и есть способ легче!!!!!!!!!!
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  
                    return
        screen.fill(BLACK)
        
        # Голова
        title_text = font.render("Выбор колоды (без выбора) также выход в меню на ESC", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)
        
        # Колода
        rect_width = 200
        rect_height = 400
        rect_x = SCREEN_WIDTH // 2 - rect_width // 2
        rect_y = SCREEN_HEIGHT // 2 - rect_height // 2
        pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_width, rect_height))
        
        pygame.display.flip()

def game_screen():
    top_indicator_x = SCREEN_WIDTH - 100
    top_indicator_y = 50
    bottom_indicator_x = SCREEN_WIDTH - 100
    bottom_indicator_y = SCREEN_HEIGHT - 100
    
    # Кнопка Конец хода !!!!!!!!!!!!!!! НЕ ЗАБУДЬ ПРО ТАЙМЕР ХОДА Я ЖЕ ТЕБЯ ЗНАЮ ЗАБУДЕШЬ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    button_width = 200
    button_height = 50
    end_turn_button = Button(SCREEN_WIDTH - button_width - 20, SCREEN_HEIGHT // 2 - 25, button_width, button_height, "Конец хода", GRAY, GRAY)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  
                    return
        screen.fill(BLACK)

        # Индикаторы верх низ (энергтя) !!! НЕ ЗАБУДЬ кол-во карт сюдаже колоде/руке навести или нажать !!!!!!!!НЕ ЗАБУДЬ проверку всунуть(только куда), карта взята или нет для отобр кол-во карт!!!!!!!!!!!!
        top_text = small_font.render("0", True, WHITE)
        bottom_text = small_font.render("0", True, WHITE)
        
        screen.blit(top_text, (top_indicator_x, top_indicator_y))
        screen.blit(bottom_text, (bottom_indicator_x, bottom_indicator_y))
        
        end_turn_button.draw(screen)
        
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()