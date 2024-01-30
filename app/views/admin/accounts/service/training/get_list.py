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


from collections import defaultdict
from datetime import datetime, timedelta
from functools import partial

from flet_core import ScrollMode
from mybody_api_client.utils.base_section import ApiException

from app.controls.information import Text
from app.controls.information.card import Card
from app.controls.layout import AdminBaseView
from app.utils import Fonts
from app.views.admin.accounts.service.training.get import AccountTrainingView
from app.views.admin.accounts.service.training.create import AccountTrainingCreateView


class AccountTrainingListView(AdminBaseView):
    route = '/admin/account/training/list/get'
    trainings: list[dict]
    role: list
    duplicate: list[dict]
    date: str = None

    def __init__(self, account_service_id):
        super().__init__()
        self.account_service_id = account_service_id

    async def build(self):
        await self.set_type(loading=True)
        self.trainings = await self.client.session.api.admin.training.get_list(
            account_service_id=self.account_service_id,
            date=self.date,
        )
        training_by_date = defaultdict(list)
        for training in self. trainings:
            training_by_date[training['date']].append(training)

        sorted_dates = sorted(training_by_date.keys(), reverse=True)
        self.duplicate = training_by_date[sorted_dates[0]]
        await self.set_type(loading=False)
        
        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_account_training_get_list_view_title'),
            on_create_click=self.create_training,
            on_create_duplicate_click=self.create_duplicate_training,
            main_section_controls=[
                Card(
                    controls=[
                        Text(
                            value=training['date'],
                            size=18,
                            font_family=Fonts.SEMIBOLD,
                        ),
                    ],
                    on_click=partial(self.training_view, training['id']),
                )
                for training in sorted(self.trainings, key=lambda x: x['date'], reverse=True)
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
    
    async def create_duplicate_training(self, _):
        await self.set_type(loading=True)
        try:
            for training in self.duplicate:
                original_date = datetime.strptime(training['date'], '%Y-%m-%d')
                new_date = original_date + timedelta(days=1)
                new_date_str = new_date.strftime('%Y-%m-%d')

                training_id = await self.client.session.api.admin.training.create(
                    account_service_id=self.account_service_id,
                    date=new_date_str,
                    article_id=0,
                )
                for exercise in training['exercises']:
                    await self.client.session.api.admin.training.create_exercise(
                        training_id=training_id,
                        exercise_id=exercise['exercise'],
                        priority=exercise['priority'],
                        value=exercise['value'],
                        rest=exercise['rest'],
                    )
            await self.build()
            await self.update_async()
        except ApiException as e:
            await self.set_type(loading=False)
            return await self.client.session.error(error=e)
