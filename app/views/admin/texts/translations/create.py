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


from flet_core import Container, Column
from flet_core.dropdown import Option

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField, Dropdown
from app.controls.layout import AdminBaseView
from app.utils import Error


class CreateTranslationTextView(AdminBaseView):
    route = '/admin'
    dd_language_id_str: Dropdown
    tf_text_key: TextField
    tf_value: TextField
    text = list[dict]

    def __init__(self, key):
        super().__init__()
        self.key = key
        self.languages = None

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.text.get(
            key=self.key
        )
        self.text = response.text
        languages = await self.client.session.api.language.get_list()
        await self.set_type(loading=False)

        languages_options = [
            Option(
                text=language.get('name'),
                key=language.get('id_str'),
            ) for language in languages.languages
        ]

        self.tf_value = TextField(
            label=await self.client.session.gtv(key='translation'),
        )
        self.dd_language_id_str = Dropdown(
            label=await self.client.session.gtv(key='language'),
            value=languages_options[0].key,
            options=languages_options,
        )
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=await self.get_controls(
                        title=await self.client.session.gtv(key='admin_translation_text_create_view_title'),
                        main_section_controls=[
                            self.tf_value,
                            self.dd_language_id_str,
                            FilledButton(
                                content=Text(
                                    value=await self.client.session.gtv(key='create'),
                                    size=16,
                                ),
                                on_click=self.create_translation,
                            ),
                        ],
                    ),
                ),
                padding=10,
            ),
        ]

    async def create_translation(self, _):
        fields = [(self.tf_value, 1, 1024)]
        for field, min_len, max_len in fields:
            if not await Error.check_field(self, field, min_len, max_len):
                return
        await self.client.session.api.text.create_translation(
            text_key=self.text['key'],
            language=self.dd_language_id_str.value,
            value=self.tf_value.value,
        )
        await self.client.change_view(go_back=True)
