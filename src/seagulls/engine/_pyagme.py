import pygame

# We create our own versions of these because the pygame engine has some typing bugs.
# https://github.com/pygame/pygame/issues/839#issuecomment-812919220
Rect = pygame.rect.Rect
Surface = pygame.surface.Surface
Color = pygame.color.Color
PixelArray = pygame.pixelarray.PixelArray
Vector2 = pygame.math.Vector2
Vector3 = pygame.math.Vector3
