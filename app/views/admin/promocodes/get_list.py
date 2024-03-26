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

from flet_core import Text, ScrollMode, colors

from app.controls.information.card import Card
from app.controls.layout import AdminBaseView
from app.utils import Fonts
from app.views.admin.promocodes import PromocodeCreateView, PromocodeView


class PromocodeListView(AdminBaseView):
    route = '/admin/promocode/list/get'
    promocodes: list[dict]

    async def build(self):
        await self.set_type(loading=True)
        self.promocodes = await self.client.session.api.admin.promocodes.get_list()
        await self.set_type(loading=False)

        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_promocode_get_list_view_title'),
            create_button=self.create_promocode,
            main_section_controls=[
                Card(
                    controls=[
                        Text(
                            value=promocode['id_str'],
                            size=18,
                            font_family=Fonts.SEMIBOLD,
                            color=colors.ON_PRIMARY,
                        ),
                    ],
                    on_click=partial(self.promocode_view, promocode['id_str']),
                )
                for promocode in self.promocodes
            ],
         )

    async def create_promocode(self, _):
        await self.client.change_view(view=PromocodeCreateView())

    async def promocode_view(self, promocode_id_str, _):
        await self.client.change_view(view=PromocodeView(promocode_id_str=promocode_id_str))
