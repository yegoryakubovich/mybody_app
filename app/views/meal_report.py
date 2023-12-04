from typing import Any

from flet_core import ButtonStyle, Column, Container, FontWeight, Image, MaterialState, RoundedRectangleBorder, Row, \
    ScrollMode, Text, padding
from flet_manager.utils import get_svg

from app.controls.button import FilledButton
from app.controls.button.product_chip import ProductChipButton
from app.controls.input import TextField
from app.controls.layout import View


class Meal:
    name: str
    weight: str

    def __init__(self, name: str, weight: str):
        self.name = name
        self.weight = weight


class AddButton(FilledButton):
    def __init__(self, on_click: Any, **kwargs):
        super().__init__(**kwargs)
        self.content = Text(
            value='#+Add',
            size=14,
            color='#ffffff',
        )
        self.on_click = on_click
        self.style = ButtonStyle(
            padding={
                MaterialState.DEFAULT: padding.symmetric(horizontal=10, vertical=12),
            },
            shape={
                MaterialState.DEFAULT: RoundedRectangleBorder(radius=6),
            },
            overlay_color={
                MaterialState.DEFAULT: '#51B62E',
                MaterialState.HOVERED: '#51B62E',  # FIXME
            },
            shadow_color=None,
        )


class MealReportView(View):
    async def build(self):
        self.bgcolor = '#FFFFFF'  # FIXME
        self.scroll = ScrollMode.ALWAYS
        self.padding = 15

        products = ['Rise', 'Buckwheat', 'Oatmeal', 'Barley']  # FIXME

        meals = [
            Meal(
                name=f'#{product}',
                weight='120g',
            ) for product in products
        ]

        self.controls = [
            Container(
                Row(
                    controls=[
                        Container(
                            Image(
                                src=get_svg(
                                    path=f'assets/icons/back.svg',
                                ),
                                color='#000000',  # FIXME
                                height=20,
                            ),
                            on_click=lambda _: None  # FIXME
                        ),
                        Text(
                            value='#Meal_Report',  # FIXME
                            size=30,
                            weight=FontWeight.BOLD,
                            color='#000000',  # FIXME
                        ),
                    ],
                ),
                padding=padding.only(bottom=15)
            ),
            Container(
                Text(
                    value='#Report_Guide',  # FIXME
                    size=18,
                    color='#000000',
                ),
                padding=padding.only(bottom=15),
            ),
            Column(
                controls=[
                    Text(
                        value='#Products',
                        size=25,
                        weight=FontWeight.BOLD,
                        color='#000000',  # FIXME
                    ),
                    Row(
                        controls=[
                            ProductChipButton(f'{meal.name} {meal.weight}') for meal in meals
                        ],
                        wrap=True,
                    ),
                    AddButton(
                        on_click=lambda _: None,  # FIXME
                    ),
                ],
                spacing=10,
            ),
            Container(
                TextField(
                    label='#Notes',  # FIXME
                ),
                padding=padding.symmetric(vertical=15)
            ),
            Column(
                controls=[
                    Text(
                        value='#Photos',
                        size=25,
                        weight=FontWeight.BOLD,
                        color='#000000',  # FIXME
                    ),
                    Text(
                        value='#Add_photos',  # FIXME
                        size=18,
                        color='#000000',
                    ),
                    AddButton(
                        on_click=lambda _: None,  # FIXME
                    ),
                    FilledButton(
                        content=Text(
                            value='#Make_a_Report',
                            size=14,
                            color='#ffffff',
                        ),
                    ),
                ],
                spacing=10,
            ),
        ]
