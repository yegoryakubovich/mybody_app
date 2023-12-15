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


from urllib.parse import urlencode

from flet_core import Container, Row, MainAxisAlignment, Card, Column, TextButton
from mybody_api_client import Article

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import View
from app.utils import Fonts
from app.views.admin.articles.create import CreateArticleView
from config import URL_ARTICLES


class ArticleView(View):
    route = '/admin'

    def __init__(self, articles_data):
        super().__init__()
        self.articles_data = articles_data

    async def build(self):
        article_data = self.articles_data
        translations = article_data.get('translations', [])

        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                         Row(
                             controls=[
                                 Text(
                                     value=await self.client.session.gtv(key=article_data['name_text']),
                                     font_family=Fonts.BOLD,
                                     size=30,
                                 ),
                                 FilledButton(
                                     content=Text(
                                         value=await self.client.session.gtv(key='Back'),
                                     ),
                                     on_click=self.go_back,
                                 ),
                             ],
                             alignment=MainAxisAlignment.SPACE_BETWEEN,
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
                     ] + [
                         Card(
                             content=Container(
                                 content=Column(
                                     controls=[
                                         Text(
                                             value=await self.client.session.gtv(
                                                 key=f"Language article {translation.get('language')}"
                                             ),
                                             size=30,
                                             font_family=Fonts.SEMIBOLD,
                                         ),
                                         Row(
                                             controls=[
                                                 TextButton(
                                                     await self.client.session.gtv(key='Deleted_article')),
                                             ],
                                             alignment=MainAxisAlignment.END,
                                         ),
                                     ],
                                 ),
                                 ink=True,
                                 padding=10,
                                 url=URL_ARTICLES.format(
                                     id_=article_data.get('id')) + urlencode(
                                     {
                                         'is_admin': True,
                                         'token': '00000001:608c6cf5eb052a47e41e0ae21ff5c106',
                                     }
                                 ),
                             ),
                             margin=0,
                         )
                         for translation in translations
                     ],
                ),
                padding=10,
            ),
        ]

    async def create_translation(self, _):
        pass

    async def go_back(self, _):
        await self.client.change_view(go_back=True)

    async def create_article(self, _):
        await self.client.change_view(view=CreateArticleView())

    async def article_view(self, _):
        response = await Article().get(
            id_=1,
            language=self.client.session.language,
        )
        names = [response.name]
        print(response)
