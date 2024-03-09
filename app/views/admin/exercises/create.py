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


class ExerciseCreateView(AdminBaseView):
    route = '/admin/exercise/create'
    tf_name: TextField
    dd_exercise_type: Dropdown

    async def build(self):
        self.tf_name = TextField(
            label=await self.client.session.gtv(key='name'),
        )
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
            title=await self.client.session.gtv(key='admin_exercise_create_view_title'),
            main_section_controls=[
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
         )

    async def create_exercise(self, _):
        fields = [(self.tf_name, 1, 1024)]
        for field, min_len, max_len in fields:
            if not await Error.check_field(self, field, min_len=min_len, max_len=max_len):
                return

        try:
            await self.set_type(loading=True)
            await self.client.session.api.admin.exercises.create(
                type_=self.dd_exercise_type.value,
                name=self.tf_name.value,
            )
            await self.client.session.get_text_pack()
            await self.set_type(loading=False)
            await self.client.change_view(go_back=True, with_restart=True, delete_current=True)
        except ApiException as exception:
            await self.set_type(loading=False)
            return await self.client.session.error(exception=exception)
