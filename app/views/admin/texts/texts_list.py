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

from flet_core import Container, Column, Row, MainAxisAlignment, Card, ScrollMode

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import View
from app.utils import Fonts
from app.views.admin.texts.create_text import CreateTextView
from app.views.admin.texts.get_text import TextGetView


class TextView(View):
    route = '/admin'

    def __init__(self, texts):
        super().__init__()
        self.texts = texts
        self.text_data = None

    async def build(self):
        self.scroll = ScrollMode.AUTO
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                         Row(
                             controls=[
                                 Text(
                                     value=await self.client.session.gtv(key='Texts'),
                                     font_family=Fonts.BOLD,
                                     size=30,
                                 ),
                                 FilledButton(
                                     content=Text(
                                         value=await self.client.session.gtv(key='Create'),
                                     ),
                                     on_click=self.create_text,
                                 ),
                             ],
                             alignment=MainAxisAlignment.SPACE_BETWEEN,
                         ),
                     ] + [
                         Card(
                             content=Container(
                                 content=Column(
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
                                         Row(),
                                     ],
                                 ),
                                 ink=True,
                                 padding=10,
                                 on_click=self.text_view,
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

    async def text_view(self, _):
        await self.client.change_view(view=TextGetView())
