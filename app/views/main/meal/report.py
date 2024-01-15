from typing import Any

from flet_core import (ButtonStyle, Column, Container, Image, MaterialState, RoundedRectangleBorder, Row, ScrollMode,
                       Text, TextStyle, padding, colors)
from flet_manager.utils import get_svg

from app.controls.button import FilledButton
from app.controls.button.product_chip import ProductChipButton
from app.controls.input import TextField
from app.controls.layout import View
from app.utils import Fonts


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
            value='Add',  # FIXME await self.client.session.gtv(key='+Add')
            size=14,
            color='#ffffff',  # FIXME
            font_family=Fonts.REGULAR,
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
                MaterialState.DEFAULT: '#51B62E',  # FIXME
                MaterialState.HOVERED: '#51B62E',  # FIXME
            },
            shadow_color=None,
        )


class MealReportView(View):
    async def go_back(self, _):
        await self.client.change_view(go_back=True)

    async def build(self):
        self.scroll = ScrollMode.ALWAYS

        products = ['Rise', 'Buckwheat', 'Oatmeal', 'Barley']  # FIXME

        meals = [
            Meal(
                name=await self.client.session.gtv(key=f'{product}'),
                weight='120',
            ) for product in products
        ]

        self.controls = self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        Container(
                            Row(
                                controls=[
                                    Container(
                                        Image(
                                            src=get_svg(
                                                path=f'assets/icons/arrow_back.svg',
                                            ),
                                            color=colors.TERTIARY,
                                            height=20,
                                        ),
                                        on_click=self.go_back,
                                    ),
                                    Text(
                                        value=await self.client.session.gtv(key='Meal_Report'),  # FIXME
                                        size=30,
                                        font_family=Fonts.BOLD,
                                        color='#000000',  # FIXME
                                    ),
                                ],
                            ),
                            padding=padding.only(bottom=15)
                        ),
                        Container(
                            Text(
                                value=await self.client.session.gtv(key='Report_Guide'),  # FIXME
                                size=18,
                                color='#000000',  # FIXME
                                font_family=Fonts.REGULAR,
                            ),
                            padding=padding.only(bottom=15),
                        ),
                        Column(
                            controls=[
                                Text(
                                    value=await self.client.session.gtv(key='Products'),
                                    size=25,
                                    font_family=Fonts.BOLD,
                                    color='#000000',  # FIXME
                                ),
                                Row(
                                    controls=[
                                        ProductChipButton(
                                            text=f"{meal.name} {meal.weight}{await self.client.session.gtv(key='g')}",
                                            on_click=None,
                                        )
                                        for meal in meals
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
                                label=await self.client.session.gtv(key='Notes'),  # FIXME
                                text_style=TextStyle(
                                    font_family=Fonts.MEDIUM,
                                    color='#000000',  # FIXME
                                ),
                                label_style=TextStyle(
                                    font_family=Fonts.BOLD,
                                    color='#868686',  # FIXME
                                ),
                                cursor_color='#868686',  # FIXME
                                border_width=1.5,
                                border_color='#868686',  # FIXME
                                multiline=True,
                            ),
                            padding=padding.symmetric(vertical=15)
                        ),
                        Column(
                            controls=[
                                Text(
                                    value=await self.client.session.gtv(key='Photos'),
                                    size=25,
                                    font_family=Fonts.BOLD,
                                    color='#000000',  # FIXME
                                ),
                                Text(
                                    value=await self.client.session.gtv(key='Add_photos'),  # FIXME
                                    size=18,
                                    color='#000000',  # FIXME
                                    font_family=Fonts.REGULAR,
                                ),
                                AddButton(
                                    on_click=lambda _: None,  # FIXME
                                ),
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='Send_a_Report'),
                                        size=14,
                                        color='#ffffff',  # FIXME
                                        font_family=Fonts.REGULAR,
                                    ),
                                    on_click=lambda _: None,
                                ),
                            ],
                            spacing=10,
                        ),
                    ],
                    spacing=0,
                ),
                padding=15,
            ),
        ]
