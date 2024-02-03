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


from datetime import datetime


class Error:

    @staticmethod
    async def check_field(self, field, check_int=False, min_len=None, max_len=None,
                          error_text_key='error_count_letter'):
        field.error_text = None

        if check_int:
            if not field.value.isdigit():
                field.error_text = await self.client.session.gtv(key='error_not_int')
                await self.update_async()
                return False

        if not check_int and (min_len is not None or max_len is not None):
            if min_len is not None and len(field.value) < min_len:
                field.error_text = await self.client.session.gtv(key=error_text_key)
                await self.update_async()
                return False

            if max_len is not None and len(field.value) > max_len:
                field.error_text = await self.client.session.gtv(key=error_text_key)
                await self.update_async()
                return False

        return True

    @staticmethod
    async def check_date_format(self, field, date_format='%Y-%m-%d', error_text_key='error_invalid_date_format'):
        field.error_text = None
        try:
            datetime.strptime(field.value, date_format)
        except ValueError:
            field.error_text = await self.client.session.gtv(key=error_text_key)
            await self.update_async()
            return False
        return True
