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


from app.controls.layout import AdminBaseView
from app.views.admin.accounts.role import AccountRoleListView


class AccountServiceView(AdminBaseView):
    route = '/admin/accounts/service/get'
    account = list
    service = list

    def __init__(self, account_id):
        super().__init__()
        self.account_id = account_id

    async def build(self):
        await self.set_type(loading=True)
        self.account = await self.client.session.api.admin.account.get(
            id_=self.account_id
        )
        await self.set_type(loading=False)

        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_account_get_list_view_title')
        )

    async def delete_article(self):
        pass

    async def role_view(self, _):
        await self.client.change_view(view=AccountRoleListView(account_id=self.account_id))

    async def service_view(self, _):
        await self.client.change_view(view=AccountRoleListView(account_id=self.account_id))