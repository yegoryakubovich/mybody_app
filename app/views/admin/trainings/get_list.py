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


import functools

from flet_core import ScrollMode

from app.controls.information import Text
from app.controls.information.card import Card
from app.controls.layout import AdminBaseView
from app.utils import Fonts

from app.views.admin.trainings.create import CreateTrainingView
from app.views.admin.trainings.get import TrainingView


class TrainingListView(AdminBaseView):
    route = '/admin'
    trainings: list[dict]

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.client.training.get_list()
        self.trainings = response.trainings
        await self.set_type(loading=False)

        self.scroll = ScrollMode.AUTO
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_training_get_list_view_title'),
            on_create_click=self.create_training,
            main_section_controls=[
                Card(
                    controls=[
                        Text(
                            value=training['date'],
                            size=18,
                            font_family=Fonts.SEMIBOLD,
                        ),
                    ],
                    on_click=functools.partial(self.training_view, training['id']),
                )
                for training in self.trainings
            ],
        )

    async def create_training(self, _):
        await self.client.change_view(view=CreateTrainingView())

    async def training_view(self, text_id, _):
        await self.client.change_view(view=TrainingView(text_id=text_id))
