import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
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
    def __init__(self, x, y, width, height, text, color, text_color, active=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.active = active
        
    def draw(self, surface):
        color = self.color if self.active else GRAY
        pygame.draw.rect(surface, color, self.rect, 2)
        text_surface = font.render(self.text, True, self.text_color if self.active else GRAY)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def is_clicked(self, pos):
        return self.active and self.rect.collidepoint(pos)

class Card:
    def __init__(self, x, y, width, height, card_id, fixed_position=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.card_id = card_id
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.fixed_position = fixed_position
        self.original_x = x
        self.original_y = y
        
    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        card_text = small_font.render(str(self.card_id), True, BLACK)
        card_text_rect = card_text.get_rect(center=self.rect.center)
        surface.blit(card_text, card_text_rect)
    
    def update_position(self, x, y):
        if not self.fixed_position:
            self.rect.x = x
            self.rect.y = y
            self.original_x = x
            self.original_y = y
        else:
        
            pass
    
    def reset_to_fixed_position(self):
        if self.fixed_position:
            self.rect.x = self.original_x
            self.rect.y = self.original_y
    
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
        
        start_button = Button(center_x, 150, button_width, button_height, "START", WHITE, WHITE)
        decks_button = Button(center_x, 250, button_width, button_height, "Колоды", WHITE, WHITE)
        quit_button = Button(center_x, 350, button_width, button_height, "QUIT", WHITE, WHITE)
        
        start_button.draw(screen)
        decks_button.draw(screen)
        quit_button.draw(screen)
        
        pygame.display.flip()

def decks_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        
        screen.fill(BLACK)
        
        title_text = font.render("Выбор колоды (без выбора)", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)
        
        rect_width = 200
        rect_height = 100
        rect_x = SCREEN_WIDTH // 2 - rect_width // 2
        rect_y = SCREEN_HEIGHT // 2 - rect_height // 2
        pygame.draw.rect(screen, WHITE, (rect_x, rect_y, rect_width, rect_height))
        
        pygame.display.flip()

def game_screen():
    # Индикаторы
    top_indicator_x = SCREEN_WIDTH - 100
    top_indicator_y = 50
    bottom_indicator_x = SCREEN_WIDTH - 100
    bottom_indicator_y = SCREEN_HEIGHT - 100
    
    # Верхняя колода
    top_deck_x = top_indicator_x - 80
    top_deck_y = top_indicator_y - 30
    top_deck_width = 60
    top_deck_height = 80
    
    # Нижняя колода
    bottom_deck_x = bottom_indicator_x - 80
    bottom_deck_y = bottom_indicator_y - 30
    bottom_deck_width = 60
    bottom_deck_height = 80
    
    # Кнопки
    button_width = 200
    button_height = 50
    end_turn_button = Button(SCREEN_WIDTH - button_width - 20, SCREEN_HEIGHT // 2 - 25, 
                             button_width, button_height, "Конец хода", GRAY, GRAY, active=False)
    hand_button = Button(SCREEN_WIDTH - button_width - 20, SCREEN_HEIGHT // 2 + 40, 
                         button_width, button_height, "Рука", WHITE, WHITE, active=True)
    
    # Размер карт
    card_width = 90
    card_height = 120
    
    # Середина 
    line_y = SCREEN_HEIGHT // 2
    
    # ВР
    center_card_x = SCREEN_WIDTH // 2 - card_width // 2
    center_card_y = line_y + 50
    center_card = Card(center_card_x, center_card_y, card_width, card_height, "Карта", fixed_position=True)
    
    # Фиксированные позиции для карт по бокам
    left_positions = []
    right_positions = []
    spacing = 15
    
    # Левая сторона 
    for i in range(3):
        pos_x = center_card_x - card_width - 30 - i * (card_width + spacing)
        pos_y = center_card_y
        left_positions.append((pos_x, pos_y))
    
    # Правая сторона 
    for i in range(3):
        pos_x = center_card_x + card_width + 30 + i * (card_width + spacing)
        pos_y = center_card_y
        right_positions.append((pos_x, pos_y))
    
    # Карты в руке
    hand_cards = []
    for i in range(5):
        hand_cards.append(Card(0, 0, card_width, card_height, i + 1, fixed_position=False))
    
    # Карты в зонах
    left_zone_cards = []
    right_zone_cards = []
    
    # Перетаскивание
    dragged_card = None
    original_owner = None
    original_index = -1
    original_fixed_state = False
    
    # Показывать руку
    show_cards = False
    
    # Обновления позиций карт в руке
    def update_hand_positions():
        if not show_cards:
            return
            
        cards_spacing = 15
        current_cards_count = len(hand_cards)
        
        if current_cards_count > 0:
            total_width = current_cards_count * card_width + (current_cards_count - 1) * cards_spacing
            start_x = (SCREEN_WIDTH - total_width) // 2
            cards_y = SCREEN_HEIGHT - card_height - 20
            
            for i, card in enumerate(hand_cards):
                card_x = start_x + i * (card_width + cards_spacing)
                card.update_position(card_x, cards_y)
    
    # Фиксация в зоне
    def update_zone_positions():
        # Левая зона
        for i, card in enumerate(left_zone_cards):
            if i < len(left_positions):
                card.original_x = left_positions[i][0]
                card.original_y = left_positions[i][1]
                card.rect.x = left_positions[i][0]
                card.rect.y = left_positions[i][1]
        
        # Правая зона
        for i, card in enumerate(right_zone_cards):
            if i < len(right_positions):
                card.original_x = right_positions[i][0]
                card.original_y = right_positions[i][1]
                card.rect.x = right_positions[i][0]
                card.rect.y = right_positions[i][1]
    
    # Определение зон
    left_zone_rect = pygame.Rect(0, center_card_y - card_height, 
                                 center_card_x - 20, card_height * 2)
    right_zone_rect = pygame.Rect(center_card_x + card_width + 20, center_card_y - card_height, 
                                  SCREEN_WIDTH - (center_card_x + card_width + 20), card_height * 2)
    
    # Инициализация
    update_hand_positions()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hand_button.is_clicked(event.pos):
                    show_cards = not show_cards
                    if show_cards:
                        update_hand_positions()
                
                # Проверка нажатия на карты в руке
                if show_cards:
                    for i, card in enumerate(hand_cards):
                        if card.is_clicked(event.pos):
                            dragged_card = card
                            original_owner = "hand"
                            original_index = i
                            original_fixed_state = card.fixed_position
                            drag_x, drag_y = event.pos
                            card.drag_offset_x = card.rect.x - drag_x
                            card.drag_offset_y = card.rect.y - drag_y
                            card.is_dragging = True
                            break
                
                # Проверка нажатия на карты в левой зоне
                for i, card in enumerate(left_zone_cards):
                    if card.is_clicked(event.pos):
                        dragged_card = card
                        original_owner = "left_zone"
                        original_index = i
                        original_fixed_state = card.fixed_position
                        drag_x, drag_y = event.pos
                        card.drag_offset_x = card.rect.x - drag_x
                        card.drag_offset_y = card.rect.y - drag_y
                        card.is_dragging = True
                        break
                
                # Проверка нажатия на карты в правой зоне
                for i, card in enumerate(right_zone_cards):
                    if card.is_clicked(event.pos):
                        dragged_card = card
                        original_owner = "right_zone"
                        original_index = i
                        original_fixed_state = card.fixed_position
                        drag_x, drag_y = event.pos
                        card.drag_offset_x = card.rect.x - drag_x
                        card.drag_offset_y = card.rect.y - drag_y
                        card.is_dragging = True
                        break
            
            if event.type == pygame.MOUSEMOTION and dragged_card and dragged_card.is_dragging:
                drag_x, drag_y = event.pos
                new_x = drag_x + dragged_card.drag_offset_x
                new_y = drag_y + dragged_card.drag_offset_y
                dragged_card.rect.x = new_x
                dragged_card.rect.y = new_y
            
            if event.type == pygame.MOUSEBUTTONUP and dragged_card and dragged_card.is_dragging:
                placed = False
                
                # Проверка левой зоны
                if left_zone_rect.colliderect(dragged_card.rect) and len(left_zone_cards) < 3:
                    if original_owner == "left_zone":
                        left_zone_cards.pop(original_index)
                    elif original_owner == "right_zone":
                        right_zone_cards.pop(original_index)
                    elif original_owner == "hand":
                        hand_cards.pop(original_index)
                    
                    dragged_card.fixed_position = True
                    left_zone_cards.append(dragged_card)
                    placed = True
                
                # Проверка правой зоны
                elif right_zone_rect.colliderect(dragged_card.rect) and len(right_zone_cards) < 3:
                    if original_owner == "left_zone":
                        left_zone_cards.pop(original_index)
                    elif original_owner == "right_zone":
                        right_zone_cards.pop(original_index)
                    elif original_owner == "hand":
                        hand_cards.pop(original_index)
                    
                    dragged_card.fixed_position = True
                    right_zone_cards.append(dragged_card)
                    placed = True
                
                # Если не положили в зону
                if not placed:
                    if original_owner == "hand":
                        hand_cards.insert(original_index, dragged_card)
                        dragged_card.fixed_position = False
                    elif original_owner == "left_zone":
                        left_zone_cards.insert(original_index, dragged_card)
                        dragged_card.fixed_position = True
                    elif original_owner == "right_zone":
                        right_zone_cards.insert(original_index, dragged_card)
                        dragged_card.fixed_position = True
                
                dragged_card.is_dragging = False
                dragged_card = None
                original_owner = None
                original_index = -1
                
                # Обновляем позиции карт 
                update_zone_positions()
                if show_cards:
                    update_hand_positions()
        

        screen.fill(BLACK)
        
        # Горизонтальная разделяющая линия
        pygame.draw.line(screen, WHITE, (0, line_y), (SCREEN_WIDTH, line_y), 2)
        

        top_text = small_font.render("0", True, WHITE)
        bottom_text = small_font.render("0", True, WHITE)
        screen.blit(top_text, (top_indicator_x, top_indicator_y))
        screen.blit(bottom_text, (bottom_indicator_x, bottom_indicator_y))
        
        # Верхняя колода
        pygame.draw.rect(screen, WHITE, (top_deck_x, top_deck_y, top_deck_width, top_deck_height))
        top_deck_text = small_font.render("Колода", True, BLACK)
        top_deck_text_rect = top_deck_text.get_rect(center=(top_deck_x + top_deck_width // 2, top_deck_y + top_deck_height // 2))
        screen.blit(top_deck_text, top_deck_text_rect)
        
        # Нижняя колода
        pygame.draw.rect(screen, WHITE, (bottom_deck_x, bottom_deck_y, bottom_deck_width, bottom_deck_height))
        bottom_deck_text = small_font.render("Колода", True, BLACK)
        bottom_deck_text_rect = bottom_deck_text.get_rect(center=(bottom_deck_x + bottom_deck_width // 2, bottom_deck_y + bottom_deck_height // 2))
        screen.blit(bottom_deck_text, bottom_deck_text_rect)
        
        # Кнопки
        end_turn_button.draw(screen)
        hand_button.draw(screen)
        
        # Центральная карта
        center_card.draw(screen)
        
        # Карты в зонах
        for card in left_zone_cards:
            card.draw(screen)
        for card in right_zone_cards:
            card.draw(screen)
        
        # Карты в руке
        if show_cards:
            for card in hand_cards:
                if card != dragged_card:
                    card.draw(screen)
            
            if dragged_card and dragged_card.is_dragging:
                dragged_card.draw(screen)
        
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()