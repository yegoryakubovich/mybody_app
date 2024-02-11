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

from flet_core import Column
from flet_core.dropdown import Option

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import Dropdown
from app.controls.layout import AuthView


class GenderSelectionView(AuthView):
    dd_gender: Dropdown

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
            title=await self.client.session.gtv(key='gender_selection'),
            controls=[
                Column(
                    controls=[
                        self.dd_gender,
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='next'),
                                size=16,
                            ),
                            on_click=partial(self.change_view, self.dd_gender.value),
                        ),
                    ],
                ),
            ],
        )

    async def change_view(self, gender, _):
        from app.views.auth.purchase import QuestionnaireView
        await self.client.change_view(QuestionnaireView(gender=gender))