from PIL import Image
from io import BytesIO

def exif_transpose(img):
    exif_orientation_tag = 274
    if hasattr(img, '_getexif'):
        exif_data = img._getexif()
        if exif_data is not None:
            orientation = exif_data.get(exif_orientation_tag, 1)
            orientation_transpose_map = {
                2: Image.FLIP_LEFT_RIGHT,
                3: Image.ROTATE_180,
                4: Image.FLIP_TOP_BOTTOM,
                5: Image.TRANSPOSE,
                6: Image.ROTATE_270,
                7: Image.TRANSVERSE,
                8: Image.ROTATE_90,
            }
            if orientation in orientation_transpose_map:
                img = img.transpose(orientation_transpose_map[orientation])
    return img

def ReSizeImages(avatar,W,H):
    image = Image.open(avatar)

    image = exif_transpose(image)

    size_avatar = (W, H)
    avatarNEWSize = image.resize(size_avatar)
    avatarNew = BytesIO()
    avatarNEWSize.save(avatarNew, format='PNG')
    avatarNew.seek(0)
    image.close
    return avatarNew