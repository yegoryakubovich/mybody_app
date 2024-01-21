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


class AccountTrainingExerciseCreateView(AdminBaseView):
    route = '/admin/account/training/exercise/create'
    exercises: list[dict]
    dd_exercise: Dropdown
    tf_priority: TextField
    tf_value: TextField
    tf_rest: TextField

    def __init__(self, training_id):
        super().__init__()
        self.training_id = training_id

    async def build(self):
        await self.set_type(loading=True)
        self.exercises = await self.client.session.api.client.exercise.get_list()
        await self.set_type(loading=False)

        exercise_options = [
            Option(
                text=await self.client.session.gtv(key=exercise['name_text']),
                key=exercise['id']
            ) for exercise in self.exercises
        ]
        self.dd_exercise = Dropdown(
            label=await self.client.session.gtv(key='exercise'),
            value=exercise_options[0].key,
            options=exercise_options,
        )
        self.tf_priority = TextField(
            label=await self.client.session.gtv(key='priority'),
        )
        self.tf_value = TextField(
            label=await self.client.session.gtv(key='value'),
        )
        self.tf_rest = TextField(
            label=await self.client.session.gtv(key='rest'),
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_account_training_exercise_create_view_title'),
            main_section_controls=[
                self.tf_priority,
                self.tf_value,
                self.tf_rest,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='create'),
                        size=16,
                    ),
                    on_click=self.create_training_exercise,
                ),
            ]
        )

    async def create_training_exercise(self, _):
        from app.views.admin.accounts.training import AccountTrainingView
        await self.client.session.api.admin.meal.create_product(
            training_id=self.training_id,
            exercise_id=self.dd_exercise.value,
            priority=self.tf_priority.value,
            value=self.tf_value.value,
            rest=self.tf_rest.value,
        )
        await self.client.change_view(AccountTrainingView(training_id=self.training_id), delete_current=True)
