import cv2
from django.http import HttpResponse
import imageio
import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from .models import TextRequest

WIDTH, HEIGHT = 100, 100
FPS = 24
DURATION = 3
FRAME_COUNT = int(FPS * DURATION)
BACKGROUND_COLOR = (0, 128, 255)
FONT_SIZE = 20
TEXT_COLOR = (255, 255, 255)
FONT_PATH = 'Arial.ttf'
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)


def create_video(text):
    video_stream = io.BytesIO()

    ready_images = []

    img_pil_blank = Image.new('RGB', (WIDTH, HEIGHT))
    draw_sample = ImageDraw.Draw(img_pil_blank)
    text_bbox = draw_sample.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    y = (HEIGHT - text_height) // 2

    for i in range(FRAME_COUNT):
        frame = np.full((HEIGHT, WIDTH, 3), BACKGROUND_COLOR, dtype=np.uint8)

        img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)

        x = WIDTH - (i * (WIDTH + text_width) // FRAME_COUNT)

        draw.text((x, y), text, font=font, fill=TEXT_COLOR)

        frame = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        ready_images.append(frame)

    kargs = {'macro_block_size': None}
    imageio.mimwrite(video_stream, ready_images, fps=FPS, format='mp4', codec='libx264', **kargs)

    response = HttpResponse(content_type='video/mp4')
    response.write(video_stream.getvalue())
    response['Content-Disposition'] = 'attachment; filename="output.mp4"'

    return response


def video_view(request):
    text = request.GET.get('text', 'Бегущая строка')
    TextRequest.objects.create(text=text)
    return create_video(text)
