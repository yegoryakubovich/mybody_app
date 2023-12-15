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

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import View
from app.utils import Fonts


class CreateArticleView(View):
    route = '/admin'
    tf_name: TextField

    async def build(self):
        self.tf_name = TextField(
            label=await self.client.session.gtv(key='Name Article'),
        )
        self.controls = [
            await self.get_header(),
            Container(
                Column(
                    controls=[
                        Text(
                            value=await self.client.session.gtv(key='Create Article'),
                            size=25,
                            font_family=Fonts.SEMIBOLD,
                        ),
                        self.tf_name,
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='Create'),
                                size=16,
                            ),
                            on_click=self.create_article,
                            horizontal_padding=54,
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='go_back'),
                                size=16,
                            ),
                            on_click=self.go_back,
                            horizontal_padding=54,
                        ),
                    ],
                ),
                padding=10,
            ),
        ]

    async def go_back(self, _):
        await self.client.change_view(go_back=True)

    async def create_article(self, _):
        if len(self.tf_name.value) < 1 or len(self.tf_name.value) > 1024:
            self.tf_name.error_text = await self.client.session.gtv(key='name_min_max_letter')
        else:
            response = await self.client.session.api.article.create(
                name=self.tf_name.value,
            )
            print(response)