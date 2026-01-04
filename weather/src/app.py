import flet as ft
from api import get_area_data, get_weather


def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.window_width = 900
    page.window_height = 600

    weather_view = ft.Column(scroll=ft.ScrollMode.AUTO)

    # ===== 天気表示 =====
    def show_weather(area_code, area_name):
        weather_view.controls.clear()

        data = get_weather(area_code)
        ts = data[0]["timeSeries"][0]
        area_weather = ts["areas"][0]
        times = ts["timeDefines"]
        weathers = area_weather["weathers"]

        weather_view.controls.append(ft.Text(area_name, size=22, weight="bold"))

        for t, w in zip(times[:3], weathers[:3]):
            weather_view.controls.append(ft.Text(f"{t[:10]}：{w}"))

        page.update()

    # ===== 地域リスト =====
    area_json = get_area_data()
    centers = area_json["centers"]
    offices = area_json["offices"]
    center_codes = list(centers.keys())

    office_list = ft.Column(scroll=ft.ScrollMode.AUTO)

    def create_office_list(center_code):
        office_list.controls.clear()
        for office_code in centers[center_code]["children"]:
            name = offices[office_code]["name"]
            office_list.controls.append(
                ft.ListTile(
                    title=ft.Text(name),
                    on_click=lambda e, c=office_code, n=name: show_weather(c, n),
                )
            )
        page.update()

    def on_center_change(e):
        create_office_list(center_codes[e.control.selected_index])

    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        on_change=on_center_change,
    )

    for code in center_codes:
        nav_rail.destinations.append(
            ft.NavigationRailDestination(
                icon=ft.Icons.LOCATION_ON,
                label=centers[code]["name"],
            )
        )

    create_office_list(center_codes[0])

    page.add(
        ft.Row(
            [
                nav_rail,
                ft.VerticalDivider(width=1),
                ft.Container(width=250, content=office_list),
                ft.VerticalDivider(width=1),
                ft.Container(expand=True, padding=20, content=weather_view),
            ],
            expand=True,
        )
    )


ft.app(target=main)
