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


class CreateExerciseView(View):
    route = '/admin'
    tf_name: TextField
    dd_exercise_type: Dropdown

    async def build(self):
        self.tf_name = TextField(
            label=await self.client.session.gtv(key='name'),
        )
        exercise_type = ['time', 'quantity']
        exercise_type_options = [
            Option(
                text=exercise_type,
            ) for exercise_type in exercise_type
        ]

        self.dd_exercise_type = Dropdown(
            label=await self.client.session.gtv(key='type'),
            value=exercise_type[0],
            options=exercise_type_options,
        )

        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                            title=await self.client.session.gtv(key='create_exercise'),
                            create_button=False,
                        ),
                        self.tf_name,
                        self.dd_exercise_type,
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='create'),
                                size=16,
                            ),
                            on_click=self.create_exercise,
                        ),
                    ],
                ),
                padding=10,
            ),
        ]

    async def create_exercise(self, _):
        if len(self.tf_name.value) < 1 or len(self.tf_name.value) > 32:
            self.tf_name.error_text = await self.client.session.gtv(key='name_min_max_letter')
        else:
            await self.client.session.api.exercise.create(
                type_=self.dd_exercise_type.value,
                name=self.tf_name.value,
            )
            await self.client.change_view(go_back=True)
            await self.client.page.views[-1].restart()
