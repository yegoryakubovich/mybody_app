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

from flet_core import ScrollMode, AlertDialog, Row, Container, Image, MainAxisAlignment
from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.information.card import Card
from app.controls.input import TextField
from app.controls.layout import AdminBaseView
from app.utils import Fonts, Icons
from app.views.admin.accounts.service.training.create import AccountTrainingCreateView
from app.views.admin.accounts.service.training.get import AccountTrainingView


class AccountTrainingListView(AdminBaseView):
    route = '/admin/account/training/list/get'
    trainings: list[dict]
    role: list
    duplicate: list[dict]
    date: str = None
    dlg_modal = AlertDialog
    tf_date_duplicate_training = TextField

    def __init__(self, account_service_id):
        super().__init__()
        self.account_service_id = account_service_id

    async def build(self):
        await self.set_type(loading=True)
        self.trainings = await self.client.session.api.admin.training.get_list(
            account_service_id=self.account_service_id,
            date=self.date,
        )
        await self.set_type(loading=False)

        self.tf_date_duplicate_training = TextField(
                label=await self.client.session.gtv(key='date'),
            )
        self.dlg_modal = AlertDialog(
            content=self.tf_date_duplicate_training,
            actions=[
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='create'),
                        size=16,
                    ),
                    on_click=self.create_duplicate_training
                ),
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='close'),
                        size=16,
                    ),
                    on_click=self.close_dlg,
                ),
            ],
            modal=False,
        )
        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_account_training_get_list_view_title'),
            on_create_click=self.create_training,
            main_section_controls=[
                self.dlg_modal, ] + [
                Card(
                    controls=[
                        Row(
                            controls=[
                                Text(
                                    value=training['date'],
                                    size=18,
                                    font_family=Fonts.SEMIBOLD,
                                ),
                                Container(
                                    content=Row(
                                        controls=[
                                            Image(
                                                src=Icons.CREATE,
                                                height=10,
                                                color='#FFFFFF',
                                            ),
                                            Text(
                                                value=await self.client.session.gtv(key='create_duplicate'),
                                                size=13,
                                                font_family=Fonts.SEMIBOLD,
                                                color='#FFFFFF',
                                            ),
                                        ],
                                        spacing=4,
                                    ),
                                    padding=7,
                                    border_radius=24,
                                    bgcolor='#008F12',
                                    on_click=partial(self.open_dlg_modal, training['date']),
                                ),
                            ],
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ],
                    on_click=partial(self.training_view, training['id']),
                )
                for training in sorted(self.trainings, key=lambda x: x['date'], reverse=True)
            ],
        )

    async def close_dlg(self, _):
        self.dlg_modal.open = False
        await self.update_async()

    async def open_dlg_modal(self, date, _):
        self.date = date
        self.dlg_modal.open = True
        await self.update_async()

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
        duplicate_training = await self.client.session.api.admin.training.get_list(
            account_service_id=self.account_service_id,
            date=self.date,
        )
        print(duplicate_training)
        try:
            for training in duplicate_training:
                training_id = await self.client.session.api.admin.training.create(
                    account_service_id=self.account_service_id,
                    date=self.tf_date_duplicate_training.value,
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
            await self.set_type(loading=False)
            await self.build()
            await self.update_async()
        except ApiException as e:
            await self.set_type(loading=False)
            return await self.client.session.error(error=e)
