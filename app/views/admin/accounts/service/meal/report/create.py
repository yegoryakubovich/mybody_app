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


from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import AdminBaseView


class AccountMealReportCreateView(AdminBaseView):
    route = '/admin/account/meal/report/create'

    async def build(self):
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_account_meal_report_create_view_title'),
            main_section_controls=[
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='create'),
                        size=16,
                    ),
                    on_click=None,
                ),
            ]
        )