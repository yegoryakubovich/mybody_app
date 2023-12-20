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


from flet_core import Container, Row, Column

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import View


class TranslationView(View):
    route = '/admin'
    tf_value = TextField

    def __init__(self, language, text_key):
        super().__init__()
        self.text_key = text_key
        self.language = language

    async def build(self):
        self.tf_value = TextField(
            label=await self.client.session.gtv(key='value'),
            value=self.language['value']
        )
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                         title=self.language['value'],
                         create_button=False,
                        ),
                        self.tf_value,
                        Row(
                            controls=[
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='update_translation'),
                                    ),
                                    on_click=self.update_translation,
                                ),
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='delete_translation'),
                                    ),
                                    on_click=self.delete_translation,
                                ),
                            ]
                        )
                    ],
                ),
                padding=10
            ),
        ]

    async def delete_translation(self, _):
        await self.client.session.api.text.delete_translation(
            text_key=self.text_key,
            language=self.language['language'],
        )
        await self.client.change_view(go_back=True)
        await self.client.page.views[-1].restart()

    async def update_translation(self, _):
        await self.client.session.api.text.update_translation(
            text_key=self.text_key,
            language=self.language['language'],
            value=self.tf_value.value,

        ),
        await self.client.change_view(go_back=True)
        await self.client.page.views[-1].restart()
