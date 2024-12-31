# pygame_test.py

# Импортировать библиотеку Pygame.
import pygame

# Инициализировать библиотеку Pygame.
pygame.init()

# Создать окно размером 800x600.
screen = pygame.display.set_mode((800, 600))
# Задать окну заголовок.
pygame.display.set_caption('Пример графического окна Pygame')


running = True

# Описание главного цикла игры.
# Этот цикл работает до тех пор, пока пользователь не закроет окно.
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Рисование линии.
    pygame.draw.line(screen, (255, 0, 0), (100, 100), (700, 500), 5)

    # Рисование квадрата.
    # Квадрат с верхним левым углом в точке (300, 200) и размерами 200x200
    # будет нарисован зелёным цветом.
    pygame.draw.rect(screen, (0, 128, 0), pygame.Rect(300, 200, 200, 200))

    # Отобразить нарисованные элементы в окне.
    pygame.display.update()


# Деинициализирует все модули pygame, которые были инициализированы ранее.
pygame.quit()
