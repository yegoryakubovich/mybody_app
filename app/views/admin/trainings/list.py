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


import functools

from flet_core import Container, Column, Row, Card, ScrollMode

from app.controls.information import Text
from app.controls.layout import View
from app.utils import Fonts
from app.views.admin.texts.create import CreateTextView
from app.views.admin.texts.get import TextView


class TrainingListView(View):
    route = '/admin'
    trainings: list[dict]

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.training.get_list()
        self.trainings = response.trainings
        await self.set_type(loading=False)

        self.scroll = ScrollMode.AUTO
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                            title=await self.client.session.gtv(key='trainings'),
                            on_create_click=self.create_training,
                        ),
                    ] + [
                        Card(
                            content=Container(
                                content=Column(
                                    controls=[
                                        Text(
                                            value=training['key'].upper(),
                                            size=18,
                                            font_family=Fonts.SEMIBOLD,
                                        ),
                                        Text(
                                            value=text['value_default'],
                                            size=10,
                                            font_family=Fonts.MEDIUM,
                                        ),
                                        Row(),
                                    ],
                                ),
                                ink=True,
                                padding=10,
                                on_click=functools.partial(self.text_view, text['id']),
                            ),
                            margin=0,
                        )
                        for text in self.texts
                    ],
                ),
                padding=10,
            ),
        ]

    async def create_text(self, _):
        await self.client.change_view(view=CreateTextView())

    async def text_view(self, text_id, _):
        await self.client.change_view(view=TextView(text_id=text_id))
