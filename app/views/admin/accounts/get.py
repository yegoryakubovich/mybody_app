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

from app.controls.button import FilledButton
from app.controls.information import Text, Card
from app.controls.layout import AdminBaseView, Section
from app.utils import Fonts
from app.views.admin.accounts.role import AccountRoleListView
from app.views.admin.accounts.service.get import AccountServiceView


class AccountView(AdminBaseView):
    route = '/admin/accounts/get'
    account: dict
    service: list[dict] = None

    def __init__(self, account_id):
        super().__init__()
        self.account_id = account_id

    async def build(self):
        await self.set_type(loading=True)
        self.account = await self.client.session.api.admin.account.get(
            id_=self.account_id
        )
        self.service = await self.client.session.api.admin.account.get_list_services(
            account_id=self.account_id,
        )
        await self.set_type(loading=False)

        # FIXME
        surname = self.account['surname'] if self.account['surname'] else await self.client.session.gtv(key='absent')

        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_account_get_view_title'),
            main_section_controls=[
                Text(
                    value=await self.client.session.gtv(key='basic_information'),
                    size=20,
                    font_family=Fonts.SEMIBOLD,
                ),
                Text(
                    value=f"{await self.client.session.gtv(key='firstname')}: {self.account['firstname']}\n"
                          f"{await self.client.session.gtv(key='lastname')}: {self.account['lastname']}\n"
                          f"{await self.client.session.gtv(key='surname')}: "
                          f"{surname}",
                    size=15,
                    font_family=Fonts.MEDIUM,
                ),
                Text(
                    value=await self.client.session.gtv(key='contact_details'),
                    size=20,
                    font_family=Fonts.SEMIBOLD,
                ),
                Text(
                    value=f"{await self.client.session.gtv(key='country')}: {self.account['country']}\n"
                          f"{await self.client.session.gtv(key='language')}: {self.account['language']}\n",
                    size=15,
                    font_family=Fonts.MEDIUM,
                ),
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='roles'),
                    ),
                    on_click=self.role_view,
                ),
            ],
            sections=[
                Section(
                    title=await self.client.session.gtv(key='services'),
                    controls=[
                        Card(
                            controls=[
                                Text(
                                    value='похудение',
                                    size=15,
                                    font_family=Fonts.REGULAR,
                                ),
                            ],
                            on_click=partial(self.service_view, service['id']),
                        )
                        for service in self.service
                    ],
                ),
            ],
        )

    async def role_view(self, _):
        await self.client.change_view(view=AccountRoleListView(account_id=self.account_id))

    async def service_view(self, service, _):
        await self.client.change_view(view=AccountServiceView(account_service_id=service))
