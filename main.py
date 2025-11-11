import pygame
import json
from utils.checkword import WordChecker

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_NAME = 'arial'

# --- Block Class ---
class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, char):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((50, 50))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.char = char
        self.font = pygame.font.Font(self.game.font, 30)
        text_surface = self.font.render(self.char, True, WHITE)
        text_rect = text_surface.get_rect(center=self.image.get_rect().center)
        self.image.blit(text_surface, text_rect)


# --- Player Class ---
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.image.load('assets/Fighter/Idle.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100)


# --- Game Class ---
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Type or Die")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.match_font(FONT_NAME)
        self.running = True
        self.word_checker = WordChecker()
        self.load_data()
        self.question_index = 0
        self.current_question = ""
        self.current_answer = ""
        self.user_text = ""
        self.message = ""
        self.message_color = WHITE
        self.block_tower = []
        self.timer = 30
        self.start_time = 0
        self.score = 0
        self.game_over = False
        self.background = pygame.image.load('assets/Background/Bright/Background.png').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def load_data(self):
        with open('database.json') as f:
            self.questions = json.load(f)

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.select_question()
        self.run()

    def select_question(self):
        if self.question_index < len(self.questions):
            question_data = self.questions[self.question_index]
            self.current_question = question_data['question']
            self.current_answer = question_data['answer']
            self.user_text = ""
            self.start_time = pygame.time.get_ticks()
        else:
            # Game over, player wins
            self.game_over = True
            self.playing = False

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        time_elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
        self.timer = 30 - time_elapsed
        if self.timer <= 0:
            self.message = "Time's up!"
            self.message_color = (255, 0, 0)
            self.clear_tower()
            self.question_index += 1
            self.select_question()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    is_valid, message, color = self.word_checker.check_word(self.user_text)
                    self.message = message
                    self.message_color = color
                    if is_valid:
                        # Check answer
                        if self.user_text.lower() in [ans.lower() for ans in self.current_answer]:
                            self.score += int(self.timer) * 10
                            self.add_blocks(self.user_text)
                            self.question_index += 1
                            self.select_question()
                        else:
                            self.message = "Wrong answer!"
                            self.message_color = (255, 0, 0)
                            self.clear_tower()
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                else:
                    self.user_text += event.unicode

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def add_blocks(self, answer):
        x = SCREEN_WIDTH / 2
        y_start = SCREEN_HEIGHT - 50 * len(self.block_tower)
        for i, char in enumerate(answer):
            y = y_start - (i + 1) * 50
            block = Block(self, x, y, char)
            self.all_sprites.add(block)
            self.block_tower.append(block)

    def clear_tower(self):
        for block in self.block_tower:
            block.kill()
        self.block_tower = []

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        self.draw_text(self.current_question, 30, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        self.draw_text(self.user_text, 40, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.draw_text(f"Time: {int(self.timer)}", 25, WHITE, 60, 20)
        self.draw_text(f"Score: {self.score}", 25, WHITE, SCREEN_WIDTH - 60, 20)
        if self.message:
            self.draw_text(self.message, 20, self.message_color, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)

        if self.game_over:
            self.draw_text("You Win!", 60, (0, 255, 0), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50)
            self.draw_text(f"Final Score: {self.score}", 40, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20)

        pygame.display.flip()

    def show_start_screen(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_text("Type or Die", 64, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        self.draw_text("Press any key to start", 22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        pygame.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        if not self.running:
            return
        self.screen.blit(self.background, (0, 0))
        self.draw_text("GAME OVER", 48, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        self.draw_text("Press a key to play again", 22, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

# --- Main ---
if __name__ == '__main__':
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.show_go_screen()

    pygame.quit()
# --- End of Main ---
