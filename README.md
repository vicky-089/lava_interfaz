import flet as ft
import asyncio

def main(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = ft.colors.LIGHT_BLUE_50
    page.window_maximized = True
    page.window_resizable = False

    timer_running = False
    paused = False
    remaining_seconds = 0
    timer_task = None

    async def update_timer():
        nonlocal remaining_seconds
        while remaining_seconds > 0 and not paused:
            minutes_left = remaining_seconds // 60
            seconds_left = remaining_seconds % 60
            timer_text.value = (
                f"Tiempo restante: {minutes_left} minutos {seconds_left} segundos"
            )
            await timer_text.update_async()
            await asyncio.sleep(1)
            remaining_seconds -= 1
        if remaining_seconds == 0:
            timer_text.value = "Ciclo completado"
            await timer_text.update_async()

    async def start_cycle(e):
        nonlocal timer_running, remaining_seconds, timer_task, paused
        if not timer_running or paused:
            notification_text.value = "Iniciando ciclo"
            await notification_text.update_async()
            try:
                minutes = int(timer_dropdown.value)
                if not paused:
                    remaining_seconds = minutes * 60
                timer_running = True
                paused = False
                timer_task = asyncio.create_task(update_timer())
            except ValueError:
                timer_text.value = "Por favor, seleccione un tiempo válido."
                await timer_text.update_async()
        else:
            paused = False
            timer_task = asyncio.create_task(update_timer())

    async def pause_cycle(e):
        nonlocal paused
        if timer_running:
            paused = True

    async def reset_cycle(e):
        nonlocal timer_running, paused, remaining_seconds, timer_task
        if timer_running:
            timer_task.cancel()
            timer_running = False
            paused = False
            remaining_seconds = 0
            timer_text.value = "Tiempo restante: 0 minutos 0 segundos"
            notification_text.value = "Ciclo reiniciado"
            await timer_text.update_async()
            await notification_text.update_async()

    def dropdown_change(e):
        timer_text.value = f"Tiempo restante: {timer_dropdown.value} minutos 0 segundos"
        page.update()

    c1 = ft.ElevatedButton(
        text="ON/Encendido",
        bgcolor=ft.colors.GREEN_200,
        on_hover=ft.colors.GREEN_300,
        color=ft.colors.BLACK,
        width=300,
        height=80,
        on_click=start_cycle,
        icon=ft.icons.POWER_SETTINGS_NEW,
    )
    c2 = ft.ElevatedButton(
        text="OFF/Apagado",
        bgcolor=ft.colors.RED_200,
        on_hover=ft.colors.RED_300,
        color=ft.colors.BLACK,
        width=300,
        height=80,
        on_click=pause_cycle,
        icon=ft.icons.POWER_SETTINGS_NEW,
    )

    reset_button = ft.ElevatedButton(
        text="Reset/Reiniciar",
        color=ft.colors.BLACK,
        bgcolor=ft.colors.YELLOW_200,
        on_hover=ft.colors.YELLOW_300,
        width=300,
        height=80,
        icon=ft.icons.RESTART_ALT,
        on_click=reset_cycle,
    )

    timer_text = ft.Text(
        value="Tiempo restante: ", size=20, weight="bold", color=ft.colors.BLACK
    )
    timer_dropdown = ft.Dropdown(
        label="Seleccione el tiempo (minutos)",
        options=[
            ft.dropdown.Option(key="5", text="5"),
            ft.dropdown.Option(key="10", text="10"),
            ft.dropdown.Option(key="15", text="15"),
            ft.dropdown.Option(key="20", text="20"),
            ft.dropdown.Option(key="30", text="30"),
            ft.dropdown.Option(key="45", text="45"),
            ft.dropdown.Option(key="60", text="60"),
        ],
        width=200,
        value="10",
        on_change=dropdown_change,
    )
    notification_text = ft.Text(value="", size=20, weight="bold", color=ft.colors.BLACK)

    button_prelavado = ft.ElevatedButton(
        text="Prelavado",
        color=ft.colors.BLACK,
        bgcolor=ft.colors.LIGHT_BLUE_100,
        on_hover=ft.colors.LIGHT_BLUE_200,
        width=300,
        height=80,
        icon=ft.icons.CLEAN_HANDS,
        on_click=lambda e: asyncio.create_task(start_cycle(e)),
    )

    button_lavado = ft.ElevatedButton(
        text="Lavado",
        color=ft.colors.BLACK,
        bgcolor=ft.colors.LIGHT_BLUE_100,
        on_hover=ft.colors.LIGHT_BLUE_200,
        width=300,
        height=80,
        icon=ft.icons.WATER,
        on_click=lambda e: asyncio.create_task(start_cycle(e)),
    )

    button_enjuague = ft.ElevatedButton(
        text="Enjuague",
        color=ft.colors.BLACK,
        bgcolor=ft.colors.LIGHT_BLUE_100,
        on_hover=ft.colors.LIGHT_BLUE_200,
        width=300,
        height=80,
        icon=ft.icons.INVERT_COLORS,
        on_click=lambda e: asyncio.create_task(start_cycle(e)),
    )

    button_centrifugado = ft.ElevatedButton(
        text="Centrifugado",
        color=ft.colors.BLACK,
        bgcolor=ft.colors.LIGHT_BLUE_100,
        on_hover=ft.colors.LIGHT_BLUE_200,
        width=300,
        height=80,
        icon=ft.icons.AUTORENEW,
        on_click=lambda e: asyncio.create_task(start_cycle(e)),
    )

    lavarropas = ft.Column(
        [
            ft.Container(
                bgcolor=ft.colors.LIGHT_BLUE_50,
                width=page.adaptive,
                height=page.adaptive,
                border_radius=30,
                padding=20,
                content=ft.Column(
                    [
                        ft.Text(
                            value="Bienvenido a tu Lavarropas",
                            weight="bold",
                            size=30,
                            color=ft.colors.BLACK,
                        ),
                        ft.Container(
                            padding=ft.padding.only(top=20),
                            content=ft.Row(
                                [c1, c2, reset_button], alignment="center", spacing=10
                            ),
                        ),
                        ft.Container(
                            padding=ft.padding.only(top=20),
                            content=ft.Column(
                                [
                                    timer_dropdown,
                                    timer_text,
                                ],
                                spacing=10,
                                horizontal_alignment="center",
                                alignment="center",
                            ),
                        ),
                        ft.Container(
                            padding=ft.padding.only(top=20),
                            content=notification_text,
                        ),
                        ft.Container(
                            padding=ft.padding.only(top=20),
                            content=ft.Row(
                                [
                                    button_prelavado,
                                    button_enjuague,
                                ],
                                alignment="center",
                                spacing=30,
                            ),
                        ),
                        ft.Container(
                            padding=ft.padding.only(top=20),
                            content=ft.Row(
                                [
                                    button_lavado,
                                    button_centrifugado,
                                ],
                                alignment="center",
                                spacing=30,
                            ),
                        ),
                    ],
                    spacing=20,
                    horizontal_alignment="center",
                    alignment="center",
                ),
            ),
        ]
    )

    page.add(lavarropas)


if __name__ == "__main__":
    ft.app(target=main)
