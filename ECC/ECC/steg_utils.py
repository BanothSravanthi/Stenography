from PIL import Image

def encode_text_to_image(image_path, text, output_path):
    img = Image.open(image_path)
    binary = ''.join(format(ord(char), '08b') for char in text)
    pixels = img.load()
    idx = 0
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if idx < len(binary):
                r, g, b = pixels[i, j]
                r = (r & ~1) | int(binary[idx])
                pixels[i, j] = (r, g, b)
                idx += 1
    img.save(output_path)

def decode_text_from_image(image_path, length):
    img = Image.open(image_path)
    pixels = img.load()
    binary = ''
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = pixels[i, j]
            binary += str(r & 1)
            if len(binary) >= length * 8:
                break
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)
