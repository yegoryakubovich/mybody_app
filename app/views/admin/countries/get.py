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


from flet_core import Row
from flet_core.dropdown import Option, Dropdown

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import AdminBaseView


class CountryView(AdminBaseView):
    route = '/admin/country/get'
    country = dict
    languages = list[dict]
    timezones = list[dict]
    currencies = list[dict]
    dd_language = Dropdown
    dd_timezone = Dropdown
    dd_currency = Dropdown

    def __init__(self, country_id_str):
        super().__init__()
        self.country_id_str = country_id_str

    async def build(self):
        await self.set_type(loading=True)
        self.country = await self.client.session.api.client.country.get(
            id_str=self.country_id_str
        )
        self.languages = await self.client.session.api.client.language.get_list()
        self.timezones = await self.client.session.api.client.timezone.get_list()
        self.currencies = await self.client.session.api.client.currency.get_list()
        await self.set_type(loading=False)

        language_options = [
            Option(
                text=language.get('name'),
                key=language.get('id_str'),
            ) for language in self.languages
        ]
        timezone_options = [
            Option(
                text=timezone.get('id_str'),
                key=timezone.get('id_str'),
            ) for timezone in self.timezones
        ]
        currency_options = [
            Option(
                text=currency.get('name_text'),
                key=currency.get('id_str'),
            ) for currency in self.currencies
        ]

        self.dd_language = Dropdown(
            label=await self.client.session.gtv(key='language'),
            value=self.country['language'],
            options=language_options,
        )
        self.dd_timezone = Dropdown(
            label=await self.client.session.gtv(key='timezone'),
            value=self.country['timezone'],
            options=timezone_options,
        )
        self.dd_currency = Dropdown(
            label=await self.client.session.gtv(key='currency'),
            value=self.country['currency'],
            options=currency_options,
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key=self.country['name_text']),
            main_section_controls=[
                self.dd_language,
                self.dd_currency,
                self.dd_timezone,
                Row(
                    controls=[
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='save'),
                            ),
                            on_click=self.update_country,
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='delete'),
                            ),
                            on_click=self.delete_country,
                        ),
                    ],
                ),
            ],
        )

    async def delete_country(self, _):
        await self.client.session.api.admin.country.delete(
            id_str=self.country_id_str,
        )
        await self.client.change_view(go_back=True)

    async def update_country(self, _):
        await self.client.session.api.admin.country.update(
            id_str=self.country_id_str,
            language=self.dd_language.value,
            currency=self.dd_currency.value,
            timezone=self.dd_timezone.value,
        )
        await self.client.change_view(go_back=True)
