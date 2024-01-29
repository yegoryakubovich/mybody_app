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


from flet_core.dropdown import Option
from mybody_api_client.utils.base_section import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField, Dropdown
from app.controls.layout import AdminBaseView
from app.utils import Error, Fonts


class ArticleTranslationCreateView(AdminBaseView):
    route = '/admin/articles/translation/create'
    dd_language: Dropdown
    tf_name: TextField
    languages: list[dict]
    article: dict
    tf_not_language: Text

    def __init__(self, article_id):
        super().__init__()
        self.article_id = article_id

    async def build(self):
        await self.set_type(loading=True)
        self.article = await self.client.session.api.client.article.get(
            id_=self.article_id,
        )
        self.languages = await self.client.session.api.client.language.get_list()
        await self.set_type(loading=False)

        existing_translation_languages = [
            translation.get('language') for translation in self.article.get('translations', [])
        ]
        available_languages = [
            language for language in self.languages
            if language.get('id_str') not in existing_translation_languages
        ]

        languages_options = [
            Option(
                text=language.get('name'),
                key=language.get('id_str'),
            ) for language in available_languages
        ]

        self.tf_name = TextField(
            label=await self.client.session.gtv(key='name'),
        )
        if languages_options:
            self.dd_language = Dropdown(
                label=await self.client.session.gtv(key='language'),
                value=languages_options[0].key,
                options=languages_options,
            )
            language_control = self.dd_language
            button = FilledButton(
                content=Text(
                    value=await self.client.session.gtv(key='create'),
                    size=16,
                ),
                on_click=self.create_translation,
            )
            controls = [self.tf_name, language_control, button]
        else:
            self.tf_not_language = Text(
                value=await self.client.session.gtv(key='not_language'),
                size=20,
                font_family=Fonts.MEDIUM,
            )
            language_control = self.tf_not_language
            controls = [language_control]

        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_article_translation_create_view_title'),
            main_section_controls=controls,
        )

    async def create_translation(self, _):
        fields = [(self.tf_name, 1, 1024)]
        for field, min_len, max_len in fields:
            if not await Error.check_field(self, field, min_len=min_len, max_len=max_len):
                return
        try:
            await self.client.session.api.admin.article.create_translation(
                id_=self.article_id,
                language=self.dd_language.value,
                name=self.tf_name.value,
            )
            await self.client.change_view(go_back=True, with_restart=True)
        except ApiException as e:
            await self.set_type(loading=False)
            return await self.client.session.error(error=e)
