from fastapi import FastAPI
import flet as ft
from lava_interfaz import main

app = FastAPI()


@app.get("/")
async def read_root():
    def page_callback(page: ft.Page):
        main(page)

    ft.app(target=page_callback, view=ft.WEB_BROWSER)

    return {"message": "Flet app is running"}
