from fastapi import FastAPI, File, UploadFile
from moviepy.editor import *
import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")

app = FastAPI()


@app.post("/convert/", description="Конвертация видео в gif", tags=["Конвертация"])
async def convert_gif(file: UploadFile):
    file_bytes = await file.read()
    f = open(path, 'wb')
    f.write(file_bytes)
    f.close()
    return {"filename": file.filename}
