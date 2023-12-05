#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from typing import Any

from flet_core import Column, Container, CrossAxisAlignment, FontWeight, Image, Row, ScrollMode, Text, alignment, \
    margin, padding
from flet_manager.utils import get_svg

from app.controls.button import FilledButton
from app.controls.button.product_chip import ProductChipButton
from app.controls.layout import View


class Exercise:
    name: str
    quantity: int
    is_time: bool

    def __init__(self, name: str, quantity: int, is_time: bool):
        self.name = name
        self.quantity = quantity
        self.is_time = is_time


class TrainingView(View):
    async def build(self):
        self.bgcolor = '#FFFFFF'  # FIXME
        self.scroll = ScrollMode.ALWAYS

        exercises = [  # FIXME
            Exercise(name='#Exercise_Quantity', quantity=30, is_time=False) for i in range(5)
        ] + [
            Exercise(name='#Exercise_Time', quantity=60, is_time=True) for i in range(5)
        ]
        self.controls = [
            await self.get_header(),
            Container(
                Column(
                    controls=[
                        Container(
                            Row(
                                controls=[
                                    Container(
                                        Image(
                                            src=get_svg(
                                                path=f'assets/icons/arrow_back.svg',
                                            ),
                                            color='#000000',  # FIXME
                                            height=20,
                                        ),
                                        on_click=lambda _: None  # FIXME
                                    ),
                                    Text(
                                        value='#Training',  # FIXME
                                        size=30,
                                        weight=FontWeight.BOLD,
                                        color='#000000'  # FIXME
                                    ),
                                ]
                            ),
                            padding=padding.only(bottom=15)
                        ),
                        Container(
                            Text(
                                value='#Your_Plan_for_Today',  # FIXME
                                size=18,
                                color='#000000',
                            ),
                            padding=padding.only(bottom=15)
                        ),
                        Container(
                            content=Column(
                                controls=[
                                    Container(
                                        Row(
                                            controls=[
                                                Column(
                                                    [
                                                        Text(
                                                            value='№',
                                                            weight=FontWeight.BOLD,
                                                        ),
                                                    ],
                                                    expand=True,
                                                    horizontal_alignment=CrossAxisAlignment.START,
                                                ),
                                                Column(
                                                    [
                                                        Text(
                                                            value='#Name',
                                                            weight=FontWeight.BOLD,
                                                        ),
                                                    ],
                                                    expand=True,
                                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                                ),
                                                Column(
                                                    [
                                                        Text(
                                                            value='#Quantity',
                                                            weight=FontWeight.BOLD,
                                                        ),
                                                    ],
                                                    expand=True,
                                                    horizontal_alignment=CrossAxisAlignment.END,
                                                ),
                                            ],
                                        ),
                                        bgcolor='#008F12',
                                        padding=10,
                                    ),
                                    Container(
                                        Column(
                                            controls=[
                                                Row(
                                                    controls=[
                                                        Column(
                                                            [
                                                                Text(
                                                                    value=str(i),
                                                                    color='#000000',
                                                                    weight=FontWeight.BOLD,
                                                                ),
                                                            ],
                                                            width=60,
                                                            horizontal_alignment=CrossAxisAlignment.START,
                                                        ),
                                                        Column(
                                                            [
                                                                Text(
                                                                    value=exercises[i].name,
                                                                    color='#000000',
                                                                    weight=FontWeight.BOLD,
                                                                ),
                                                            ],
                                                            expand=True,
                                                            horizontal_alignment=CrossAxisAlignment.CENTER,
                                                        ),
                                                        Column(
                                                            [
                                                                Text(
                                                                    value=f'{exercises[i].quantity} #sec' if exercises[
                                                                        i].is_time else str(exercises[i].quantity),
                                                                    color='#000000',
                                                                    weight=FontWeight.BOLD,
                                                                ),
                                                            ],
                                                            width=60,
                                                            horizontal_alignment=CrossAxisAlignment.CENTER,
                                                        ),
                                                    ],
                                                ) for i in range(len(exercises))
                                            ],
                                            spacing=5
                                        ),
                                        padding=10,
                                        bgcolor='#D9D9D9',
                                    )
                                ],
                                spacing=0
                            ),
                            border_radius=15,
                            margin=margin.only(bottom=15),
                        ),
                        Container(
                            FilledButton(
                                content=Text(
                                    value='#Start',
                                    size=14,
                                    color='#ffffff',
                                ),
                            ),
                        )
                    ],
                    spacing=0,
                ),
                padding=15
            )
        ]
