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


import functools

from flet_core import Text, ScrollMode

from app.controls.information.card import Card
from app.controls.layout import AdminBaseView
from app.utils import Fonts
from app.views.admin.articles.create import ArticleCreateView
from app.views.admin.articles.get import ArticleView


class ArticleListView(AdminBaseView):
    route = '/admin/article/list/get'
    articles: dict

    async def build(self):
        await self.set_type(loading=True)
        self.articles = await self.client.session.api.client.article.get_list()
        await self.set_type(loading=False)

        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_article_list_view_title'),
            on_create_click=self.create_article,
            main_section_controls=[
                Card(
                    controls=[
                        Text(
                            value=await self.client.session.gtv(key=article['name_text']),
                            size=18,
                            font_family=Fonts.SEMIBOLD,
                        ),
                    ],
                    on_click=functools.partial(self.article_view, article['id']),
                )
                for article in self.articles
            ],
        )

    async def create_article(self, _):
        await self.client.change_view(view=ArticleCreateView())

    async def article_view(self, article_id, _):
        await self.client.change_view(view=ArticleView(article_id=article_id))
