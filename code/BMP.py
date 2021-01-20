import struct

from PIL import Image

def read_rows(path, width):
    """
    Helper function for the check_all_same_color function
    """
    image_file = open(path, "rb")
    # Blindly skip the BMP header.
    image_file.seek(54)

    # We need to read pixels in as rows to later swap the order
    # since BMP stores pixels starting at the bottom left.
    rows = []
    row = []
    pixel_index = 0

    while True:
        if pixel_index == width:
            pixel_index = 0
            rows.insert(0, row)
            row = []
        pixel_index += 1

        r_string = image_file.read(1)
        g_string = image_file.read(1)
        b_string = image_file.read(1)

        if len(r_string) == 0:
            # This is expected to happen when we've read everything.
            break

        if len(g_string) == 0:
            break

        if len(b_string) == 0:
            break

        r = ord(r_string)
        g = ord(g_string)
        b = ord(b_string)

        row.append(b)
        row.append(g)
        row.append(r)

    image_file.close()

    return rows

def repack_sub_pixels(rows):
    sub_pixels = []
    for row in rows:
        for sub_pixel in row:
            sub_pixels.append(sub_pixel)
    return sub_pixels

def checkEqualIvo(lst):
    return not lst or lst.count(lst[0]) == len(lst)


def check_if_all_same_color(path):
    """
    Check if the image in the given path is a unicolor image
    """
    if path.endswith(".bmp"):
        bmp = open(path, 'rb')
        #reading the bytes before the width and length
        bmp.read(18)
        width=struct.unpack('I', bmp.read(4))[0]
        rows = read_rows(path,width)

        # This list is raw sub-pixel values. A red image is for example (255, 0, 0, 255, 0, 0, ...).
        sub_pixels = repack_sub_pixels(rows)
        return checkEqualIvo(sub_pixels)
    else:
        try:
            im = Image.open(path)
            pixels = [im.getpixel((i, j)) for j in range(im.height) for i in range(im.width)]
            return len(set(pixels))==1
        except:
            return True






