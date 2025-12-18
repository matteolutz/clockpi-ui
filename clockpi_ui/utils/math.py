from typing import Tuple


def lerp_color(
    start_color: Tuple[int, int, int], end_color: Tuple[int, int, int], t: float
) -> Tuple[int, int, int]:
    return (
        int(start_color[0] + (end_color[0] - start_color[0]) * t),
        int(start_color[1] + (end_color[1] - start_color[1]) * t),
        int(start_color[2] + (end_color[2] - start_color[2]) * t),
    )


def lerp_color_4(
    start_color: Tuple[int, int, int, int],
    end_color: Tuple[int, int, int, int],
    t: float,
) -> Tuple[int, int, int, int]:
    return (
        int(start_color[0] + (end_color[0] - start_color[0]) * t),
        int(start_color[1] + (end_color[1] - start_color[1]) * t),
        int(start_color[2] + (end_color[2] - start_color[2]) * t),
        int(start_color[3] + (end_color[3] - start_color[3]) * t),
    )
