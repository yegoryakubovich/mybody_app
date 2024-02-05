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


from mybody_api_client.utils import ApiException

from app.controls.button import FilledButton
from app.controls.information import Text
from app.controls.layout import AdminBaseView
from app.utils import Fonts
from app.views.admin.accounts.service.training.report.create import AccountTrainingReportCreateView


class AccountTrainingReportView(AdminBaseView):
    route = '/admin/account/training/report/get'
    tf_comment: Text
    tf_not_report: Text
    report: dict

    def __init__(self, training_report_id, training_id):
        super().__init__()
        self.training_id = training_id
        self.training_report_id = training_report_id

    async def build(self):
        await self.set_type(loading=True)
        try:
            self.report = await self.client.session.api.admin.training.get_report(
                id_=self.training_report_id,
            )
        except ApiException:
            self.report = {}
        await self.set_type(loading=False)
        if self.report:
            self.tf_comment = Text(
                value=self.report['comment'],
                size=20,
                font_family=Fonts.MEDIUM,
            )
            button = FilledButton(
                content=Text(
                    value=await self.client.session.gtv(key='delete'),
                ),
                on_click=self.delete_training_report,
            )
            on_create_click = None
            controls = [self.tf_comment, button]
        else:
            self.tf_not_report = Text(
                value=await self.client.session.gtv(key='not_report'),
                size=20,
                font_family=Fonts.MEDIUM,
            )
            on_create_click = self.create_training_report
            controls = [self.tf_not_report]

        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='report'),
            on_create_click=on_create_click,
            main_section_controls=controls,
        )

    async def delete_training_report(self, _):
        await self.client.session.api.admin.training.delete_report(
            id_=self.training_report_id,
        )
        await self.client.change_view(go_back=True, with_restart=True)

    async def create_training_report(self, _):
        await self.client.change_view(
            AccountTrainingReportCreateView(
                training_report_id=self.training_report_id,
                training_id=self.training_id,
            ),
            delete_current=True,
        )
