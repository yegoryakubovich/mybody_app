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


import functools

from flet_core import Container, Row, Card, Text, Column, ScrollMode

from app.controls.layout import View
from app.utils import Fonts
from app.views.admin.countries.create import CreateCountryView
from app.views.admin.countries.get import CountryView


class CountryListView(View):
    route = '/admin'
    countries: list[dict]

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.country.get_list()
        self.countries = response.countries
        await self.set_type(loading=False)

        self.scroll = ScrollMode.AUTO
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                            title=await self.client.session.gtv(key='countries'),
                            on_create_click=self.create_country,
                        ),
                    ] + [
                        Card(
                            content=Container(
                                content=Column(
                                    controls=[
                                        Text(
                                            value=await self.client.session.gtv(key=country['name_text']),
                                            size=18,
                                            font_family=Fonts.SEMIBOLD,
                                        ),
                                        Row(),
                                    ],
                                ),
                                ink=True,
                                padding=10,
                                on_click=functools.partial(self.country_view, country['id_str']),
                            ),
                            margin=0,
                        )
                        for country in self.countries
                    ],
                ),
                padding=10,
            ),
        ]

    async def create_country(self, _):
        await self.client.change_view(view=CreateCountryView())

    async def country_view(self, country_id_str, _):
        await self.client.change_view(view=CountryView(country_id_str=country_id_str))
