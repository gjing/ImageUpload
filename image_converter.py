from PIL import Image
import numpy as np
import io
import xxhash

def process_image(file):
    in_mem_file = io.BytesIO()
    im = Image.open(file)
    na = np.array(im)
    filename = xxhash.xxh32(na)
    result = Image.fromarray(na)
    if im.getpalette():
        result.putpalette(im.getpalette())
    result.save(in_mem_file, format='WEBP', save_all=True)
    in_mem_file.seek(0)
    return filename, in_mem_file