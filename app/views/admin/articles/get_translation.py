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

from flet_core import Container, Row, Column

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import View
from config import URL_ARTICLES_UPDATE, URL_ARTICLES_GET


class TranslationView(View):
    route = '/admin'

    def __init__(self, language, article_id):
        super().__init__()
        self.article_id = article_id
        self.language = language

    async def build(self):
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                         title=self.language['language'],
                         create_button=False,
                        ),
                        Row(
                            controls=[
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='get_article'),
                                    ),
                                    url=URL_ARTICLES_GET + urlencode(
                                        {
                                            'id_': self.article_id,
                                            'token': '00000001:608c6cf5eb052a47e41e0ae21ff5c106',
                                            'is_admin': False,
                                            'language': self.language['language'],
                                        },
                                    ),
                                ),
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='update_article'),
                                    ),
                                    url=URL_ARTICLES_UPDATE + urlencode(
                                        {
                                            'id_': self.article_id,
                                            'token': '00000001:608c6cf5eb052a47e41e0ae21ff5c106',
                                            'is_admin': True,
                                            'language': self.language['language'],
                                        },
                                    ),
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
        response = await self.client.session.api.article.delete_translation(
            id_=self.article_id,
            language=self.language['language'],
        )
        print(response)
        await self.client.change_view(go_back=True)
        await self.client.page.views[-1].restart()
