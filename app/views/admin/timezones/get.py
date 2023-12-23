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
from app.controls.layout import View


class TimezoneView(View):
    route = '/admin'
    timezone = list[dict]

    def __init__(self, timezone_id_str):
        super().__init__()
        self.timezone_id_str = timezone_id_str

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.timezone.get(
            id_str=self.timezone_id_str
        )
        self.timezone = response.language
        await self.set_type(loading=False)

        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                         title=await self.client.session.gtv(key=self.timezone['id_str']),
                         create_button=False,
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='delete_timezone'),
                            ),
                            on_click=self.delete_timezone,
                        ),
                    ],
                ),
                padding=10,
            ),
        ]

    async def delete_timezone(self, _):
        await self.client.session.api.timezone.delete(
            id_str=self.timezone_id_str
        )
        await self.client.change_view(go_back=True)
        await self.client.page.views[-1].restart()
