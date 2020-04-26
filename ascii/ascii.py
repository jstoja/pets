from PIL import Image
from typing import List, Tuple

BRIGHTNESS_CHARACTERS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

def load_image(file_name: str) -> List[List[Tuple[int, int, int]]]:
    im = Image.open(file_name)
    max_x = im.size[0]
    max_y = im.size[1]
    print("Successfully loaded image!")
    print("Format:", im.format)
    print("Size: {} x {}".format(im.size[0], im.size[1]))

    pixels = []
    data = list(im.getdata())
    for y in range(max_y):
        pixels.append(data[y*max_x:(y*max_x + max_x)])
    return pixels

def colors_to_brightness(pixels: List[List[Tuple[int, int, int]]], brightness_function) -> List[List[int]]:
    brightness_map = []
    for y in range(len(pixels)):
        brightness_map.append([int(brightness_function(pixels[y][x])) for x in range(len(pixels[y]))])
    return brightness_map

def average_brightness(pixel: Tuple[int, int, int]) -> float:
    r, g, b = pixel
    return (r + g + b) / 3

def brightness_to_ascii(pixels: List[List[int]], brightness_chars: str) -> List[List[str]]:
    def brightness_to_char(brightness: int, chars: str) -> str:
        i = int(brightness * len(chars) / 255)
        return brightness_chars[i]
    ascii_map = []
    for y in range(len(pixels)):
        ascii_map.append([brightness_to_char(pixels[y][x], brightness_chars) for x in range(len(pixels[y]))])
    return ascii_map

def print_ascii(pixels: List[List[str]]) -> None:
    for y in range(len(pixels)):
        line = []
        for x in range(len(pixels[y])):
            line.append("{}{}{}".format(pixels[y][x], pixels[y][x], pixels[y][x]))
        print("".join(line))

def main():
    file_name = "ascii-pineapple.jpg"
    pixels = load_image(file_name)
    brightness_pixels = colors_to_brightness(pixels, average_brightness)
    ascii_pixels = brightness_to_ascii(brightness_pixels, BRIGHTNESS_CHARACTERS)
    print_ascii(ascii_pixels)

if __name__ == "__main__":
    main()
