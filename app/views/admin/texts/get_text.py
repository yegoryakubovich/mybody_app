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


from flet_core import Container, Row, MainAxisAlignment, Card, Column, ScrollMode

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import View
from app.utils import Fonts
from app.views.admin.texts.create_translation import CreateTranslationView


class TextGetView(View):
    route = '/admin'
    tf_key = TextField
    tf_value_default = TextField

    async def on_load(self):
        self.text_list = await self.client.session.api.text.get_list().texts

    async def build(self):
        self.text_list = await self.client.session.api.text.get_list().texts
        self.tf_key = TextField(
            label=await self.client.session.gtv(key='key'),
            value=await self.client.session.gtv(key=self.texts['key'])
        )
        self.tf_value_default = TextField(
            label=await self.client.session.gtv(key='value_default'),
            value=await self.client.session.gtv(key=self.texts['value_default'])
        )
        self.scroll = ScrollMode.AUTO
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                                 Row(
                                     controls=[
                                         Text(
                                             value=await self.client.session.gtv(key=self.texts['key']),
                                             font_family=Fonts.BOLD,
                                             size=30,
                                         ),
                                     ],
                                     alignment=MainAxisAlignment.SPACE_BETWEEN,
                                 ),
                                 Column(
                                     controls=[
                                         self.tf_key,
                                         self.tf_value_default,
                                         Row(
                                             controls=[
                                                 FilledButton(
                                                     content=Text(
                                                         value=await self.client.session.gtv(key='save'),
                                                     ),
                                                     on_click=self.update_text,
                                                 ),
                                                 FilledButton(
                                                     content=Text(
                                                         value=await self.client.session.gtv(key='delete'),
                                                     ),
                                                     on_click=self.delete_text,
                                                 ),
                                             ],

                                         ),
                                         Row(
                                             controls=[
                                                 Text(
                                                     value=await self.client.session.gtv(key='Translation'),
                                                     size=30,
                                                     font_family=Fonts.BOLD,
                                                 ),
                                                 FilledButton(
                                                     content=Text(
                                                         value=await self.client.session.gtv(key='create_translation'),
                                                     ),
                                                     on_click=self.create_translation,
                                                 ),
                                             ],
                                             alignment=MainAxisAlignment.SPACE_BETWEEN,
                                         ),
                                     ],
                                 ),
                             ] + [
                                 Card(
                                     content=Container(
                                         content=Column(
                                             controls=[
                                                 Text(
                                                     value=translate['language'],
                                                     size=15,
                                                     font_family=Fonts.REGULAR,
                                                 ),
                                                 Text(
                                                     value=translate['value'],
                                                     size=10,
                                                     font_family=Fonts.MEDIUM,
                                                 ),
                                                 Row(),
                                             ],
                                         ),
                                         ink=True,
                                         padding=10,
                                     ),
                                     margin=0,
                                 )
                                 for translate in self.texts.get('translates', [])
                             ],
                ),
                padding=10,
            ),
        ]

    async def create_translation(self, _):
        await self.client.change_view(view=CreateTranslationView(texts=self.texts))

    async def delete_translation(self, _):
        print(self.texts)
        response = await self.client.session.api.text.delete_translation(
            text_key=self.texts['key'],
        )
        print(response)
        await self.update_async()

    async def update_translation(self, text, _):
        pass

    async def delete_text(self, _):
        await self.client.session.api.text.delete(
            key=self.texts['key'],
        )
        await self.client.change_view(view=True)

    async def update_text(self, _):
        await self.client.session.api.text.update(
            key=self.texts['key'],
            value_default=self.tf_value_default.value,
            new_key=self.tf_key.value
        )
