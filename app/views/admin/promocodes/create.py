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

from flet_core.dropdown import Option
from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField, Dropdown
from app.controls.input.textfielddate import TextFieldDate
from app.controls.layout import AdminBaseView
from app.utils import Error


class PromocodeCreateView(AdminBaseView):
    route = '/admin/promocode/create'
    tf_id_str: TextField
    tf_usage_quantity: TextField
    tf_date_from: TextField
    tf_date_to: TextField
    dd_promocode_type: Dropdown

    async def build(self):
        now = datetime.now()

        promocode_type_dict = {
            await self.client.session.gtv(key='percent'): 'percent',
            await self.client.session.gtv(key='amount'): 'amount',
        }
        promocode_type_options = [
            Option(
                text=promocode_type,
                key=promocode_type_dict[promocode_type],
            ) for promocode_type in promocode_type_dict
        ]
        self.dd_promocode_type = Dropdown(
            label=await self.client.session.gtv(key='type'),
            value=promocode_type_options[0].key,
            options=promocode_type_options,
        )
        self.tf_id_str = TextField(
            label=await self.client.session.gtv(key='name'),
        )
        self.tf_usage_quantity = TextField(
            label=await self.client.session.gtv(key='usage_quantity'),
        )
        self.tf_date_to = TextFieldDate(
            label=await self.client.session.gtv(key='date_to'),
            value=now.strftime("%Y-%m-%d"),
            client=self.client
        )
        self.tf_date_from = TextFieldDate(
            label=await self.client.session.gtv(key='date_from'),
            value=now.strftime("%Y-%m-%d"),
            client=self.client
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_promocode_create_view_title'),
            main_section_controls=[
                self.tf_id_str,
                self.tf_usage_quantity,
                self.tf_date_to,
                self.tf_date_from,
                self.dd_promocode_type,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='create'),
                        size=16,
                    ),
                    on_click=self.create_url,
                ),
            ],
         )

    async def create_url(self, _):
        fields = [(self.tf_id_str, 1, 64, False), (self.tf_usage_quantity, 1, 64, True)]
        for field, min_len, max_len, check_int in fields:
            if not await Error.check_field(self, field, check_int=check_int, min_len=min_len, max_len=max_len):
                return
        try:
            await self.set_type(loading=True)
            await self.client.session.api.admin.promocodes.create(
                id_str=self.tf_id_str.value,
                usage_quantity=self.tf_usage_quantity.value,
                date_from=self.tf_date_from.value,
                date_to=self.tf_date_to.value,
                type_=self.dd_promocode_type.value,
            )
            await self.set_type(loading=False)
            await self.client.change_view(go_back=True, with_restart=True, delete_current=True)
        except ApiException as exception:
            await self.set_type(loading=False)
            return await self.client.session.error(exception=exception)
