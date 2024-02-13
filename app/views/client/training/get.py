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


from flet_core import Column, Container, Row, ScrollMode, Text, MainAxisAlignment, alignment, AlertDialog, TextButton, \
    colors
from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.input import TextField
from app.controls.layout import ClientBaseView
from app.utils import Fonts, Error


class Exercise:
    name: str
    quantity: int
    is_time: bool

    def __init__(self, name: str, quantity: int, is_time: bool):
        self.name = name
        self.quantity = quantity
        self.is_time = is_time


class TrainingView(ClientBaseView):
    tf_comment: TextField
    dlg_modal: AlertDialog
    training: dict

    def __init__(self, exercise, training_id):
        super().__init__()
        self.exercise = exercise
        self.training_id = training_id

    async def build(self):
        if self.training_id:
            self.training = await self.client.session.api.client.trainings.get(
                id_=self.training_id,
            )
        controls = []
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
                                    key='seconds') + '.',
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

        main_section_controls = []
        if not self.exercise:
            main_section_controls.append(
                Text(
                    value=await self.client.session.gtv(key='training_planning_stage'),
                    size=15,
                    font_family=Fonts.MEDIUM,
                )
            )
        else:
            main_section_controls.extend([
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
                                expand=3,
                            ),
                            Container(
                                Text(
                                    value=await self.client.session.gtv(key='name'),
                                    font_family=Fonts.SEMIBOLD,
                                    color='#ffffff',
                                ),
                                expand=8,
                                alignment=alignment.center,
                            ),
                            Container(
                                Text(
                                    value=await self.client.session.gtv(key='quantity'),
                                    font_family=Fonts.SEMIBOLD,
                                    color='#ffffff',
                                ),
                                expand=4,
                                alignment=alignment.center_right,
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
            ])
        if self.training_id:
            if self.training['training_report_id'] is None:
                main_section_controls.append(
                    FilledButton(
                        content=Text(
                            value=await self.client.session.gtv(key='send_report'),
                        ),
                        on_click=self.open_dlg,
                    ),
                )
            else:
                main_section_controls.append(
                    Text(
                        value=await self.client.session.gtv(key='thanks_for_report'),
                        size=25,
                        font_family=Fonts.SEMIBOLD,
                        color=colors.ON_BACKGROUND,
                    ),
                )

        self.tf_comment = TextField(
            label=await self.client.session.gtv(key='comment')
        )
        self.dlg_modal = AlertDialog(
            content=Container(
                content=Column(
                    controls=[
                        Text(
                            value=await self.client.session.gtv(key='training_report_info'),
                            size=20,
                            font_family=Fonts.SEMIBOLD,
                        ),
                        self.tf_comment,
                    ],
                ),
                height=120,
            ),
            actions=[
                Row(
                    controls=[
                        TextButton(
                            content=Text(
                                value=await self.client.session.gtv(key='send'),
                                size=16,
                            ),
                            on_click=self.create_report
                        ),
                        TextButton(
                            content=Text(
                                value=await self.client.session.gtv(key='close'),
                                size=16,
                            ),
                            on_click=self.close_dlg,
                        ),
                    ],
                    alignment=MainAxisAlignment.END,
                ),
            ],
            modal=False,
        )

        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='training'),
            main_section_controls=main_section_controls + [
                self.dlg_modal,
            ],
        )

    async def close_dlg(self, _):
        self.dlg_modal.open = False
        await self.update_async()

    async def open_dlg(self, _):
        self.dlg_modal.open = True
        await self.update_async()

    async def create_report(self, _):
        await self.set_type(loading=True)
        fields = [(self.tf_comment, 1, 1024)]
        for field, min_len, max_len in fields:
            if not await Error.check_field(self, field, min_len=min_len, max_len=max_len):
                return
        try:
            await self.client.session.api.client.trainings.reports.create(
                training_id=self.training_id,
                comment=self.tf_comment.value,
            )
            await self.set_type(loading=False)
            await self.restart()
        except ApiException as e:
            await self.set_type(loading=False)
            return await self.client.session.error(error=e)
