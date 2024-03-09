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

from flet_core import ScrollMode, AlertDialog, Row, Container, Image, MainAxisAlignment, TextButton, colors
from mybody_api_client.utils import ApiException

from app.controls.information import Text
from app.controls.information.card import Card
from app.controls.input import TextField
from app.controls.input.textfielddate import TextFieldDate
from app.controls.layout import AdminBaseView
from app.utils import Fonts, Icons
from app.views.admin.accounts.service.training.create import AccountTrainingCreateView
from app.views.admin.accounts.service.training.get import AccountTrainingView


class AccountTrainingListView(AdminBaseView):
    route = '/admin/account/trainings/list/get'
    trainings: list[dict]
    duplicate: list[dict]
    role: dict
    date: str = None
    duplicate_date: str = None
    dlg_modal: AlertDialog
    tf_date_duplicate_training: TextField

    def __init__(self, account_service_id):
        super().__init__()
        self.account_service_id = account_service_id

    async def build(self):
        await self.set_type(loading=True)
        self.trainings = await self.client.session.api.admin.trainings.get_list(
            account_service_id=self.account_service_id,
        )
        await self.set_type(loading=False)

        self.tf_date_duplicate_training = TextFieldDate(
            label=await self.client.session.gtv(key='date'),
            client=self.client
        )
        self.dlg_modal = AlertDialog(
            content=self.tf_date_duplicate_training,
            actions=[
                Row(
                    controls=[
                        TextButton(
                            content=Text(
                                value=await self.client.session.gtv(key='create'),
                                size=16,
                            ),
                            on_click=self.create_duplicate_training
                        ),
                        TextButton(
                            content=Text(
                                value=await self.client.session.gtv(key='close'),
                                size=16,
                            ),
                            on_click=self.close_dlg,
                        ),
                    ],
                    alignment=MainAxisAlignment.END
                ),
            ],
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
                                           color=colors.ON_PRIMARY,
                                       ),
                                   ] + (
                                       [
                                           Container(
                                               content=Row(
                                                   controls=[
                                                       Image(
                                                           src=Icons.CREATE,
                                                           height=10,
                                                           color=colors.ON_BACKGROUND,
                                                       ),
                                                       Text(
                                                           value=await self.client.session.gtv(
                                                               key='create_duplicate'),
                                                           size=13,
                                                           font_family=Fonts.SEMIBOLD,
                                                           color=colors.ON_BACKGROUND,
                                                       ),
                                                   ],
                                                   spacing=4,
                                               ),
                                               padding=7,
                                               border_radius=24,
                                               bgcolor=colors.BACKGROUND,
                                               on_click=partial(self.open_dlg,
                                                                training['date']),
                                           ),
                                       ] if 'exercises' in training and training[
                                           'exercises'] else []
                                   ),
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

    async def open_dlg(self, date, _):
        self.duplicate_date = date
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
        try:
            duplicate_training = await self.client.session.api.admin.trainings.get_by_date(
                account_service_id=self.account_service_id,
                date=self.duplicate_date,
            )
            for training in duplicate_training:
                training_id = await self.client.session.api.admin.trainings.create(
                    account_service_id=self.account_service_id,
                    date=self.tf_date_duplicate_training.value,
                )
                for exercise in training['exercises']:
                    await self.client.session.api.admin.trainings.exercises.create(
                        training_id=training_id,
                        exercise_id=exercise['exercise'],
                        priority=exercise['priority'],
                        value=exercise['value'],
                        rest=exercise['rest'],
                    )
                    await self.set_type(loading=False)
            await self.restart()
        except ApiException as exception:
            await self.set_type(loading=False)
            return await self.client.session.error(exception=exception)
