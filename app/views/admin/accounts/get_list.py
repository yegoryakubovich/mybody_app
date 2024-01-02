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

from flet_core import Container, Row, Card, Text, Column, ScrollMode, IconButton, icons

from app.controls.button import FilledButton
from app.controls.input import TextField
from app.controls.layout import View
from app.controls.navigation.pagination import PaginationWidget
from app.utils import Fonts
from app.views.admin.accounts.get import AccountView


class AccountListView(View):
    route = '/admin'
    accounts: list[dict]
    page_account: int = 1
    total_pages: int = 1
    tf_search = TextField

    async def build(self):
        await self.set_type(loading=True)
        response = await self.client.session.api.account.search(
            page=self.page_account,
        )
        self.accounts = response.accounts
        self.total_pages = response.pages
        await self.set_type(loading=False)

        self.tf_search = TextField(
            label=await self.client.session.gtv(key='search'),
            on_change=self.search
        )

        self.scroll = ScrollMode.AUTO
        self.controls = [
            await self.get_header(),
            Container(
                content=Column(
                    controls=[
                        await self.get_title(
                            title=await self.client.session.gtv(key='admin_account_get_list_view_title'),
                        ),
                        self.tf_search,
                    ] + [
                        Card(
                            content=Container(
                                content=Column(
                                    controls=[
                                        Text(
                                            value=await self.client.session.gtv(
                                                    key=account['username']),
                                            size=18,
                                            font_family=Fonts.SEMIBOLD,
                                        ),
                                        Row(
                                            controls=[
                                                Text(
                                                    value=await self.client.session.gtv(
                                                        key=account['firstname']),
                                                    size=13,
                                                    font_family=Fonts.REGULAR,
                                                ),
                                                Text(
                                                    value=await self.client.session.gtv(
                                                        key=account['lastname']),
                                                    size=13,
                                                    font_family=Fonts.REGULAR,
                                                ),
                                            ],
                                        ),
                                        Row(),
                                    ],
                                ),
                                ink=True,
                                padding=10,
                                on_click=functools.partial(self.account_view, account['id']),
                            ),
                            margin=0,
                        )
                        for account in self.accounts
                    ] + [
                        PaginationWidget(
                            current_page=self.page_account,
                            total_pages=self.total_pages,
                            on_back=self.previous_page,
                            on_next=self.next_page,
                        ),
                    ]
                ),
                padding=10,
            ),
        ]

    async def account_view(self, account_id, _):
        await self.client.change_view(view=AccountView(account_id=account_id))

    async def search(self, _):
        response = await self.client.session.api.account.search(
            username=self.tf_search.value,
        )

    async def next_page(self, _):
        if self.page_account < self.total_pages:
            self.page_account += 1
            await self.build()
            await self.update_async()

    async def previous_page(self, _):
        if self.page_account > 1:
            self.page_account -= 1
            await self.build()
            await self.update_async()