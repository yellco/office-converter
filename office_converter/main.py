from fastapi import FastAPI, Query
from moviepy.editor import VideoFileClip
import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")

app = FastAPI()


def output_path(input_path):
    input_lambda = lambda splitter: input_path.split(splitter)[-1].split(".")[0]
    if "\\" in input_path:
        file_input = input_lambda("\\")
    elif "/" in input_path:
        file_input = input_lambda("/")
    else:
        file_input = "result"

    return os.path.join(os.path.dirname(input_path), f"{file_input}.gif")


@app.get("/convert/", description="Конвертация видео в gif", tags=["Конвертация"])
async def convert_gif(
        input_path_to_video: str = Query(..., description="Путь для исходного видео файла"),
        output_gif_path: str = Query(None, description="Путь для сохранения gif файла")
):
    if not output_gif_path:
        output_gif_path = output_path(input_path_to_video)
    try:
        video_clip = VideoFileClip(input_path_to_video)
    except OSError as e:
        return {"result": "fail", "detail": e}
    video_clip.write_gif(output_gif_path)
    return {"result": "success"}
