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

from flet_core import Container, Row, MainAxisAlignment, Card, Column, ScrollMode

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import View
from app.utils import Fonts
from app.views.admin.texts.create_translation import CreateTranslationView
from app.views.admin.texts.get_translation import TranslationView


class TextView(View):
    route = '/admin'
    tf_key = TextField
    tf_value_default = TextField
    text = dict

    def __init__(self, text_id):
        super().__init__()
        self.text_id = text_id

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.text.get(
            id_=self.text_id
        )
        self.text = response.text
        await self.set_type(loading=False)

        self.tf_key = TextField(
            label=await self.client.session.gtv(key='key'),
            value=await self.client.session.gtv(key=self.text['key'])
        )
        self.tf_value_default = TextField(
            label=await self.client.session.gtv(key='value_default'),
            value=await self.client.session.gtv(key=self.text['value_default'])
        )
        self.scroll = ScrollMode.AUTO
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                            title=await self.client.session.gtv(key=self.text['value_default']),
                        ),
                        Column(
                            controls=[
                                self.tf_key,
                                self.tf_value_default,
                                Row(
                                    controls=[
                                        FilledButton(
                                            content=Text(
                                                value=await self.client.session.gtv(key='update'),
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
                                            value=await self.client.session.gtv(key='translation'),
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
                                            value=language['language'],
                                            size=15,
                                            font_family=Fonts.REGULAR,
                                        ),
                                        Text(
                                            value=language['value'],
                                            size=10,
                                            font_family=Fonts.MEDIUM,
                                        ),
                                        Row(),
                                    ],
                                ),
                                ink=True,
                                padding=10,
                                on_click=functools.partial(self.translation_view, language),
                            ),
                            margin=0,
                        )
                        for language in self.text['translations']
                    ],
                ),
                padding=10,
            ),
        ]

    async def delete_text(self, _):
        from app.views.admin.texts.list import TextListView
        await self.client.session.api.text.delete(
            key=self.text['key'],
        )
        await self.client.change_view(view=TextListView())

    async def update_text(self, _):
        await self.client.session.api.text.update(
            key=self.text['key'],
            value_default=self.tf_value_default.value,
            new_key=self.tf_key.value
        )
        await self.update_async()

    async def create_translation(self, _):
        await self.client.change_view(view=CreateTranslationView(text_id=self.text_id))

    async def delete_translation(self, _):
        from app.views.admin.texts.list import TextListView
        await self.client.session.api.text.delete_translation(
            text_key=self.text['key'],
        )
        await self.client.change_view(view=TextListView())

    async def translation_view(self, language, _):
        text_key = self.text['key']
        await self.client.change_view(TranslationView(language=language, text_key=text_key))
