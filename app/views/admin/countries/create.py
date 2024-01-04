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
from app.utils import Error


class CountryCreateView(AdminBaseView):
    route = '/admin/country/create'
    tf_name: TextField
    tf_id_str: TextField
    languages = list[dict]
    timezones = list[dict]
    currencies = list[dict]
    dd_language = Dropdown
    dd_timezone = Dropdown
    dd_currency = Dropdown

    async def build(self):
        await self.set_type(loading=True)
        self.languages = await self.client.session.api.language.get_list()
        self.timezones = await self.client.session.api.timezone.get_list()
        self.currencies = await self.client.session.api.currency.get_list()
        await self.set_type(loading=False)

        language_options = [
            Option(
                text=language.get('name'),
                key=language.get('id_str'),
            ) for language in self.languages.languages
        ]
        timezone_options = [
            Option(
                text=timezone.get('id_str'),
                key=timezone.get('id_str'),
            ) for timezone in self.timezones.timezones
        ]
        currency_options = [
            Option(
                text=currency.get('name_text'),
                key=currency.get('id_str'),
            ) for currency in self.currencies.currencies
        ]

        self.dd_language = Dropdown(
            label=await self.client.session.gtv(key='language'),
            value=self.languages.languages[0]['id_str'],
            options=language_options,
        )
        self.dd_timezone = Dropdown(
            label=await self.client.session.gtv(key='timezone'),
            value=self.timezones.timezones[0]['id_str'],
            options=timezone_options,
        )
        self.dd_currency = Dropdown(
            label=await self.client.session.gtv(key='currency'),
            value=self.currencies.currencies[0]['id_str'],
            options=currency_options,
        )

        self.tf_id_str = TextField(
            label=await self.client.session.gtv(key='key'),
        )
        self.tf_name = TextField(
            label=await self.client.session.gtv(key='name'),
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_country_create_view_title'),
            main_section_controls=[
                self.tf_id_str,
                self.tf_name,
                self.dd_language,
                self.dd_timezone,
                self.dd_currency,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='create'),
                        size=16,
                    ),
                    on_click=self.create_country,
                ),
            ],
        )

    async def create_country(self, _):
        fields = [(self.tf_id_str, 2, 16), (self.tf_name, 1, 1024)]
        for field, min_len, max_len in fields:
            if not await Error.check_field(self, field, min_len, max_len):
                return
        await self.client.session.api.country.create(
            id_str=self.tf_id_str.value,
            name=self.tf_name.value,
            language=self.dd_language.value,
            timezone=self.dd_timezone.value,
            currency=self.dd_currency.value,
        )
        await self.client.change_view(go_back=True)
