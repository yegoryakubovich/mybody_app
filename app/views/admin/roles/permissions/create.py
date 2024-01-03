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


from flet_core import Container, Column
from flet_core.dropdown import Option

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import Dropdown
from app.controls.layout import AdminBaseView


class RoleCreatePermissionView(AdminBaseView):
    route = '/admin'
    dd_permission: Dropdown
    permissions = dict

    def __init__(self, role_id):
        super().__init__()
        self.role_id = role_id

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.permission.get_list()
        self.permissions = response.permissions
        await self.set_type(loading=False)

        permissions_options = [
            Option(
                text=permission.get('name_text'),
                key=permission.get('id_str'),
            ) for permission in self.permissions
        ]
        self.dd_permission = Dropdown(
            label=await self.client.session.gtv(key='permission'),
            value=self.permissions[0]['name_text'],
            options=permissions_options,
        )
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=await self.get_controls(
                        title=await self.client.session.gtv(key='admin_role_permission_create_view_title'),
                        main_section_controls=[
                            self.dd_permission,
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
            )
        ]

    async def create_permission(self, _):
        await self.client.session.api.role.create_permission(
            role_id=self.role_id,
            permission=self.dd_permission.value,
        )
        await self.client.change_view(go_back=True)
