#
# (c) 2024, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
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


from flet_core import Column, Container, CrossAxisAlignment, Image, Row, ScrollMode, Text, margin, padding
from flet_manager.utils import get_svg

from app.controls.button import FilledButton
from app.controls.layout import View
from app.utils import Fonts


class Exercise:
    name: str
    quantity: int
    is_time: bool

    def __init__(self, name: str, quantity: int, is_time: bool):
        self.name = name
        self.quantity = quantity
        self.is_time = is_time


class TrainingView(View):
    async def go_back(self, _):
        await self.client.change_view(go_back=True)

    async def build(self):
        self.bgcolor = '#FFFFFF'  # FIXME
        self.scroll = ScrollMode.ALWAYS

        exercises = [  # FIXME
                        Exercise(name=await self.client.session.gtv(key='Exercise_Quantity'), quantity=30,
                                 is_time=False)
                        for _ in range(5)
                    ] + [
                        Exercise(name=await self.client.session.gtv(key='Exercise_Time'), quantity=60,
                                 is_time=True)
                        for _ in range(5)
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
                                        on_click=self.go_back,
                                    ),
                                    Text(
                                        value=await self.client.session.gtv(key='Training'),  # FIXME
                                        size=30,
                                        font_family=Fonts.BOLD,
                                        color='#000000',  # FIXME
                                    ),
                                ]
                            ),
                            padding=padding.only(bottom=15),
                        ),
                        Container(
                            Text(
                                value=await self.client.session.gtv(key='Your_Plan_for_Today'),  # FIXME
                                size=18,
                                color='#000000',
                                font_family=Fonts.REGULAR,
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
                                                            font_family=Fonts.SEMIBOLD,
                                                            color='#ffffff',
                                                        ),
                                                    ],
                                                    expand=True,
                                                    horizontal_alignment=CrossAxisAlignment.START,
                                                ),
                                                Column(
                                                    [
                                                        Text(
                                                            value=await self.client.session.gtv(key='Name'),
                                                            font_family=Fonts.SEMIBOLD,
                                                            color='#ffffff',
                                                        ),
                                                    ],
                                                    expand=True,
                                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                                ),
                                                Column(
                                                    [
                                                        Text(
                                                            value=await self.client.session.gtv(key='Quantity'),
                                                            font_family=Fonts.SEMIBOLD,
                                                            color='#ffffff',
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
                                                                    font_family=Fonts.MEDIUM,
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
                                                                    font_family=Fonts.MEDIUM,
                                                                ),
                                                            ],
                                                            expand=True,
                                                            horizontal_alignment=CrossAxisAlignment.CENTER,
                                                        ),
                                                        Column(
                                                            [
                                                                Text(
                                                                    value=f'{exercises[i].quantity} {await self.client.session.gtv(key="""sec""")}' if
                                                                    exercises[i].is_time else str(
                                                                        exercises[i].quantity),
                                                                    color='#000000',
                                                                    font_family=Fonts.MEDIUM,
                                                                ),
                                                            ],
                                                            width=60,
                                                            horizontal_alignment=CrossAxisAlignment.CENTER,
                                                        ),
                                                    ],
                                                ) for i in range(len(exercises))
                                            ],
                                            spacing=5,
                                        ),
                                        padding=10,
                                        bgcolor='#D9D9D9',
                                    )
                                ],
                                spacing=0,
                            ),
                            border_radius=15,
                            margin=margin.only(bottom=15),
                        ),
                        Container(
                            FilledButton(
                                content=Text(
                                    value=await self.client.session.gtv(key='Start'),
                                    size=14,
                                    color='#ffffff',
                                    font_family=Fonts.REGULAR,
                                ),
                            ),
                        ),
                    ],
                    spacing=0,
                ),
                padding=15
            ),
        ]
