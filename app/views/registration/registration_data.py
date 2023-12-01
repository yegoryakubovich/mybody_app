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


from flet_core.dropdown import Option

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import Dropdown, TextField
from app.controls.layout import AuthView
from app.views.registration.user_agreement import UserAgreement


class RegistrationDataView(AuthView):
    route = '/registration'
    dd_country: Dropdown
    dd_currency: Dropdown
    dd_timezone: Dropdown
    tf_firstname: TextField
    tf_lastname: TextField
    tf_surname: TextField

    def __init__(self, countries, currencies, timezones, **kwargs):
        self.countries = countries
        self.currencies = currencies
        self.timezones = timezones
        super().__init__(**kwargs)

    async def build(self):
        country_options = [
            Option(
                text=i.get('name'),
                key=i.get('id_str'),
            ) for i in self.countries
        ]
        currency_options = [
            Option(
                text=i.get('name'),
                key=i.get('id_str'),
            ) for i in self.currencies
        ]
        timezone_options = [
            Option(
                text=i.get('name'),
                key=i.get('id_str'),
            ) for i in self.timezones
        ]

        self.tf_firstname = TextField(
            label=await self.client.session.gtv(key='firstname'),
        )
        self.tf_lastname = TextField(
            label=await self.client.session.gtv(key='lastname'),
        )
        self.tf_surname = TextField(
            label=await self.client.session.gtv(key='surname'),
        )
        self.dd_country = Dropdown(
            label=await self.client.session.gtv(key='country'),
            options=country_options,
        )
        self.dd_currency = Dropdown(
            label=await self.client.session.gtv(key='currency'),
            options=currency_options,
        )
        self.dd_timezone = Dropdown(
            label=await self.client.session.gtv(key='timezone'),
            options=timezone_options,
        )

        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='account_creation'),
            controls=[
                self.tf_firstname,
                self.tf_lastname,
                self.tf_surname,
                self.dd_country,
                self.dd_currency,
                self.dd_timezone,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='next'),
                        size=16,
                    ),
                    on_click=self.change_view,
                ),
            ],
        )

    async def change_view(self, _):
        firstname_error = await self.client.session.gtv(key='firstname_min_max_letter')
        lastname_error = await self.client.session.gtv(key='lastname_min_max_letter')
        surname_error = await self.client.session.gtv(key='surname_min_max_letter')
        country_error = await self.client.session.gtv(key='country_error')
        currency_error = await self.client.session.gtv(key='currency_error')
        timezone_error = await self.client.session.gtv(key='timezone_error')

        if len(self.tf_firstname.value) < 2 or len(self.tf_firstname.value) > 32:
            self.tf_firstname.error_text = firstname_error
        elif len(self.tf_lastname.value) < 2 or len(self.tf_lastname.value) > 32:
            self.tf_lastname.error_text = lastname_error
        elif self.tf_surname.value and (len(self.tf_surname.value) < 2 or len(self.tf_surname.value) > 32):
            self.tf_surname.error_text = surname_error
        elif not self.dd_country.value:
            self.dd_country.error_text = country_error
        elif not self.dd_currency.value:
            self.dd_currency.error_text = currency_error
        elif not self.dd_timezone.value:
            self.dd_timezone.error_text = timezone_error
        else:
            # Save in Registration
            self.client.session.registration.firstname = self.tf_firstname.value
            self.client.session.registration.lastname = self.tf_lastname.value
            self.client.session.registration.surname = self.tf_surname.value
            self.client.session.registration.country = self.dd_country.value
            self.client.session.registration.currency = self.dd_currency.value
            self.client.session.registration.timezone = self.dd_timezone.value

            await self.client.change_view(view=UserAgreement())

        await self.update_async()
        self.tf_firstname.error_text = None
        self.tf_lastname.error_text = None
        self.tf_surname.error_text = None
        self.dd_country.error_text = None
        self.dd_currency.error_text = None
        self.dd_timezone.error_text = None
