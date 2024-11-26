import random
import pygame
import colorama
from colorama import Fore, Style

colorama.init()

# Definindo constantes para os caracteres
WATER = (0, 0, 255)  # Azul
SAND = (255, 255, 0)  # Amarelo
LAND = (0, 255, 0)  # Verde


def generate_random_island(width, height, island_size, beach_width, land_thickness):
    # Criando um mapa inicial com água
    map_grid = [[WATER for _ in range(width)] for _ in range(height)]

    # Gerando pontos aleatórios para a ilha
    island_points = set()

    for _ in range(island_size):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        island_points.add((x, y))

    # Preenchendo a ilha com espessura da terra
    for x, y in island_points:
        for dx in range(-land_thickness, land_thickness + 1):
            for dy in range(-land_thickness, land_thickness + 1):
                if 0 <= x + dx < width and 0 <= y + dy < height:
                    map_grid[y + dy][x + dx] = LAND

    # Adicionando areia ao redor da ilha com largura da praia
    for y in range(height):
        for x in range(width):
            if map_grid[y][x] == LAND:
                for bw in range(1, beach_width + 1):
                    for dx in range(-bw, bw + 1):
                        for dy in range(-bw, bw + 1):
                            if 0 <= x + dx < width and 0 <= y + dy < height:
                                if (abs(dx) + abs(dy)) == bw and map_grid[y + dy][x + dx] == WATER:
                                    if random.random() < 0.5:  # 50% de chance de ser areia
                                        map_grid[y + dy][x + dx] = SAND

    return map_grid


def draw_map(map_grid, cell_size):
    # Inicializando o Pygame
    pygame.init()

    # Dimensões da tela e configurações de mapa
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Ilha em ASCII")

    # Variáveis de controle para drag e zoom
    offset_x, offset_y = 0, 0
    dragging = False
    zoom_factor = cell_size

    # Loop principal do Pygame
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Início do "drag" ao pressionar o botão esquerdo do mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    dragging = True
                    drag_start_x, drag_start_y = event.pos  # Ponto de partida do "drag"

                # Zoom in/out com a roda do mouse
                elif event.button == 4:  # Scroll para cima (zoom in)
                    zoom_factor = min(zoom_factor + 2, 50)  # Limite de zoom in
                elif event.button == 5:  # Scroll para baixo (zoom out)
                    zoom_factor = max(zoom_factor - 2, 4)  # Limite de zoom out

            # Parar o "drag" ao soltar o botão do mouse
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False

            # Atualizar o offset com o movimento do mouse
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    dx, dy = event.rel  # Movimento relativo do mouse
                    offset_x += dx
                    offset_y += dy

        # Limpar a tela antes de redesenhar
        screen.fill((0, 0, 0))

        # Desenhar o mapa com o zoom e offset atualizados
        for y, row in enumerate(map_grid):
            for x, cell in enumerate(row):
                color = WATER if cell == WATER else SAND if cell == SAND else LAND
                pygame.draw.rect(
                    screen, color,
                    (x * zoom_factor + offset_x, y * zoom_factor + offset_y, zoom_factor, zoom_factor)
                )

        pygame.display.flip()  # Atualiza a tela

    pygame.quit()


if __name__ == "__main__":
    width = 100
    height = 100

    island_size = 50  # Número de pontos que compõem a ilha
    beach_width = 2  # Largura da praia
    land_thickness = 8  # Espessura da terra
    cell_size = 10

    # Gera o mapa da ilha
    island_map = generate_random_island(width, height, island_size, beach_width, land_thickness)

    # Desenha o mapa com opções de zoom e drag
    draw_map(island_map, cell_size)
