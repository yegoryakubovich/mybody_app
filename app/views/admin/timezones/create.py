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


from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import AdminBaseView
from app.utils import Error


class TimezoneCreateView(AdminBaseView):
    route = '/admin'
    tf_deviation: TextField
    tf_id_str: TextField

    async def build(self):
        self.tf_id_str = TextField(
            label=await self.client.session.gtv(key='key'),
        )
        self.tf_deviation = TextField(
            label=await self.client.session.gtv(key='deviation'),
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_timezone_create_view_title'),
            main_section_controls=[
                self.tf_id_str,
                self.tf_deviation,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='create'),
                        size=16,
                    ),
                    on_click=self.create_timezone,
                ),
            ],
         )

    async def create_timezone(self, _):
        fields = [(self.tf_id_str, 1, 16)]
        for field, min_len, max_len in fields:
            if not await Error.check_field(self, field, min_len, max_len):
                return
        if not self.tf_deviation.value.isdigit():
            self.tf_deviation.error_text = await self.client.session.gtv(key='deviation_type')
            await self.update_async()
        else:
            await self.client.session.api.admin.timezone.create(
                id_str=self.tf_id_str.value,
                deviation=self.tf_deviation.value,
            )
            await self.client.change_view(go_back=True)
