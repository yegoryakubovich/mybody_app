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

from flet_core import Container, Column, ScrollMode

from app.controls.information import Text
from app.controls.information.card import Card
from app.controls.layout import AdminView
from app.utils import Fonts
from .create import CreateTextView
from .get import TextView


class TextListView(AdminView):
    route = '/admin'
    texts: list[dict]

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.text.get_list()
        self.texts = response.texts
        await self.set_type(loading=False)

        self.scroll = ScrollMode.AUTO
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=await self.get_controls(
                        title=await self.client.session.gtv(key='admin_text_get_list_view_title'),
                        on_create_click=self.create_text,
                        main_section_controls=[
                            Card(
                                controls=[
                                    Text(
                                        value=text['key'].upper(),
                                        size=18,
                                        font_family=Fonts.SEMIBOLD,
                                    ),
                                    Text(
                                        value=text['value_default'],
                                        size=10,
                                        font_family=Fonts.MEDIUM,
                                    ),
                                ],
                                on_click=functools.partial(self.text_view, text['key']),
                            )
                            for text in self.texts
                        ],
                    ),
                ),
                padding=10,
            ),
        ]

    async def create_text(self, _):
        await self.client.change_view(view=CreateTextView())

    async def text_view(self, key, _):
        await self.client.change_view(view=TextView(key=key))
