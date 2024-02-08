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

from flet_core import Row
from flet_core.dropdown import Dropdown
from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text, Card
from app.controls.information.snackbar import SnackBar
from app.controls.input import TextField, TextFieldDate
from app.controls.layout import AdminBaseView, Section
from app.utils import Fonts, Error
from app.views.admin.accounts.service.training.exercise.create import AccountTrainingExerciseCreateView
from app.views.admin.accounts.service.training.exercise.get import AccountTrainingExerciseView
from app.views.admin.accounts.service.training.report.get import AccountTrainingReportView


class AccountTrainingView(AdminBaseView):
    route = '/admin/account/training/get'
    training: dict
    exercise: list[dict]
    snack_bar: SnackBar
    dd_type: Dropdown
    tf_date: TextField
    dd_articles: Dropdown

    def __init__(self, training_id):
        super().__init__()
        self.training_id = training_id

    async def build(self):
        await self.set_type(loading=True)
        self.training = await self.client.session.api.admin.trainings.get(
            id_=self.training_id,
        )
        self.exercise = []
        for i, training in enumerate(self.training['exercises']):
            training_info = await self.client.session.api.client.exercises.get(id_=training['exercise'])
            # Находим соответствующий продукт в self.exercise['exercise']
            training_exercise = self.training['exercises'][i]
            if training_exercise is not None:
                training_info['training_exercise'] = training_exercise
            self.exercise.append(training_info)
        await self.set_type(loading=False)

        self.tf_date = TextFieldDate(
            label=await self.client.session.gtv(key='date'),
            value=self.training['date'],
            client=self.client,
        )
        self.snack_bar = SnackBar(
            content=Text(
                value=await self.client.session.gtv(key='successful'),
            ),
        )
        self.exercise.sort(key=lambda x: x['training_exercise']['priority'])
        self.controls = await self.get_controls(
            title=self.training['date'],
            main_section_controls=[
                self.tf_date,
                self.snack_bar,
                Row(
                    controls=[
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='save'),
                            ),
                            on_click=self.update_training,
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='delete'),
                            ),
                            on_click=self.delete_training,
                        ),
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='report'),
                            ),
                            on_click=self.view_report,
                        ),
                    ]
                )
            ],
            sections=[
                Section(
                    title=await self.client.session.gtv(key='exercises'),
                    on_create_click=self.create_training_exercise,
                    controls=[
                        Card(
                            controls=[
                                Text(
                                    value=await self.client.session.gtv(key=exercise['name_text']),
                                    size=18,
                                    font_family=Fonts.SEMIBOLD,
                                ),
                            ],
                            on_click=partial(self.exercise_view, exercise),
                        )
                        for exercise in self.exercise
                    ],
                ),
            ],
        )

    async def exercise_view(self, exercise, _):
        await self.client.change_view(
            AccountTrainingExerciseView(
                exercise=exercise,
                training_id=self.training_id,
            ),
        )

    async def view_report(self, _):
        await self.client.change_view(
            view=AccountTrainingReportView(
                training_report_id=self.training['training_report_id'],
                training_id=self.training_id,
            ),
        )

    async def delete_training(self, _):
        await self.client.session.api.admin.trainings.delete(
            id_=self.training_id,
        )
        await self.client.change_view(go_back=True, with_restart=True)

    async def create_training_exercise(self, _):
        await self.client.change_view(
            AccountTrainingExerciseCreateView(
                training_id=self.training_id,
                exercise=self.exercise,
            ),
        )

    async def update_training(self, _):
        fields = [self.tf_date]
        for field in fields:
            if not await Error.check_date_format(self, field):
                return

        try:
            update_data = {
                "id_": self.training_id,
            }
            if self.tf_date.value != self.training['date']:
                update_data.update({"date": self.tf_date.value})
            await self.client.session.api.admin.trainings.update(**update_data)
            self.snack_bar.open = True
            await self.update_async()
        except ApiException as e:
            await self.set_type(loading=False)
            return await self.client.session.error(error=e)
