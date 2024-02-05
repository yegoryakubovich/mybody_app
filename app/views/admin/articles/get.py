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


from functools import partial

from flet_core import Row, ScrollMode
from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.button.switch import StitchButton
from app.controls.information import Text
from app.controls.information.card import Card
from app.controls.layout.admin import AdminBaseView, Section
from app.utils import Fonts
from app.utils.article import get_url_article, UrlTypes
from app.views.admin.articles.create import ArticleCreateView
from app.views.admin.articles.translations.create import ArticleTranslationCreateView
from app.views.admin.articles.translations.get import ArticleTranslationView


class ArticleView(AdminBaseView):
    route = '/admin/articles/get'
    article = list[dict]
    is_hide = bool

    def __init__(self, article_id):
        super().__init__()
        self.article_id = article_id

    async def build(self):
        await self.set_type(loading=True)
        self.article = await self.client.session.api.client.articles.get(
            id_=self.article_id
        )
        await self.set_type(loading=False)
        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key=self.article['name_text']),
            main_section_controls=[
                StitchButton(
                    label=await self.client.session.gtv(key='admin_article_get_view_hide'),
                    value=self.article['is_hide'],
                    on_change=self.change_visibility
                ),
                Row(
                    controls=[
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='admin_article_get_view_look'),
                            ),
                            url=get_url_article(
                                id_=self.article.get('id'),
                                token=self.client.session.token,
                                is_admin=False,
                                type_=UrlTypes.GET,
                            ),
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='update'),
                            ),
                            url=get_url_article(
                                id_=self.article.get('id'),
                                token=self.client.session.token,
                                is_admin=True,
                                type_=UrlTypes.UPDATE,
                            ),
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='delete'),
                            ),
                            on_click=self.delete_article,
                        ),
                    ],
                ),
            ],
            sections=[
                Section(
                    title=await self.client.session.gtv(key='translations'),
                    on_create_click=self.create_translation,
                    controls=[
                        Card(
                            controls=[
                                Text(
                                    value=translation.get('language'),
                                    size=15,
                                    font_family=Fonts.REGULAR,
                                ),
                            ],
                            on_click=partial(self.translate_view, translation),
                        )
                        for translation in self.article['translations']
                    ],
                ),
            ],
        )

    async def delete_article(self, _):
        try:
            await self.client.session.api.admin.articles.delete(
                id_=self.article_id,
            )
            await self.client.change_view(go_back=True, with_restart=True)
        except ApiException as e:
            await self.set_type(loading=False)
            return await self.client.session.error(error=e)

    async def change_visibility(self, _):
        await self.client.session.api.admin.articles.update(
            id_=self.article_id,
            is_hide=not self.article['is_hide'],
        )
        await self.update_async()

    async def create_translation(self, _):
        await self.client.change_view(
            view=ArticleTranslationCreateView(
                article_id=self.article_id,
            ),
        )

    async def create_article(self, _):
        await self.client.change_view(view=ArticleCreateView())

    async def translate_view(self, translation, _):
        await self.client.change_view(
            view=ArticleTranslationView(
                article_id=self.article_id,
                language=translation,
            ),
        )
