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


class ExerciseView(AdminBaseView):
    route = '/admin/exercise/get'
    exercise = dict
    dd_exercise_type: Dropdown

    def __init__(self, exercise_id):
        super().__init__()
        self.exercise_id = exercise_id

    async def build(self):
        await self.set_type(loading=True)
        self.exercise = await self.client.session.api.client.exercise.get(
            id_=self.exercise_id
        )
        await self.set_type(loading=False)

        exercise_type_dict = {
            await self.client.session.gtv(key='time'): 'time',
            await self.client.session.gtv(key='quantity'): 'quantity',
        }
        exercise_type_options = [
            Option(
                text=exercise_type,
                key=exercise_type_dict[exercise_type],
            ) for exercise_type in exercise_type_dict
        ]

        self.dd_exercise_type = Dropdown(
            label=await self.client.session.gtv(key='type'),
            value=list(exercise_type_dict.values())[0],
            options=exercise_type_options,
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key=self.exercise['name_text']),
            main_section_controls=[
                self.dd_exercise_type,
                Row(
                    controls=[
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='update'),
                            ),
                            on_click=self.update_exercise,
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='delete'),
                            ),
                            on_click=self.delete_exercise,
                        ),
                    ],
                ),
            ],
         )

    async def delete_exercise(self, _):
        await self.client.session.api.admin.exercise.delete(
            id_=self.exercise_id,
        )
        await self.client.change_view(go_back=True)

    async def update_exercise(self, _):
        await self.client.session.api.admin.exercise.update(
            id_=self.exercise_id,
            type_=self.dd_exercise_type.value,
        )
        await self.client.change_view(go_back=True)
