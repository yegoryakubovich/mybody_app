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


class AccountTrainingCreateView(AdminBaseView):
    route = '/admin/account/training/create'
    tf_date: TextField
    dd_articles: Dropdown
    articles = list[dict]

    def __init__(self, account_service_id):
        super().__init__()
        self.account_service_id = account_service_id

    async def build(self):
        await self.set_type(loading=True)
        self.articles = await self.client.session.api.client.article.get_list()
        await self.set_type(loading=False)
        article_options = [
            Option(
                text=article['name_text'],
                key=article['id']
            ) for article in self.articles
        ]
        self.dd_articles = Dropdown(
            label=await self.client.session.gtv(key='article'),
            options=article_options,
        )
        self.tf_date = TextField(
            label=await self.client.session.gtv(key='date'),
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_account_training_create_view_title'),
            main_section_controls=[
                self.tf_date,
                self.dd_articles,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='create'),
                        size=16,
                    ),
                    on_click=self.create_training,
                ),
            ]
        )

    async def create_training(self, _):
        from app.views.admin.accounts.training.get import AccountTrainingView
        try:
            training_id = await self.client.session.api.admin.meal.create(
                account_service_id=self.account_service_id,
                date=self.tf_date.value,
                article_id=self.dd_articles.value,
            )
            await self.client.change_view(AccountTrainingView(training_id=training_id), delete_current=True)
        except ApiException:
            await self.set_type(loading=False)
            return await self.client.session.error(code=0)
