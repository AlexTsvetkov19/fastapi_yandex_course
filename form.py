# form.py
from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()


@app.post("/login")
def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    some_file: Annotated[UploadFile, File()]
):
    file_content = some_file.file.read().splitlines()
    return {
        'username': username,
        'file_content': file_content
    }