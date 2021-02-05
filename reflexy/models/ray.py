import pygame
from reflexy.helpers import get_image_path


class Ray(pygame.sprite.Sprite):
    def __init__(self, screen, spider_coordenates, direction, aim_angle):
        pygame.sprite.Sprite.__init__(self)

        self.images = [
            self.get_surface(filename)
            for filename in (["ray-0.png", "ray-1.png", "ray-2.png", "ray-3.png"])
        ]

        self.current_image = 0
        self.image = self.images[self.current_image]

        self.current_angle = aim_angle

        [self.x, self.y] = spider_coordenates[0:2]

        self.rect = pygame.Rect(self.x, self.y, 128, 64)
        self.spider_eye = (self.rect[0] + 35, self.rect[1] + 11)

        self.blitRotate(screen, self.image, self.spider_eye, (0, 0), self.current_angle)

    def next_sprite(self, screen):
        self.current_image += 1
        if self.current_image >= len(self.images) - 1:
            self.current_image = len(self.images) - 1

        self.image = self.images[self.current_image]

        self.blitRotate(
            screen, self.image, self.spider_eye, (11, 18), self.current_angle
        )

    def get_surface(self, filename, angle=0, scale=1):
        return pygame.transform.rotozoom(
            pygame.image.load(get_image_path(filename)).convert_alpha(),
            angle,
            scale,
        )

    def blitRotate(self, screen, image, pos, originPos, angle):
        # calcaulate the axis aligned bounding box of the rotated image
        w, h = image.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(angle) for p in box]
        min_box = (
            min(box_rotate, key=lambda p: p[0])[0],
            min(box_rotate, key=lambda p: p[1])[1],
        )
        max_box = (
            max(box_rotate, key=lambda p: p[0])[0],
            max(box_rotate, key=lambda p: p[1])[1],
        )

        # calculate the translation of the pivot
        pivot = pygame.math.Vector2(originPos[0], -originPos[1])
        pivot_rotate = pivot.rotate(angle)
        pivot_move = pivot_rotate - pivot

        # calculate the upper left origin of the rotated image
        origin = (
            pos[0] - originPos[0] + min_box[0] - pivot_move[0],
            pos[1] - originPos[1] - max_box[1] + pivot_move[1],
        )

        # get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)

        # rotate and blit the image
        screen.blit(rotated_image, origin), rotated_image

        return rotated_image
