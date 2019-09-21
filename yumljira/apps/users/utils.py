from io import BytesIO
import tempfile

from django.core.files.base import File
from PIL import Image


def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
    file_obj = tempfile.NamedTemporaryFile(suffix=f'.{ext}')
    image = Image.new("RGBA", size=size, color=color)
    image.save(file_obj)
    file_obj.seek(0)

    return File(file_obj, name=name)
