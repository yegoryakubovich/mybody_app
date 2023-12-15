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


from flet_core import Container, Column
from flet_core.dropdown import Option

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField, Dropdown
from app.controls.layout import View
from app.utils import Fonts



class CreateTranslationView(View):
    route = '/admin'
    dd_language_id_str: Dropdown
    tf_text_key: TextField
    tf_value: TextField

    def __init__(self, texts):
        super().__init__()
        self.texts = texts
        self.languages = None

    async def build(self):
        print(self.texts)
        self.languages = await self.client.session.api.language.get_list()

        languages_options = [
            Option(
                text=language.get('name'),
                key=language.get('id_str'),
            ) for language in self.languages.languages
        ]

        self.tf_value = TextField(
            label=await self.client.session.gtv(key='value'),
        )
        self.dd_language_id_str = Dropdown(
            label=await self.client.session.gtv(key='language_name'),
            options=languages_options,
        )
        self.controls = [
            await self.get_header(),
            Container(
                Column(
                    controls=[
                        Text(
                            value=await self.client.session.gtv(key='Create Translation'),
                            size=30,
                            font_family=Fonts.BOLD,
                        ),
                        self.tf_value,
                        self.dd_language_id_str,
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='Create'),
                                size=16,
                            ),
                            on_click=self.create_translation,
                        ),
                    ],
                ),
                padding=10,
            ),
        ]

    async def create_translation(self, _):
        if len(self.tf_value.value) < 1 or len(self.tf_value.value) > 1024:
            self.tf_value.error_text = await self.client.session.gtv(key='value_min_max_letter')
        elif len(self.dd_language_id_str.value) < 2 or len(self.dd_language_id_str.value) > 128:
            self.dd_language_id_str.error_text = await self.client.session.gtv(key='language_id_str_min_max_letter')
        else:
            await self.client.session.api.text.create_translation(
                value=self.tf_value.value,
                text_key=self.texts['key'],
                language_id_str=self.dd_language_id_str.value,
            )
            await self.client.change_view(go_back=True)
            await self.client.page.views[-1].restart()
