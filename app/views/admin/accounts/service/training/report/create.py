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
from app.controls.input import TextField
from app.controls.layout import AdminBaseView
from app.utils import Error


class AccountTrainingReportCreateView(AdminBaseView):
    route = '/admin/account/training/report/create'
    tf_comment: TextField

    def __init__(self, training_report_id, training_id):
        super().__init__()
        self.training_id = training_id
        self.training_report_id = training_report_id

    async def build(self):
        self.tf_comment = TextField(
            label=await self.client.session.gtv(key='comment'),
        )
        self.controls = await self.get_controls(
            title=await self.client.session.gtv(key='admin_account_training_report_create_view_title'),
            main_section_controls=[
                self.tf_comment,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='create'),
                        size=16,
                    ),
                    on_click=self.create_training_report,
                ),
            ]
        )

    async def create_training_report(self, _):
        from app.views.admin.accounts.service.training.report.get import AccountTrainingReportView
        fields = [(self.tf_comment, 2, 1024)]
        for field, min_len, max_len in fields:
            if not await Error.check_field(self, field, min_len=min_len, max_len=max_len):
                return
        try:
            report_id = await self.client.session.api.admin.training.create_report(
                training_id=self.training_id,
                comment=self.tf_comment.value,
            )
            await self.client.change_view(AccountTrainingReportView(
                training_id=self.training_id,
                training_report_id=report_id,
            ),
                delete_current=True,
                with_restart=True,
            )
        except ApiException as e:
            await self.set_type(loading=False)
            return await self.client.session.error(error=e)
