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


from flet_core.dropdown import Option

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField, Dropdown
from app.controls.layout import AdminBaseView


class AccountRoleCreateView(AdminBaseView):
    route = '/admin/articles/create'
    tf_name: TextField
    dd_role: Dropdown
    roles: list[dict]

    def __init__(self, account_id):
        super().__init__()
        self.account_id = account_id

    async def build(self):
        await self.set_type(loading=True)
        self.roles = await self.client.session.api.client.role.get_list()
        await self.set_type(loading=False)

        role_options = [
            Option(
                text=role.get('name_text'),
                key=role.get('id'),
            ) for role in self.roles
        ]

        self.dd_role = Dropdown(
            label=await self.client.session.gtv(key='language'),
            value=role_options[0].key,
            options=role_options,
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_account_role_create_view_title'),
            main_section_controls=[
                self.dd_role,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='create'),
                        size=16,
                    ),
                    on_click=self.create_article,
                ),
            ]
        )

    async def create_article(self, _):
        await self.client.session.api.admin.account.create_role(
            account_id=self.account_id,
            role_id=self.dd_role.value,
        )
        await self.client.change_view(go_back=True, with_restart=True)