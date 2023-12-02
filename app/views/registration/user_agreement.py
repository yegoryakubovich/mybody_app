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


from flet_core import Column
from mybody_api_client import Account

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import AuthView
from app.views.registration.registration_successful import RegistrationSuccessfulView


class UserAgreement(AuthView):
    route = '/registration'

    async def build(self):
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='account_creation'),
            controls=[
                Column(
                    controls=[
                        Text(
                            value=await self.client.session.gtv(key='agreement_info'),
                            size=16,
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='account_creation_button'),
                                size=16,
                            ),
                            on_click=self.change_view,
                        ),
                    ],
                    spacing=20,
                ),
            ],
        )

    async def change_view(self, _):
        await Account().create(
            username=self.client.session.registration.username,
            password=self.client.session.registration.password,
            firstname=self.client.session.registration.firstname,
            lastname=self.client.session.registration.lastname,
            surname=self.client.session.registration.surname or None,
            country=self.client.session.registration.country,
            language=self.client.session.language,
            timezone=self.client.session.registration.timezone,
            currency=self.client.session.registration.currency,
        )
        await self.client.change_view(view=RegistrationSuccessfulView())

        await self.update_async()
