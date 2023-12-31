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
from app.controls.input import Dropdown
from app.controls.layout import View
from app.utils import Fonts


class CreateTrainingView(View):
    route = '/admin'
    dd_account_service_id: Dropdown
    dd_article_id: Dropdown

    async def build(self):
        await self.set_type(loading=True)
        articles = await self.client.session.api.article.get_list()
        account_services = await self.client.session.api.account.services_get_list()
        await self.set_type(loading=False)

        article_options = [
            Option(
                text=article['name_text'],
                key=article['id'],
            ) for article in articles
        ]

        account_services_options = [
            Option(
                text=account_service['account'],
                key=account_service['id'],
            ) for account_service in account_services
        ]

        self.dd_account_service_id = Dropdown(
            label=await self.client.session.gtv(key='account_service'),
            value=self.product['type'],
            options=article_options,
        )
        self.dd_article_id = Dropdown(
            label=await self.client.session.gtv(key='articles'),
            value=self.product['type'],
            options=account_services_options,
        )
        self.controls = [
            await self.get_header(),
            Container(
                Column(
                    controls=[
                        Text(
                            value=await self.client.session.gtv(key='Create Texts'),
                            size=30,
                            font_family=Fonts.BOLD,
                        ),
                        self.tf_value_default,
                        self.tf_key,
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='Create'),
                                size=15,
                                font_family=Fonts.REGULAR,
                            ),
                            on_click=self.create_text,
                        ),
                    ],
                ),
                padding=10,
            ),
        ]

    async def create_text(self, _):
        if len(self.tf_value_default.value) < 1 or len(self.tf_value_default.value) > 1024:
            self.tf_value_default.error_text = await self.client.session.gtv(key='value_default_min_max_letter')
        elif len(self.tf_key.value) < 2 or len(self.tf_key.value) > 128:
            self.tf_key.error_text = await self.client.session.gtv(key='key_min_max_letter')
        else:
            await self.client.session.api.admin.text.create(
                value_default=self.tf_value_default.value,
                key=self.tf_key.value,
            )
        await self.update_async()
        for field in [
            self.tf_value_default,
            self.tf_key,
        ]:
            field.error_text = None
