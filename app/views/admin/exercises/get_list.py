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

from flet_core import Container, Text, Column, ScrollMode

from app.controls.information.card import Card
from app.controls.layout import AdminBaseView
from app.utils import Fonts
from app.views.admin.exercises.create import CreateExerciseView
from app.views.admin.exercises.get import ExerciseView


class ExerciseListView(AdminBaseView):
    route = '/admin'
    exercises: list[dict]

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.exercise.get_list()
        self.exercises = response.exercises
        await self.set_type(loading=False)

        self.scroll = ScrollMode.AUTO
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=await self.get_controls(
                        title=await self.client.session.gtv(key='admin_exercises_list_get_view_title'),
                        on_create_click=self.create_exercise,
                        main_section_controls=[
                            Card(
                                controls=[
                                    Text(
                                        value=await self.client.session.gtv(key=exercise['name_text']),
                                        size=18,
                                        font_family=Fonts.SEMIBOLD,
                                    ),
                                    Text(
                                        value=await self.client.session.gtv(key=exercise['type']),
                                        size=10,
                                        font_family=Fonts.MEDIUM,
                                    ),
                                ],
                                on_click=functools.partial(self.exercise_view, exercise['id']),
                            )
                            for exercise in self.exercises
                        ],
                    ),
                ),
                padding=10,
            ),
        ]

    async def create_exercise(self, _):
        await self.client.change_view(view=CreateExerciseView())

    async def exercise_view(self, exercise_id, _):
        await self.client.change_view(view=ExerciseView(exercise_id=exercise_id))
