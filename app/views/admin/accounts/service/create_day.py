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

from datetime import datetime

from flet_core import ScrollMode
from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.input.textfielddate import TextFieldDate
from app.controls.layout import AdminBaseView
from app.utils import Error
from app.views.admin.accounts.service.get_day import DayView


class DayCreateView(AdminBaseView):
    route = '/admin/account/meal/day/create'
    tf_water_amount: TextField
    tf_date: TextField

    def __init__(self, account_service_id):
        super().__init__()
        self.account_service_id = account_service_id

    async def build(self):
        now = datetime.now()
        self.tf_date = TextFieldDate(
            label=await self.client.session.gtv(key='date'),
            value=now.strftime("%Y-%m-%d"),
            client=self.client
        )
        self.tf_water_amount = TextField(
            label=await self.client.session.gtv(key='water_amount'),
        )
        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_account_day_create_view_title'),
            main_section_controls=[
                self.tf_date,
                self.tf_water_amount,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='create'),
                        size=16,
                    ),
                    on_click=self.create_meal,
                ),
            ]
        )

    async def create_meal(self, _):
        fields = [(self.tf_water_amount, True)]
        for field, check_int in fields:
            if not await Error.check_field(self, field, check_int):
                return
        try:
            await self.set_type(loading=True)
            day_id = await self.client.session.api.admin.days.create(
                account_service_id=self.account_service_id,
                date=self.tf_date.value,
                water_amount=self.tf_water_amount.value,
            )
            await self.set_type(loading=False)
            await self.client.change_view(DayView(
                day_id=day_id
            ),
                delete_current=True,
            )
        except ApiException as exception:
            await self.set_type(loading=False)
            return await self.client.session.error(exception=exception)
