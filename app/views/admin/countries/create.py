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


from flet_core import Container, Column
from flet_core.dropdown import Option

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField, Dropdown
from app.controls.layout import View


class CreateCountryView(View):
    route = '/admin'
    tf_name: TextField
    tf_id_str: TextField
    dd_language = Dropdown
    dd_timezone = Dropdown
    dd_currency = Dropdown

    async def build(self):
        await self.set_type(loading=True)
        languages = await self.client.session.api.language.get_list()
        timezones = await self.client.session.api.timezone.get_list()
        currencies = await self.client.session.api.currency.get_list()
        await self.set_type(loading=False)

        language_options = [
            Option(
                text=language.get('name'),
                key=language.get('id_str'),
            ) for language in languages.languages
        ]
        timezone_options = [
            Option(
                text=timezone.get('id_str'),
                key=timezone.get('id_str'),
            ) for timezone in timezones.timezones
        ]
        currency_options = [
            Option(
                text=currency.get('name_text'),
                key=currency.get('id_str'),
            ) for currency in currencies.currencies
        ]

        self.dd_language = Dropdown(
            label=await self.client.session.gtv(key='language'),
            value=languages.languages[0]['id_str'],
            options=language_options,
        )
        self.dd_timezone = Dropdown(
            label=await self.client.session.gtv(key='timezone'),
            value=timezones.timezones[0]['id_str'],
            options=timezone_options,
        )
        self.dd_currency = Dropdown(
            label=await self.client.session.gtv(key='currency'),
            value=currencies.currencies[0]['id_str'],
            options=currency_options,
        )

        self.tf_id_str = TextField(
            label=await self.client.session.gtv(key='id_str'),
        )
        self.tf_name = TextField(
            label=await self.client.session.gtv(key='name_currency'),
        )
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                            title=await self.client.session.gtv(key='create_country'),
                            create_button=False,
                        ),
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
                ),
                padding=10,
            ),
        ]

    async def create_country(self, _):
        if len(self.tf_id_str.value) < 2 or len(self.tf_id_str.value) > 16:
            self.tf_id_str.error_text = await self.client.session.gtv(key='id_str_min_max_letter')
        elif len(self.tf_name.value) < 1 or len(self.tf_name.value) > 1024:
            self.tf_name.error_text = await self.client.session.gtv(key='name_min_max_letter')
        else:
            await self.client.session.api.country.create(
                id_str=self.tf_id_str.value,
                name=self.tf_name.value,
                language=self.dd_language.value,
                timezone=self.dd_timezone.value,
                currency=self.dd_currency.value,
            )
            await self.client.change_view(go_back=True)
            await self.client.page.views[-1].restart()
