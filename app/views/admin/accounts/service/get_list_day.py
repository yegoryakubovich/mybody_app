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

from flet_core import ScrollMode, Row, Container, Image, MainAxisAlignment, AlertDialog, TextButton, colors

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.information.card import Card
from app.controls.input import TextField
from app.controls.input.textfielddate import TextFieldDate
from app.controls.layout import AdminBaseView, Section
from app.utils import Fonts, Icons
from app.views.admin.accounts.service.create_day import DayCreateView
from app.views.admin.accounts.service.get_day import DayView


class AccountServiceView(AdminBaseView):
    route = '/admin/accounts/service/get'
    days: list[dict]
    duplicate: list[dict]
    date: str = None
    duplicate_date: str = None
    dlg_modal = AlertDialog
    tf_date_duplicate_meal = TextField

    def __init__(self, account_service_id):
        super().__init__()
        self.account_service_id = account_service_id

    async def build(self):
        self.days = await self.client.session.api.admin.days.get_list(
            account_service_id=self.account_service_id,
        )
        self.tf_date_duplicate_meal = TextFieldDate(
            label=await self.client.session.gtv(key='date'),
            client=self.client
        )
        self.dlg_modal = AlertDialog(
            content=self.tf_date_duplicate_meal,
            actions=[
                Row(
                    controls=[
                        TextButton(
                            content=Text(
                                value=await self.client.session.gtv(key='create'),
                                size=16,
                            ),
                            on_click=self.create_duplicate_meal
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
                )
            ],
            modal=False,
        )
        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='individual_nutrition_plan'),
            main_section_controls=[
                self.dlg_modal,
                Row(
                    controls=[
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='go_questionnaire'),
                            ),
                            on_click=self.questionnaire_view,
                        ),
                    ],
                ),
            ],
            sections=[
                Section(
                    title=await self.client.session.gtv(key='days'),
                    create_button=self.create_day,
                    controls=[
                        Card(
                            controls=[
                                Row(
                                    controls=[
                                                 Text(
                                                     value=days['date'],
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
                                                                     no_wrap=False,
                                                                 ),
                                                             ],
                                                             spacing=4,
                                                         ),
                                                         padding=7,
                                                         border_radius=24,
                                                         bgcolor=colors.BACKGROUND,
                                                         on_click=partial(self.open_dlg, days),
                                                     ),
                                                 ]
                                             ),
                                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                                ),
                            ],
                            on_click=partial(self.day_view, days['id']),
                        ) for days in self.days
                    ],
                )
            ],
        )

    async def create_day(self, _):
        await self.client.change_view(view=DayCreateView(account_service_id=self.account_service_id))

    async def day_view(self, day_id, _):
        await self.client.change_view(view=DayView(day_id=day_id))

    async def create_duplicate_meal(self, _):
        pass

    async def close_dlg(self, _):
        self.dlg_modal.open = False
        await self.update_async()

    async def open_dlg(self, date, _):
        self.duplicate_date = date
        self.dlg_modal.open = True
        await self.update_async()

    async def questionnaire_view(self, _):
        from app.views.admin.accounts.service.questionnaire import AccountQuestionnaireGetView
        await self.client.change_view(view=AccountQuestionnaireGetView(account_service_id=self.account_service_id))
