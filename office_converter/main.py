from fastapi import FastAPI, Query, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from moviepy.editor import VideoFileClip
import os
import aiofiles


path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")

app = FastAPI()

base_path = "./office_converter/tmp"

if not os.path.exists(base_path):
    os.mkdir(base_path)


def output_path(input_path):
    input_lambda = lambda splitter: input_path.split(splitter)[-1].split(".")[0]
    if "\\" in input_path:
        file_input = input_lambda("\\")
    elif "/" in input_path:
        file_input = input_lambda("/")
    else:
        file_input = "result"

    return os.path.join(os.path.dirname(input_path), f"{file_input}.gif")


def delete_files(*files):
    for file_path in files:
        os.remove(file_path)


@app.post("/convert", description="Конвертация видео в gif", tags=["Конвертация"])
async def convert_gif(
    video_file: UploadFile, background_tasks: BackgroundTasks
):
    path_to_filename = f"{base_path}/{video_file.filename}"
    result_filename = f"{video_file.filename.split('.')[0]}.gif"
    result_path = f"{base_path}/{result_filename}"
    async with aiofiles.open(path_to_filename, 'wb') as out_file:
        content = await video_file.read()
        await out_file.write(content)

    try:
        video_clip = VideoFileClip(path_to_filename)
    except OSError as e:
        return {"result": "fail", "detail": e}
    video_clip.write_gif(result_path)

    background_tasks.add_task(delete_files, path_to_filename, result_path)
    return FileResponse(result_path, filename=result_filename)
