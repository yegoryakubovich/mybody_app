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


from flet_core import Row, Column, Container, padding

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField
from app.controls.layout import AuthView
from app.utils import Fonts
from app.utils.registration import Registration
from app.views.registration.registration_data import RegistrationDataView


class RegistrationView(AuthView):
    route = '/registration'
    tf_username: TextField
    tf_password: TextField

    async def change_view(self, _):
        username_error = await self.client.session.gtv(key='username_min_max_letter')
        password_error = await self.client.session.gtv(key='password_min_max_letter')

        if len(self.tf_username.value) < 6 or len(self.tf_username.value) > 32:
            self.tf_username.error_text = username_error
        elif len(self.tf_password.value) < 6 or len(self.tf_password.value) > 128:
            self.tf_password.error_text = password_error
        else:
            # Save in Registration
            self.client.session.registration = Registration()
            self.client.session.registration.username = self.tf_username.value
            self.client.session.registration.password = self.tf_password.value

            currencies = await self.client.session.api.currency.get_list()
            countries = await self.client.session.api.country.get_list()
            timezones = await self.client.session.api.timezone.get_list()

            await self.client.change_view(
                view=RegistrationDataView(
                    currencies=currencies.currencies,
                    countries=countries.countries,
                    timezones=timezones.timezones,
                ),
            )

        await self.update_async()
        for field in [
            self.tf_username,
            self.tf_password,
        ]:
            field.error_text = None

    async def go_authentication(self, _):
        from app.views.authentication import AuthenticationView
        await self.client.change_view(view=AuthenticationView())

    async def build(self):
        self.tf_username = TextField(
            label=await self.client.session.gtv(key='username'),
        )
        self.tf_password = TextField(
            label=await self.client.session.gtv(key='password'),
            password=True,
        )

        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='account_creation'),
            controls=[
                Column(
                    controls=[
                        self.tf_username,
                        self.tf_password,
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='next'),
                                size=16,
                            ),
                            on_click=self.change_view,
                            horizontal_padding=54,
                        ),
                        Container(
                            content=Row(
                                controls=[
                                    Text(
                                        value=await self.client.session.gtv(key='Already have an account?'),
                                        size=16,
                                        font_family=Fonts.REGULAR,
                                    ),
                                    Text(
                                        value=await self.client.session.gtv(key='Sign In'),
                                        size=16,
                                        font_family=Fonts.SEMIBOLD,
                                        color='#008F12',  # FIXME
                                    ),
                                ],
                                spacing=4,
                            ),
                            on_click=self.go_authentication,
                            ink=True,
                            padding=padding.symmetric(vertical=4),
                        ),
                    ],
                    spacing=20,
                ),
            ]
        )
