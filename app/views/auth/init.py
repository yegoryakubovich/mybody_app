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

from app.controls.input import Dropdown
from app.controls.layout import AuthView
from app.utils import Session
from app.utils.payment import Payment
from app.views.auth.authentication import AuthenticationView
from app.views.auth.language import LanguageView
from app.views.auth.purchase import GenderSelectionView
from app.views.auth.purchase.about import PaymentView, PurchaseFirstView
from app.views.auth.purchase.about.formation_check import FormationCheckView
from app.views.main import MainView
from config import settings


class InitView(AuthView):
    dropdown: Dropdown
    languages: list

    async def on_load(self):
        await self.set_type(loading=True)
        self.client.session = Session(client=self.client)
        await self.client.session.init()
        await self.set_type(loading=False)

        # If not language
        if not self.client.session.language:
            await self.client.change_view(view=LanguageView(), delete_current=True)
            return

        await self.client.session.get_text_pack(language=self.client.session.language)

        # If not token
        if not self.client.session.token:
            await self.client.change_view(view=AuthenticationView(), delete_current=True)
            return

        # Get account service
        account_services = await self.client.session.api.client.accounts.services.get_list()
        account_service = None
        for as_ in account_services:
            if as_.service_id == settings.service_id:
                account_service = as_

        if account_service:
            self.client.session.account_service = account_service
        else:
            await self.client.change_view(view=GenderSelectionView(), delete_current=True)
            return

        if not self.client.session.language:
            await self.client.change_view(view=LanguageView(), delete_current=True)
            return

        await self.set_type(loading=True)
        try:
            payments = await self.client.session.api.client.payments.get_list(
                account_service_id=account_service.id
            )
        except ApiException as exception:
            await self.set_type(loading=False)
            return await self.client.session.error(exception=exception)

        if not payments:
            await self.client.change_view(view=PurchaseFirstView(), delete_current=True)
            return
        else:
            for payment in payments:
                if payment.state == 'waiting':
                    self.client.session.payment = Payment()
                    self.client.session.payment.currency = payment.service_cost.currency
                    self.client.session.payment.payment_id = payment.id
                    self.client.session.payment.data = payment.data
                    await self.client.change_view(view=PaymentView(), delete_current=True)
                    return
                elif payment.state == 'creating':
                    self.client.session.payment = Payment()
                    self.client.session.payment.payment_id = payment.id
                    await self.client.change_view(view=FormationCheckView(), delete_current=True)
                    return
                elif payment.state == 'paid':
                    self.client.session.payment = {}
                    await self.client.change_view(view=MainView(), delete_current=True)
                    return
                else:
                    await self.client.change_view(view=PurchaseFirstView(), delete_current=True)
                    return

        await self.client.change_view(view=MainView())
