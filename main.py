import pygame
import sys
import json
import os

# Инициализация Pygame
pygame.init()

# Файл для сохранения
CONFIG_FILE = "game_config.json"


DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600
DEFAULT_FULLSCREEN = False

# Функция загрузки
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return (config.get('screen_width', DEFAULT_WIDTH), 
                       config.get('screen_height', DEFAULT_HEIGHT),
                       config.get('fullscreen', DEFAULT_FULLSCREEN))
        except:
            return DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_FULLSCREEN
    return DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_FULLSCREEN

# Функция сохранения
def save_config(width, height, fullscreen):
    config = {
        'screen_width': width,
        'screen_height': height,
        'fullscreen': fullscreen
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

# Загрузка сохраненных настроек
SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN = load_config()

# Создание окна с учетом полноэкранного режима
if FULLSCREEN:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

pygame.display.set_caption("Коллекционная карточная игра")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (169, 169, 169)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Шрифты
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)
tiny_font = pygame.font.Font(None, 18)

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
    def __init__(self, x, y, width, height, card_id, attack=0, health=0, fixed_position=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.card_id = card_id
        self.attack = attack
        self.health = health
        self.max_health = health
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.fixed_position = fixed_position
        self.original_x = x
        self.original_y = y
        self.selected_for_attack = False
        self.can_attack_this_turn = True
        
    def draw(self, surface):
        # Рисуем карту
        if self.selected_for_attack:
            pygame.draw.rect(surface, YELLOW, self.rect)
            pygame.draw.rect(surface, WHITE, self.rect, 3)
        else:
            pygame.draw.rect(surface, WHITE, self.rect)
            pygame.draw.rect(surface, BLACK, self.rect, 2)
        

        if isinstance(self.card_id, str):
            card_text = tiny_font.render(self.card_id, True, BLACK)
        else:
            card_text = tiny_font.render(f"Карта {self.card_id}", True, BLACK)
        card_text_rect = card_text.get_rect(center=(self.rect.centerx, self.rect.y + 15))
        surface.blit(card_text, card_text_rect)
        
        # Атака и здоровье
        if self.attack > 0:
            attack_text = tiny_font.render(f"{self.attack}", True, RED)
            attack_rect = attack_text.get_rect(bottomleft=(self.rect.x + 5, self.rect.bottom - 5))
            surface.blit(attack_text, attack_rect)
        
        if self.health > 0:
            health_text = tiny_font.render(f"{self.health}/{self.max_health}", True, GREEN)
            health_rect = health_text.get_rect(bottomright=(self.rect.right - 5, self.rect.bottom - 5))
            surface.blit(health_text, health_rect)
    
    def update_position(self, x, y):
        if not self.fixed_position:
            self.rect.x = x
            self.rect.y = y
            self.original_x = x
            self.original_y = y
    
    def reset_to_fixed_position(self):
        if self.fixed_position:
            self.rect.x = self.original_x
            self.rect.y = self.original_y
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0

def toggle_fullscreen():
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen, FULLSCREEN
    
    FULLSCREEN = not FULLSCREEN
    
    display_info = pygame.display.Info()
    
    if FULLSCREEN:
        SCREEN_WIDTH = display_info.current_w
        SCREEN_HEIGHT = display_info.current_h
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    else:
        config = load_config()
        SCREEN_WIDTH = config[0]
        SCREEN_HEIGHT = config[1]
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    
    save_config(SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN)

def settings_screen():
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen, FULLSCREEN
    
    resolutions = [
        (800, 600),
        (1024, 768),
        (1280, 720),
        (1366, 768),
        (1600, 900),
        (1920, 1080)
    ]
    
    selected_resolution = (SCREEN_WIDTH, SCREEN_HEIGHT) if not FULLSCREEN else resolutions[0]
    
    resolution_buttons = []
    button_width = 200
    button_height = 40
    start_y = 100
    
    for i, res in enumerate(resolutions):
        btn = Button(SCREEN_WIDTH // 2 - button_width // 2, start_y + i * 50, button_width, button_height, f"{res[0]}x{res[1]}", WHITE if res != selected_resolution else LIGHT_GRAY,WHITE)
        resolution_buttons.append((btn, res))
    
    apply_button = Button(SCREEN_WIDTH // 2 - 100, 
                         start_y + len(resolutions) * 50 + 30,
                         200, 50, 
                         "Применить", 
                         WHITE, WHITE)
    
    back_button = Button(SCREEN_WIDTH // 2 - 100, 
                        start_y + len(resolutions) * 50 + 90,
                        200, 50, 
                        "Назад", 
                        WHITE, WHITE)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_F1:
                    toggle_fullscreen()
                    return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn, res in resolution_buttons:
                    if btn.is_clicked(event.pos):
                        selected_resolution = res
                        for b, r in resolution_buttons:
                            b.color = WHITE if r != selected_resolution else LIGHT_GRAY
                
                if apply_button.is_clicked(event.pos) and not FULLSCREEN:
                    SCREEN_WIDTH, SCREEN_HEIGHT = selected_resolution
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                    save_config(SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN)
                    
                    for btn, _ in resolution_buttons:
                        btn.rect.centerx = SCREEN_WIDTH // 2
                    apply_button.rect.centerx = SCREEN_WIDTH // 2
                    back_button.rect.centerx = SCREEN_WIDTH // 2
                
                if back_button.is_clicked(event.pos):
                    return
        
        screen.fill(BLACK)
        
        title_text = font.render("Настройки разрешения", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)
        
        if FULLSCREEN:
            mode_text = font.render("Полноэкранный режим активен", True, LIGHT_GRAY)
            mode_rect = mode_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
            screen.blit(mode_text, mode_rect)
            info_text = small_font.render("Нажмите F1 для выхода из полноэкранного режима", True, GRAY)
            info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
            screen.blit(info_text, info_rect)
        else:
            current_text = small_font.render(f"Текущее разрешение: {SCREEN_WIDTH}x{SCREEN_HEIGHT}", True, LIGHT_GRAY)
            current_rect = current_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
            screen.blit(current_text, current_rect)
            
            for btn, _ in resolution_buttons:
                btn.rect.centerx = SCREEN_WIDTH // 2
                btn.draw(screen)
            
            apply_button.rect.centerx = SCREEN_WIDTH // 2
            back_button.rect.centerx = SCREEN_WIDTH // 2
            apply_button.draw(screen)
            back_button.draw(screen)
        
        hint_text = small_font.render("F1 - полноэкранный режим | ESC - назад", True, GRAY)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(hint_text, hint_rect)
        
        pygame.display.flip()

def main_menu():
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen, FULLSCREEN
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE and not FULLSCREEN:
                SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                save_config(SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    toggle_fullscreen()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event.pos):
                    game_screen()
                if decks_button.is_clicked(event.pos):
                    decks_screen()
                if settings_button.is_clicked(event.pos):
                    settings_screen()
                if quit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()
        
        screen.fill(BLACK)
        
        button_width = 200
        button_height = 50
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        
        start_button = Button(center_x, 100, button_width, button_height, "START", WHITE, WHITE)
        decks_button = Button(center_x, 170, button_width, button_height, "Колоды", WHITE, WHITE)
        settings_button = Button(center_x, 240, button_width, button_height, "Настройки", WHITE, WHITE)
        quit_button = Button(center_x, 310, button_width, button_height, "QUIT", WHITE, WHITE)
        
        start_button.draw(screen)
        decks_button.draw(screen)
        settings_button.draw(screen)
        quit_button.draw(screen)
        
        mode_text = "Fullscreen" if FULLSCREEN else "Windowed"
        res_text = small_font.render(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT} | {mode_text} | F1", True, GRAY)
        screen.blit(res_text, (10, SCREEN_HEIGHT - 30))
        
        pygame.display.flip()

def decks_screen():
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen, FULLSCREEN
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_F1:
                    toggle_fullscreen()
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
        
        hint_text = small_font.render("Нажмите ESC для возврата | F1 - полноэкранный режим", True, GRAY)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(hint_text, hint_rect)
        
        pygame.display.flip()

def game_screen():
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen, FULLSCREEN
    
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
    
    # Карта "Враг"
    enemy_card_width = 120
    enemy_card_height = 160
    enemy_card_x = SCREEN_WIDTH // 2 - enemy_card_width // 2
    enemy_card_y = 50
    enemy_card = Card(enemy_card_x, enemy_card_y, enemy_card_width, enemy_card_height, "Враг", attack=3, health=15, fixed_position=True)
    
    # Кнопки размеры
    button_width = 200
    button_height = 50
    end_turn_button = Button(SCREEN_WIDTH - button_width - 20, SCREEN_HEIGHT // 2 - 25, button_width, button_height, "Конец хода", GRAY, GRAY, active=False)
    hand_button = Button(SCREEN_WIDTH - button_width - 20, SCREEN_HEIGHT // 2 + 40, button_width, button_height, "Рука", WHITE, WHITE, active=True)
    attack_button = Button(SCREEN_WIDTH - button_width - 20, SCREEN_HEIGHT // 2 + 105, button_width, button_height, "Атака", WHITE, WHITE, active=True)
    
    # Параметры карт
    card_width = 90
    card_height = 120
    
    line_y = SCREEN_HEIGHT // 2
    center_card_x = SCREEN_WIDTH // 2 - card_width // 2
    center_card_y = line_y + 50
    center_card = Card(center_card_x, center_card_y, card_width, card_height, "Карта", fixed_position=True)
    
    left_positions = []
    right_positions = []
    spacing = 15
    
    for i in range(3):
        pos_x = center_card_x - card_width - 30 - i * (card_width + spacing)
        pos_y = center_card_y
        left_positions.append((pos_x, pos_y))
    
    for i in range(3):
        pos_x = center_card_x + card_width + 30 + i * (card_width + spacing)
        pos_y = center_card_y
        right_positions.append((pos_x, pos_y))
    
    # Карты в руке
    hand_cards = []
    for i in range(5):
        hand_cards.append(Card(0, 0, card_width, card_height, i + 1, attack=2, health=3, fixed_position=False))
    
    # Карты в зонах (на столе)
    left_zone_cards = []
    right_zone_cards = []
    
    # Перетаскивание
    dragged_card = None
    original_owner = None
    original_index = -1
    
    # Показывать ли руку
    show_cards = False
    
    # Состояние атаки
    attack_mode = False
    selected_attacker = None
    
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
    
    def update_zone_positions():
        # Обновляем позиции карт в левой зоне
        for i, card in enumerate(left_zone_cards):
            if i < len(left_positions):
                card.original_x = left_positions[i][0]
                card.original_y = left_positions[i][1]
                card.rect.x = left_positions[i][0]
                card.rect.y = left_positions[i][1]
        
        # Обновляем позиции карт в правой зоне
        for i, card in enumerate(right_zone_cards):
            if i < len(right_positions):
                card.original_x = right_positions[i][0]
                card.original_y = right_positions[i][1]
                card.rect.x = right_positions[i][0]
                card.rect.y = right_positions[i][1]
    
    def perform_attack(attacker, target):
        target.take_damage(attacker.attack)
        attacker.take_damage(target.attack)
        
        # Проверяем, уничтожен ли атакующий
        if attacker.health <= 0:
            if attacker in left_zone_cards:
                left_zone_cards.remove(attacker)
            elif attacker in right_zone_cards:
                right_zone_cards.remove(attacker)
            update_zone_positions()
        
        for card in left_zone_cards + right_zone_cards:
            card.selected_for_attack = False
        enemy_card.selected_for_attack = False
    
    # Зоны для размещения карт
    left_zone_rect = pygame.Rect(0, center_card_y - card_height, center_card_x - 20, card_height * 2)
    right_zone_rect = pygame.Rect(center_card_x + card_width + 20, center_card_y - card_height, SCREEN_WIDTH - (center_card_x + card_width + 20), card_height * 2)
    
    update_hand_positions()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_F1:
                    toggle_fullscreen()
                    return
            
            if event.type == pygame.VIDEORESIZE and not FULLSCREEN:
                SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                save_config(SCREEN_WIDTH, SCREEN_HEIGHT, FULLSCREEN)
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hand_button.is_clicked(event.pos):
                    show_cards = not show_cards
                    update_hand_positions()
                
                if attack_button.is_clicked(event.pos):
                    attack_mode = not attack_mode
                    if attack_mode:
                        attack_button.color = YELLOW
                        for card in left_zone_cards + right_zone_cards:
                            card.selected_for_attack = True
                        enemy_card.selected_for_attack = True
                    else:
                        attack_button.color = WHITE
                        for card in left_zone_cards + right_zone_cards:
                            card.selected_for_attack = False
                        enemy_card.selected_for_attack = False
                        selected_attacker = None
                
                # Выбор атакующей карты
                if attack_mode and not selected_attacker:
                    for card in left_zone_cards + right_zone_cards:
                        if card.is_clicked(event.pos) and card.health > 0:
                            selected_attacker = card
                            attack_button.text = f"Атака врага"
                            attack_button.color = BLUE
                            break
                
                # Атака по врагу если выбран атакующий
                elif attack_mode and selected_attacker:
                    if enemy_card.is_clicked(event.pos) and enemy_card.health > 0:
                        perform_attack(selected_attacker, enemy_card)
                        attack_mode = False
                        attack_button.text = "Атака"
                        attack_button.color = WHITE
                        selected_attacker = None
                        for card in left_zone_cards + right_zone_cards:
                            card.selected_for_attack = False
                        enemy_card.selected_for_attack = False
                
                # Перетаскивание карт из руки на стол (только если не в режиме атаки)
                elif not attack_mode and show_cards:
                    for i, card in enumerate(hand_cards):
                        if card.is_clicked(event.pos):
                            dragged_card = card
                            original_owner = "hand"
                            original_index = i
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
                    hand_cards.pop(original_index)
                    dragged_card.fixed_position = True
                    left_zone_cards.append(dragged_card)
                    placed = True
                
                # Проверка правой зоны
                elif right_zone_rect.colliderect(dragged_card.rect) and len(right_zone_cards) < 3:
                    hand_cards.pop(original_index)
                    dragged_card.fixed_position = True
                    right_zone_cards.append(dragged_card)
                    placed = True
                
                # Если не положили в зону, возвращаем в руку
                if not placed:
                    hand_cards.insert(original_index, dragged_card)
                    dragged_card.fixed_position = False
                
                dragged_card.is_dragging = False
                dragged_card = None
                original_owner = None
                original_index = -1
                
                # Обновляем позиции
                update_zone_positions()
                update_hand_positions()
        
        screen.fill(BLACK)
        
        # Горизонтальная разделяющая линия
        pygame.draw.line(screen, WHITE, (0, line_y), (SCREEN_WIDTH, line_y), 2)
        
        # Индикаторы
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
        
        enemy_card.draw(screen)
        
        # Кнопки
        end_turn_button.draw(screen)
        hand_button.draw(screen)
        attack_button.draw(screen)
        
        # Центральная карта
        center_card.draw(screen)
        
        # Карты в зонах (на столе)
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
        
        # Подсказки
        hint_text = small_font.render("F1 - полноэкранный режим | ESC - выход", True, GRAY)
        screen.blit(hint_text, (10, SCREEN_HEIGHT - 25))
        
        if attack_mode and selected_attacker:
            attack_hint = small_font.render("Нажмите на карту Враг для атаки", True, YELLOW)
            screen.blit(attack_hint, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 50))
        elif attack_mode:
            attack_hint = small_font.render("Выберите карту для атаки", True, YELLOW)
            screen.blit(attack_hint, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT - 50))
        
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()