from typing import Optional, Tuple

import pygame
import pygame.freetype

from clockpi_ui.ui.colors import PRIMARY
from clockpi_ui.utils.paths import ASSETS_DIR


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
        # self._button_font = pygame.font.SysFont("Ubuntu", 20)
        self._button_font = pygame.freetype.Font(
            ASSETS_DIR / "fonts" / "Ubuntu" / "Ubuntu-Medium.ttf", 20
        )

    def render_with_pos_and_size(
        self,
        screen: pygame.Surface,
        pos: Tuple[int, int],
        size: Tuple[int, int],
        variant_override: Optional[ButtonVariant] = None,
        label_override: Optional[str] = None,
    ):
        self.render(screen, pygame.Rect(pos, size), variant_override, label_override)

    def render(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
        variant_override: Optional[ButtonVariant] = None,
        label_override: Optional[str] = None,
    ):
        variant = variant_override if variant_override else self._variant
        label = label_override if label_override else self._label

        self._rect = rect
        if variant == ButtonVariant.DEFAULT:
            pygame.draw.rect(screen, PRIMARY, self._rect, 0, 2)
        elif variant == ButtonVariant.OUTLINE:
            pygame.draw.rect(screen, PRIMARY, self._rect, 2, 2)
        elif variant == ButtonVariant.GHOST:
            # Just render text
            pass
        elif variant == ButtonVariant.HIDDEN:
            # Render nothing
            pass

        if variant != ButtonVariant.HIDDEN and label:
            text, rect = self._button_font.render(label, (255, 255, 255))
            screen.blit(
                text,
                (
                    self._rect.centerx - rect.width // 2,
                    self._rect.centery - rect.height // 2,
                ),
            )

    def was_clicked(self, mouse_pos: Tuple[int, int]) -> bool:
        if not self._rect:
            return False
        return self._rect.collidepoint(mouse_pos)
