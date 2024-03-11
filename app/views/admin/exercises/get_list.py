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
from app.controls.navigation.pagination import PaginationWidget
from app.utils import Fonts
from app.utils.pagination import paginate_items, total_page
from app.views.admin.exercises.create import ExerciseCreateView
from app.views.admin.exercises.get import ExerciseView


class ExerciseListView(AdminBaseView):
    route = '/admin/exercise/list/get'
    exercises: list[dict]
    page_text: int = 1
    total_pages: int

    async def build(self):
        await self.set_type(loading=True)
        self.exercises = await self.client.session.api.client.exercises.get_list()
        await self.set_type(loading=False)

        self.total_pages = total_page(self.exercises)
        self.exercises = paginate_items(self.exercises, self.page_text)

        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_exercise_get_list_view_title'),
            on_create_click=self.create_exercise,
            main_section_controls=[
                Card(
                    controls=[
                        Text(
                            value=await self.client.session.gtv(key=exercise['name_text']),
                            size=18,
                            font_family=Fonts.SEMIBOLD,
                            color=colors.ON_PRIMARY,
                        ),
                        Text(
                            value=await self.client.session.gtv(key=exercise['type']),
                            size=10,
                            font_family=Fonts.MEDIUM,
                            color=colors.ON_PRIMARY,
                        ),
                    ],
                    on_click=partial(self.exercise_view, exercise['id']),
                )
                for exercise in self.exercises
            ] + [
                PaginationWidget(
                    current_page=self.page_text,
                    total_pages=self.total_pages,
                    on_back=self.previous_page,
                    on_next=self.next_page,
                    text_back=await self.client.session.gtv(key='back'),
                    text_next=await self.client.session.gtv(key='next'),
                ),
            ]
         )

    async def create_exercise(self, _):
        await self.client.change_view(view=ExerciseCreateView())

    async def exercise_view(self, exercise_id, _):
        await self.client.change_view(view=ExerciseView(exercise_id=exercise_id))

    async def next_page(self, _):
        if self.page_text < self.total_pages:
            self.page_text += 1
            await self.restart()

    async def previous_page(self, _):
        if self.page_text > 1:
            self.page_text -= 1
            await self.restart()
