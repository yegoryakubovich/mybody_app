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


from flet_core import Column, Container, Row, ScrollMode, Text, MainAxisAlignment, alignment

from app.controls.button import FilledButton
from app.controls.layout import ClientBaseView
from app.utils import Fonts


class Exercise:
    name: str
    quantity: int
    is_time: bool

    def __init__(self, name: str, quantity: int, is_time: bool):
        self.name = name
        self.quantity = quantity
        self.is_time = is_time


class TrainingView(ClientBaseView):

    def __init__(self, exercise):
        super().__init__()
        self.exercise = exercise

    async def build(self):
        self.scroll = ScrollMode.AUTO
        controls = []
        if not self.exercise:
            controls.append(
                Text(
                    value=await self.client.session.gtv(key='training_planning_stage'),
                    size=15,
                    font_family=Fonts.MEDIUM,
                )
            )
        else:
            counter = 1
            for exercise in self.exercise:
                controls.append(
                    Row(
                        controls=[
                            Container(
                                Text(
                                    value=str(counter) + '.',
                                    color='#000000',
                                    font_family=Fonts.MEDIUM,
                                ),
                                expand=1,
                            ),
                            Container(
                                Text(
                                    value=await self.client.session.gtv(key=exercise['name_text']),
                                    color='#000000',
                                    font_family=Fonts.MEDIUM,
                                ),
                                expand=10,
                                alignment=alignment.center,
                            ),
                            Container(
                                Text(
                                    value=str(exercise['training_exercise']['value']),
                                    color='#000000',
                                    font_family=Fonts.MEDIUM,
                                ),
                                expand=2,
                                alignment=alignment.center,
                            ),
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                    )
                )
                counter += 1
                controls.append(
                    Row(
                        controls=[
                            Container(
                                Text(
                                    value=str(counter) + '.',
                                    color='#000000',
                                    font_family=Fonts.MEDIUM,
                                ),
                                expand=1,
                            ),
                            Container(
                                Text(
                                    value=await self.client.session.gtv(key='rest'),
                                    color='#000000',
                                    font_family=Fonts.MEDIUM,
                                ),
                                expand=10,
                                alignment=alignment.center,
                            ),
                            Container(
                                Text(
                                    value=str(
                                        exercise['training_exercise']['rest']) + ' ' + await self.client.session.gtv(
                                        key='seconds' + '.'
                                    ),
                                    color='#000000',
                                    font_family=Fonts.MEDIUM,
                                ),
                                expand=2,
                                alignment=alignment.center,
                            ),
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                    )
                )
                counter += 1

            controls.extend([
                Text(
                    value=await self.client.session.gtv(key='training_plan_today'),
                    size=18,
                    font_family=Fonts.REGULAR,
                ),
                Container(
                    Row(
                        controls=[
                            Container(
                                content=Text(
                                    value='№',
                                    font_family=Fonts.SEMIBOLD,
                                    color='#ffffff',
                                ),
                            ),
                            Container(
                                Text(
                                    value=await self.client.session.gtv(key='name'),
                                    font_family=Fonts.SEMIBOLD,
                                    color='#ffffff',
                                ),
                            ),
                            Container(
                                Text(
                                    value=await self.client.session.gtv(key='quantity'),
                                    font_family=Fonts.SEMIBOLD,
                                    color='#ffffff',
                                ),
                            ),
                        ],
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    bgcolor='#008F12',
                    padding=10,
                    border_radius=6
                ),
                Container(
                    Column(
                        controls=controls,
                        spacing=1,
                    ),
                    padding=10,
                    bgcolor='#D9D9D9',
                    border_radius=6
                ),
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='start'),
                    ),
                    on_click=self.start_training
                ),
            ])

        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='training'),
            main_section_controls=controls,
        )

    async def start_training(self, _):
        pass
