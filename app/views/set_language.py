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


from flet_core.dropdown import Option

from app.controls.button import FilledButton
from app.controls.input import Dropdown
from app.controls.layout import AuthView


class SetLanguageView(AuthView):
    route = '/language'
    dropdown: Dropdown

    def __init__(self, languages, next_view, **kwargs):
        self.languages = languages
        self.next_view = next_view
        super().__init__(**kwargs)

    async def select(self, _):
        language = self.dropdown.value
        if not language:
            self.dropdown.error_text = await self.client.session.gtv(key='select_language_error')
            await self.update_async()
            await self.dropdown.focus_async()
        else:
            await self.set_type(loading=True)

            self.client.session.language = language
            await self.client.session.set_cs(key='language', value=language)

            await self.set_type(loading=False)
            await self.client.change_view(view=self.next_view)

    async def build(self):
        languages = self.languages.languages

        options = [
            Option(
                text=language.get('name'),
                key=language.get('id_str'),
            ) for language in languages
        ]
        self.dropdown = Dropdown(
            label=await self.client.session.gtv(key='language'),
            options=options,
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='set_language'),
            controls=[
                self.dropdown,
                FilledButton(
                    text=await self.client.session.gtv(key='next'),
                    on_click=self.select,
                ),
            ],
        )
