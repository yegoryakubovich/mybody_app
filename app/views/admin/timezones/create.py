#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
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

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import View


class CreateTimezoneView(View):
    route = '/admin'
    tf_deviation: TextField
    tf_id_str: TextField

    async def build(self):
        self.tf_id_str = TextField(
            label=await self.client.session.gtv(key='id_str'),
        )
        self.tf_deviation = TextField(
            label=await self.client.session.gtv(key='deviation'),
        )
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                            title=await self.client.session.gtv(key='create_timezone'),
                            create_button=False,
                        ),
                        self.tf_id_str,
                        self.tf_deviation,
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='create.py'),
                                size=16,
                            ),
                            on_click=self.create_timezone,
                        ),
                    ],
                ),
                padding=10,
            ),
        ]

    async def create_timezone(self, _):
        if len(self.tf_id_str.value) < 1 or len(self.tf_id_str.value) > 16:
            self.tf_id_str.error_text = await self.client.session.gtv(key='id_str_min_max_letter')
        elif not self.tf_deviation.value.isdigit():
            self.tf_deviation.error_text = await self.client.session.gtv(key='deviation_type')
        else:
            await self.client.session.api.timezone.create(
                id_str=self.tf_id_str.value,
                deviation=self.tf_deviation.value,
            )
            await self.client.change_view(go_back=True)
            await self.client.page.views[-1].restart()
