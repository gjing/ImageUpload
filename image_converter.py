from PIL import Image
from copy import deepcopy
import xxhash
import io, sys


def process_image(file):
    image_file, thumbnail_file = io.BytesIO(), io.BytesIO()
    im = Image.open(file)
    filename = xxhash.xxh32(file.read()).hexdigest()
    result = im
    if im.getpalette():
        result.putpalette(im.getpalette())

    thumbnail = deepcopy(im)
    width, height = thumbnail.size
    if width > height:
        height = int(height * 150 / width)
        width = 150
    else:
        width = int(width * 150 / height)
        height = 150
    thumbnail = thumbnail.resize((width, height))
    thumbnail.save(thumbnail_file, format='WEBP')
    thumbnail_file.seek(0)
    
    duration = im.info.get("duration", None)
    result.save(image_file, format='WEBP', duration=duration, save_all=True)
    image_file.seek(0)
    return filename, image_file.read(), thumbnail_file.read()

if __name__ == '__main__':
    n, im, thumb = None, None, None
    with open(sys.argv[1], 'rb') as f:
        n, im, thumb = process_image(f)
    with open(n + "_full.webp", 'wb') as f:
        f.write(im)
    with open(n + "_thumb.webp", 'wb') as f:
        f.write(thumb)