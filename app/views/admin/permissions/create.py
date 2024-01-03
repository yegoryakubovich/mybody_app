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
from app.controls.layout import AdminBaseView
from app.utils.error import Error


class CreatePermissionView(AdminBaseView):
    route = '/admin'
    tf_name: TextField
    tf_id_str: TextField

    async def build(self):
        self.tf_id_str = TextField(
            label=await self.client.session.gtv(key='key'),
        )
        self.tf_name = TextField(
            label=await self.client.session.gtv(key='name'),
        )
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=await self.get_controls(
                        title=await self.client.session.gtv(key='admin_permission_create_view_title'),
                        main_section_controls=[
                            self.tf_id_str,
                            self.tf_name,
                            FilledButton(
                                content=Text(
                                    value=await self.client.session.gtv(key='create'),
                                    size=16,
                                ),
                                on_click=self.create_permission,
                            ),
                        ],
                    ),
                ),
                padding=10,
            ),
        ]

    async def create_permission(self, _):
        fields = [(self.tf_name, 1, 32), (self.tf_id_str, 1, 16)]
        for field, min_len, max_len in fields:
            if not await Error.check_field(self, field, min_len, max_len):
                return
        await self.client.session.api.permission.create(
            id_str=self.tf_id_str.value,
            name=self.tf_name.value,
        )
        await self.client.change_view(go_back=True)
