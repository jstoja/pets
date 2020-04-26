from PIL import Image
from typing import List, Tuple, Iterator, Callable
import itertools


BRIGHTNESS_CHARACTERS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
CORRECT_SIZE_RATIO = 3


def load_image(file_name: str, size: Tuple[int, int]) -> Iterator[Tuple[int, int, int]]:
    im = Image.open(file_name)
    print("Successfully loaded image!")
    print("Format:", im.format)
    print("Size: {} x {}".format(im.size[0], im.size[1]))
    yield from im.resize(size).getdata()


def colors_to_brightness(pixels: Iterator[Tuple[int, int, int]],
        brightness_function: Callable[[Tuple[int, int, int]], int]) -> Iterator[int]:
    for pixel in pixels:
        yield brightness_function(pixel)


def average_brightness(pixel: Tuple[int, int, int]) -> int:
    r, g, b = pixel
    return int((r + g + b) / 3)


def lightness_brightness(pixel: Tuple[int, int, int]) -> int:
    r, g, b = pixel
    return int((max(r, g, b) + min(r, g, b)) / 2)


def luminosity_brightness(pixel: Tuple[int, int, int]) -> int:
    r, g, b = pixel
    return int(0.21*r + 0.72*g + 0.07*b)


def brightness_to_char(brightness: int, chars: str) -> str:
    i = int(brightness * len(chars) / 255)
    return chars[i]


def brightness_to_ascii(pixels: Iterator[int], brightness_chars: str) -> Iterator[str]:
    for pixel in pixels:
        yield brightness_to_char(pixel, brightness_chars)


def correct_size(pixels: Iterator[str], ratio: int) -> Iterator[str]:
    for pixel in pixels:
        yield from itertools.repeat(pixel, ratio)


def print_ascii(pixels: Iterator[str], size_x: int) -> None:
    i = 0
    for pixel in pixels:
        print(pixel, end="")
        if i % size_x == 0:
            print()
        i += 1
    print()


# TODO: Add argparse for:
#   * filename
#   * resize (maybe use termcaps instead)
#   * brightness function
#   ...
def main():
    file_name = "ascii-pineapple.jpg"
    pixels = load_image(file_name, (700, 467))
    brightness_pixels = colors_to_brightness(pixels, lightness_brightness)
    ascii_pixels = brightness_to_ascii(brightness_pixels, BRIGHTNESS_CHARACTERS)
    corrected_size_ascii = correct_size(ascii_pixels, CORRECT_SIZE_RATIO)
    print_ascii(corrected_size_ascii, 700*CORRECT_SIZE_RATIO)

if __name__ == "__main__":
    main()
