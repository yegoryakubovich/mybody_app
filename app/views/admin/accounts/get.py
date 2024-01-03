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

from app.controls.information import Text
from app.controls.layout import View


class AccountView(View):
    route = '/admin/accounts/get'
    account = list

    def __init__(self, account_id):
        super().__init__()
        self.account_id = account_id

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.account.get(
            id_=self.account_id
        )
        self.account = response.account
        await self.set_type(loading=False)

        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                         title=await self.client.session.gtv(key=self.account['username']),
                        ),
                        Text(
                            value=await self.client.session.gtv(key=self.account['firstname']),
                        ),
                        Text(
                            value=await self.client.session.gtv(key=self.account['lastname']),
                        ),
                        Text(
                            value=self.account['surname']
                            if self.account['surname']
                            else await self.client.session.gtv(key='no'),
                        ),
                        Text(
                            value=await self.client.session.gtv(key=self.account['country']),
                        ),
                        Text(
                            value=await self.client.session.gtv(key=self.account['language']),
                        ),
                        Text(
                            value=await self.client.session.gtv(key=self.account['timezone']),
                        ),
                        Text(
                            value=await self.client.session.gtv(key=self.account['currency']),
                        ),
                    ],
                ),
                padding=10,
            ),
        ]
