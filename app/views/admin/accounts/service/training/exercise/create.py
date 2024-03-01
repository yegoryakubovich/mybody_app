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
from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.input import TextField, Dropdown
from app.controls.layout import AdminBaseView
from app.utils import Error


class AccountTrainingExerciseCreateView(AdminBaseView):
    route = '/admin/account/training/exercise/create'
    exercises: list[dict]
    dd_exercise: Dropdown
    tf_priority: TextField
    tf_quantity: TextField
    tf_rest: TextField

    def __init__(self, training_id, exercises):
        super().__init__()
        self.exercises = exercises
        self.training_id = training_id

    async def build(self):
        await self.set_type(loading=True)
        self.exercises = await self.client.session.api.client.exercises.get_list()
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
        self.tf_priority, self.tf_quantity, self.tf_rest = [
            TextField(
                label=await self.client.session.gtv(key=key),
            )
            for key in ['priority', 'quantity', 'rest']
        ]
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_account_training_exercise_create_view_title'),
            main_section_controls=[
                self.dd_exercise,
                self.tf_priority,
                self.tf_quantity,
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
        fields = [(self.tf_priority, 1, 3, True), (self.tf_quantity, 1, 3, True), (self.tf_rest, 1, 3, True)]
        for field, min_len, max_len, check_int in fields:
            if not await Error.check_field(self, field, min_len, max_len, check_int):
                return
        if int(self.tf_priority.value) in [exercise['training_exercise']['priority'] for exercise in self.exercises]:
            self.tf_priority.error_text = await self.client.session.gtv(key='error_priority_exists')
            await self.update_async()
            return
        try:
            await self.client.session.api.admin.trainings.exercises.create(
                training_id=self.training_id,
                exercise_id=self.dd_exercise.value,
                priority=self.tf_priority.value,
                value=self.tf_quantity.value,
                rest=self.tf_rest.value,
            )
            await self.client.change_view(go_back=True, delete_current=True, with_restart=True)
        except ApiException as code:
            await self.set_type(loading=False)
            return await self.client.session.error(code=code)
