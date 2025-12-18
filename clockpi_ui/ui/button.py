from typing import Optional, Tuple

import pygame
import pygame.freetype

from clockpi_ui.ui.colors import PRIMARY


class ButtonVariant:
    DEFAULT = 0
    OUTLINE = 1
    GHOST = 2
    HIDDEN = 3


class Button:
    def __init__(self, label: Optional[str] = None, variant=ButtonVariant.DEFAULT):
        self._rect = None
        self._label = label
        self._variant = variant
        self._button_font = self._alarm_time_font = pygame.font.SysFont("Arial", 20)

    def render_with_pos_and_size(
        self, screen: pygame.Surface, pos: Tuple[int, int], size: Tuple[int, int]
    ):
        self.render(screen, pygame.Rect(pos, size))

    def render(self, screen: pygame.Surface, rect: pygame.Rect):
        self._rect = rect
        if self._variant == ButtonVariant.DEFAULT:
            pygame.draw.rect(screen, PRIMARY, self._rect, 0, 2)
        elif self._variant == ButtonVariant.OUTLINE:
            pygame.draw.rect(screen, PRIMARY, self._rect, 2, 2)
        elif self._variant == ButtonVariant.GHOST:
            # Just render text
            pass
        elif self._variant == ButtonVariant.HIDDEN:
            # Render nothing
            pass

        if self._variant != ButtonVariant.HIDDEN and self._label:
            text = self._button_font.render(self._label, True, (255, 255, 255))
            screen.blit(
                text,
                (
                    self._rect.centerx - text.get_width() // 2,
                    self._rect.centery - text.get_height() // 2,
                ),
            )

    def was_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        if not self._rect:
            return False
        return self._rect.collidepoint(mouse_pos)
