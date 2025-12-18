import abc

import pygame


class Screen(abc.ABC):
    @abc.abstractmethod
    def render(self, screen: pygame.Surface, dt: int):
        """
        Renders the screen on the given pygame surface.
        """
        raise NotImplementedError("Subclasses must implement render method")

    @abc.abstractmethod
    def is_overlay(self) -> bool:
        """
        Returns True if the screen is an overlay, False otherwise.

        When a screen is defined as an overlay, the screens in the
        render stack below it are still being rendered.
        """
        raise NotImplementedError("Subclasses must implement is_overlay method")

    def update(self, dt: int):
        """
        Updates the screen.
        This method is called before the screen is being rendered even if the
        screen is not part of the render stack this frame (see :func:`~clockpi_ui.screen.Screen.is_overlay`):
        """
        pass
