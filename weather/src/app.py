import flet as ft
from api import get_area_data, get_weather
from db import init_db, insert_weather, get_weather_from_db

def main(page: ft.Page):
    init_db()
    page.title = "天気予報DBアプリ"

    weather_view = ft.Column()

    def show_weather(area_code, area_name):
        data = get_weather(area_code)
        ts = data[0]["timeSeries"][0]
        area_weather = ts["areas"][0]
        times = ts["timeDefines"]
        weathers = area_weather["weathers"]

        # DBに保存
        for t, w in zip(times[:3], weathers[:3]):
            insert_weather(area_code, area_name, t[:10], w)

        # DBから取得
        records = get_weather_from_db(area_code)

        weather_view.controls.clear()
        weather_view.controls.append(ft.Text(area_name, size=20, weight="bold"))
        for d, w in records:
            weather_view.controls.append(ft.Text(f"{d}：{w}"))
        page.update()

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

    nav = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        on_change=on_center_change,
    )

    for c in center_codes:
        nav.destinations.append(
            ft.NavigationRailDestination(
                icon=ft.Icons.LOCATION_ON,
                label=centers[c]["name"]
            )
        )

    create_office_list(center_codes[0])

    page.add(
        ft.Row([
            nav,
            ft.Container(width=250, content=office_list),
            ft.Container(expand=True, padding=20, content=weather_view)
        ], expand=True)
    )

ft.app(target=main)
