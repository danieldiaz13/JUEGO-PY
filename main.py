import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Definir constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FPS = 60

# Definir la clase de la nave espacial
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.x = max(0, min(SCREEN_WIDTH - self.rect.width, self.rect.x))

# Definir la clase de los invasores alienígenas
class Alien(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        if self.color == "blue":
            self.image = pygame.Surface((30, 30))
            self.image.fill(BLUE)
        elif self.color == "green":
            self.image = pygame.Surface((30, 30))
            self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

# Función para mostrar un mensaje en la pantalla
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Función principal del juego
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders")

    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    aliens = pygame.sprite.Group()

    ship = Ship()
    all_sprites.add(ship)

    score = 0

    # Función para mostrar el menú principal
    def show_menu():
        screen.fill(BLACK)
        draw_text(screen, "Space Invaders", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        draw_text(screen, "Presiona ESPACIO para comenzar", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.flip()

        waiting = True
        while waiting:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

    show_menu()

    # Loop del juego
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualizar
        all_sprites.update()

        # Crear nuevos invasores
        if len(aliens) < 10:
            alien = Alien(random.choice(["blue", "green"]))
            all_sprites.add(alien)
            aliens.add(alien)

        # Colisiones - Nave vs. Invasores
        hits = pygame.sprite.spritecollide(ship, aliens, True)
        for hit in hits:
            if hit.color == "blue":
                running = False  # Fin del juego si toca un invasor azul
            elif hit.color == "green":
                score += 10  # Sumar 10 puntos si toca un invasor verde

        # Dibujar
        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_text(screen, f"Puntuación: {score}", 18, SCREEN_WIDTH // 2, 10)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
