import pygame
import sys
import random
import webbrowser
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_scaled(path):
    full_path = os.path.join(BASE_DIR, path)

    img = pygame.image.load(full_path).convert()
    return pygame.transform.scale(img, (WIDTH, HEIGHT))

pygame.init()

# ------------------ WINDOW ------------------
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EPIC: The Musical")

clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 28)
BIG_FONT = pygame.font.SysFont("arial", 50)

# ------------------ DATA ------------------
sagas = [
    ("Troy Saga", "Dec 25, 2022", "Images\\troy.jpg", "https://open.spotify.com/search/troy%20saga"),
    ("Cyclops Saga", "Jan 27, 2023", "Images\\cyclops.jpg", "https://open.spotify.com/search/cyclops%20saga"),
    ("Ocean Saga", "Dec 25, 2023", "Images\\ocean.jpg", "https://open.spotify.com/search/ocean%20saga"),
    ("Circe Saga", "Feb 14, 2024", "Images\\circe.jpg", "https://open.spotify.com/search/circe%20saga"),
    ("Underworld Saga", "Apr 26, 2024", "Images\\underworld.jpg", "https://open.spotify.com/search/underworld%20saga"),
    ("Thunder Saga", "Jul 4, 2024", "Images\\thunder.jpg", "https://open.spotify.com/search/thunder%20saga"),
    ("Wisdom Saga", "Aug 30, 2024", "Images\\wisdom.jpg", "https://open.spotify.com/search/wisdom%20saga"),
    ("Vengeance Saga", "Oct 31, 2024", "Images\\vengeance.jpg", "https://open.spotify.com/search/vengeance%20saga"),
    ("Ithaca Saga", "Dec 25, 2024", "Images\\ithica.jpg", "https://open.spotify.com/search/ithaca%20saga"),
]

# Load images
def load_scaled(path):
    full_path = os.path.join(BASE_DIR, path)
    img = pygame.image.load(full_path).convert()
    return pygame.transform.scale(img, (WIDTH, HEIGHT))

for i in range(len(sagas)):
    sagas[i] = (*sagas[i], load_scaled(sagas[i][2]))

# ------------------ STARFIELD ------------------
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.dx = random.uniform(-0.3, 0.3)
        self.dy = random.uniform(-0.3, 0.3)

    def update(self):
        self.x += self.dx
        self.y += self.dy

        # wrap around edges
        if self.x < 0: self.x = WIDTH
        if self.x > WIDTH: self.x = 0
        if self.y < 0: self.y = HEIGHT
        if self.y > HEIGHT: self.y = 0

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), 2)

stars = [Star() for _ in range(120)]

# ------------------ BUTTON ------------------
def draw_button(text, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, (40, 40, 60), rect, border_radius=10)
    pygame.draw.rect(screen, (150, 150, 255), rect, 2, border_radius=10)

    label = FONT.render(text, True, (255, 255, 255))
    screen.blit(label, (x + 15, y + h//2 - 10))

    return rect

# ------------------ STATE ------------------
current_saga = 0

# ------------------ MAIN LOOP ------------------
running = True

while running:
    screen.fill((0, 0, 0))

    saga = sagas[current_saga]
    title, date, img_path, link, image = saga

    # Background image
    screen.blit(image, (0, 0))

    # Dark overlay for readability
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(120)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Stars
    for star in stars:
        star.update()
        star.draw(screen)

    # Text
    title_text = BIG_FONT.render(title, True, (255, 255, 255))
    date_text = FONT.render(date, True, (200, 200, 200))

    screen.blit(title_text, (50, HEIGHT - 200))
    screen.blit(date_text, (50, HEIGHT - 140))

    # Buttons
    next_btn = draw_button("Next >", WIDTH - 160, HEIGHT - 80, 130, 50)
    prev_btn = draw_button("< Prev", 30, HEIGHT - 80, 130, 50)
    spotify_btn = draw_button("Open in Spotify", WIDTH//2 - 120, HEIGHT - 80, 240, 50)

    mouse = pygame.mouse.get_pos()
    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True

    # Button interactions
    if next_btn.collidepoint(mouse) and click:
        current_saga = (current_saga + 1) % len(sagas)

    if prev_btn.collidepoint(mouse) and click:
        current_saga = (current_saga - 1) % len(sagas)

    if spotify_btn.collidepoint(mouse) and click:
        webbrowser.open(link)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()