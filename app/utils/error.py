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


class Error:

    @staticmethod
    async def check_field(self, field, min_len, max_len):
        field.error_text = None
        if len(field.value) < min_len or len(field.value) > max_len:
            field.error_text = await self.client.session.gtv(key='error_count_letter')
            await self.update_async()
            return False
        return True
