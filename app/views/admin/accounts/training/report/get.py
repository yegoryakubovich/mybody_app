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
from mybody_api_client.utils.base_section import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.information.snackbar import SnackBar
from app.controls.input import TextField, Dropdown
from app.controls.layout import AdminBaseView


class AccountTrainingReportView(AdminBaseView):
    route = '/admin/account/training/report/get'
    tf_comment: Text
    training: dict

    def __init__(self, report_id):
        super().__init__()
        self.report_id = report_id

    async def build(self):
        await self.set_type(loading=True)
        self.training = await self.client.session.api.admin.training.get()
        await self.set_type(loading=False)

        self.tf_comment = Text(
            value=self.training['comment'],
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='report'),
            main_section_controls=[
                self.tf_comment,
                Row(
                    controls=[
                        FilledButton(
                            content=Text(
                                value=await self.client.session.gtv(key='delete'),
                            ),
                            on_click=self.delete_training_report,
                        ),
                    ],
                ),
            ],
        )

    async def delete_training_report(self, _):
        await self.client.session.api.admin.meal.delete_product(
            id_=self.report_id,
        )
        await self.client.change_view(go_back=True, with_restart=True)
