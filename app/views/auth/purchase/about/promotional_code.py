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
from app.controls.layout import AuthView
from app.utils import Fonts
from app.views.auth.purchase.about.formation_check import FormationCheckView


class PromotionalCodeView(AuthView):
    tf_promotional_code: TextField

    async def build(self):
        self.tf_promotional_code = TextField(
            label=await self.client.session.gtv(key='promotional_code'),
        )
        self.controls = await self.get_controls(
            controls=[
                Text(
                    value=await self.client.session.gtv(key='promotional_code_info'),
                    size=25,
                    font_family=Fonts.SEMIBOLD
                ),
                self.tf_promotional_code,
                FilledButton(
                    content=Text(
                        value=await self.client.session.gtv(key='next'),
                        size=16,
                    ),
                    on_click=self.change_view,
                ),
            ],
        )

    async def change_view(self, _):
        await self.set_type(loading=True)
        try:
            service_cost_id = await self.client.session.api.client.services.costs.get_list(
                service='mybody',
            )
            payment_id = await self.client.session.api.client.payments.create(
                account_service_id=self.client.session.account_service.id,
                service_cost_id=service_cost_id[0]['id'],
                payment_method=self.client.session.payment.payment_method,
                payment_method_currency_id=self.client.session.payment.payment_method_currency_id,
                promo_code=self.tf_promotional_code.value or None,
            )
            self.client.session.payment.payment_id = payment_id
            await self.set_type(loading=False)
            await self.client.change_view(view=FormationCheckView(), delete_current=True )
        except ApiException as exception:
            await self.set_type(loading=False)
            return await self.client.session.error(exception=exception)
