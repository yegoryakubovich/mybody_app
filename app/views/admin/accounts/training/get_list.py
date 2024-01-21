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

from flet_core import ScrollMode

from app.controls.information import Text
from app.controls.information.card import Card
from app.controls.layout import AdminBaseView
from app.utils import Fonts
from app.views.admin.accounts.training import AccountTrainingView, AccountTrainingCreateView


class AccountTrainingListView(AdminBaseView):
    route = '/admin/account/training/list/get'
    trainings: list[dict]
    role: list
    date: str = None

    def __init__(self, account_service_id):
        super().__init__()
        self.account_service_id = account_service_id

    async def build(self):
        await self.set_type(loading=True)
        self.trainings = await self.client.session.api.client.training.get_list(
            account_service_id=self.account_service_id,
            date=self.date,
        )
        await self.set_type(loading=False)

        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_account_training_get_list_view_title'),
            on_create_click=self.create_training,
            main_section_controls=[
                Card(
                    controls=[
                        Text(
                            value=training['date'],
                            size=18,
                            font_family=Fonts.SEMIBOLD,
                        ),
                    ],
                    on_click=functools.partial(self.training_view, training['id']),
                )
                for training in self.trainings
            ],
        )

    async def training_view(self, training, _):
        await self.client.change_view(view=AccountTrainingView(training_id=training))

    async def create_training(self, _):
        await self.client.change_view(
            view=AccountTrainingCreateView(
                account_service_id=self.account_service_id,
            ),
        )
