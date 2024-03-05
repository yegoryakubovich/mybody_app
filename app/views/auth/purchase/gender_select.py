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


from flet_core import Column, Row, MainAxisAlignment
from flet_core.dropdown import Option

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import Dropdown
from app.controls.layout import AuthView
from app.utils import Fonts


class GenderSelectionView(AuthView):
    dd_gender: Dropdown

    async def change_view(self, _):
        from app.views.auth.purchase import QuestionnaireView
        dd_answers = []
        tf_answers = []
        self.client.session.answers = {}
        gender_list = {
            await self.client.session.gtv(key='men'): 'Men',
            await self.client.session.gtv(key='women'): 'Women',
        }
        gender_value = gender_list[self.dd_gender.value]
        await self.client.change_view(
            QuestionnaireView(
                gender=gender_value,
                dd_answers=dd_answers,
                tf_answers=tf_answers,
            ),
            delete_current=True
        )

    async def logout(self, _):
        await self.client.session.set_cs(key='token', value=None)
        from app.views.auth.init import InitView
        await self.client.change_view(view=InitView(), delete_current=True)

    async def build(self):
        gender_list = [
            await self.client.session.gtv(key='men'),
            await self.client.session.gtv(key='women'),
        ]
        gender_list_options = [
            Option(
                text=gender,
                key=gender,
            ) for gender in gender_list
        ]
        self.dd_gender = Dropdown(
            label=await self.client.session.gtv(key='gender'),
            value=gender_list[0],
            options=gender_list_options,
        )
        self.controls = await self.get_controls(
            controls=[
                Column(
                    controls=[
                        Text(
                            value=await self.client.session.gtv(key='gender_selection'),
                            font_family=Fonts.SEMIBOLD,
                            size=20,
                        ),
                        self.dd_gender,
                        Row(
                            controls=[
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='next'),
                                        size=16,
                                    ),
                                    horizontal_padding=54,
                                    on_click=self.change_view,
                                ),
                                FilledButton(
                                    content=Text(
                                        value=await self.client.session.gtv(key='logout'),
                                    ),
                                    on_click=self.logout
                                ),
                            ],
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                        )
                    ],
                ),
            ],
        )
