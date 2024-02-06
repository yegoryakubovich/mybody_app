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
from flet_core.dropdown import Option
from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.information.snackbar import SnackBar
from app.controls.input import TextField, Dropdown
from app.controls.layout import AdminBaseView


class AccountTrainingExerciseView(AdminBaseView):
    route = '/admin/account/training/exercise/get'
    exercises: list[dict]
    dd_exercise: Dropdown
    tf_priority: TextField
    tf_value: TextField
    tf_rest: TextField
    snack_bar: SnackBar

    def __init__(self, training_id, exercise):
        super().__init__()
        self.exercise = exercise
        self.training_id = training_id

    async def build(self):
        await self.set_type(loading=True)
        self.exercises = await self.client.session.api.client.exercises.get_list()
        await self.set_type(loading=False)

        self.snack_bar = SnackBar(
            content=Text(
                value=await self.client.session.gtv(key='successful'),
            ),
        )
        exercise_options = [
            Option(
                text=await self.client.session.gtv(key=exercise['name_text']),
                key=exercise['id']
            ) for exercise in self.exercises
        ]
        self.dd_exercise = Dropdown(
            label=await self.client.session.gtv(key='exercise'),
            value=self.exercise['training_exercise']['exercise'],
            options=exercise_options,
        )
        self.tf_priority = TextField(
            label=await self.client.session.gtv(key='priority'),
            value=self.exercise['training_exercise']['priority'],
        )
        self.tf_value = TextField(
            label=await self.client.session.gtv(key='value'),
            value=self.exercise['training_exercise']['value'],
        )
        self.tf_rest = TextField(
            label=await self.client.session.gtv(key='rest'),
            value=self.exercise['training_exercise']['rest'],
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_account_training_exercise_get_view_title'),
            main_section_controls=[
                self.dd_exercise,
                self.tf_priority,
                self.tf_value,
                self.tf_rest,
                self.snack_bar,
                Row(
                    controls=[
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='save'),
                            ),
                            on_click=self.update_training_exercise,
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='delete'),
                            ),
                            on_click=self.delete_training_exercise,
                        ),
                    ],
                ),
            ],
        )

    async def delete_training_exercise(self, _):
        await self.client.session.api.admin.trainings.delete_exercise(
            id_=self.exercise['training_exercise']['id'],
        )
        await self.client.change_view(go_back=True, with_restart=True)

    async def update_training_exercise(self, _):
        try:
            await self.client.session.api.admin.trainings.update_exercise(
                id_=self.exercise['training_exercise']['id'],
                exercise_id=self.dd_exercise.value,
                priority=self.tf_priority.value,
                value=self.tf_value.value,
                rest=self.tf_rest.value,
            )
            self.snack_bar.open = True
            await self.update_async()
        except ApiException as e:
            await self.set_type(loading=False)
            return await self.client.session.error(error=e)