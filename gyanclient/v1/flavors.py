#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from six.moves.urllib import parse

from gyanclient import api_versions
from gyanclient.common import base
from gyanclient.common import utils
from gyanclient import exceptions


class Flavor(base.Resource):
    def __repr__(self):
        return "<Flavor %s>" % self._info


class FlavorManager(base.Manager):
    resource_class = Flavor

    @staticmethod
    def _path(id=None):

        if id:
            return '/v1/flavors/%s' % id
        else:
            return '/v1/flavors'

    def list_flavors(self, **kwargs):
        """Retrieve a list of Flavors.

        :returns: A list of flavors.

        """

        return self._list_pagination(self._path(''),
                                     "flavors")

    def get(self, id):
        try:
            return self._list(self._path(id))[0]
        except IndexError:
            return None

    def flavor_create(self, **kwargs):
        new = {
            "python_version": kwargs["hints_data"]["python_version"],
            "cpu": kwargs["hints_data"]["cpu"],
            "memory": kwargs["hints_data"]["memory"],
            "disk": kwargs["hints_data"]["disk"],
            "driver": kwargs["hints_data"]["driver"],
            "additional_details": kwargs["hints_data"]["additional_details"]
        }
        new["name"] = kwargs["name"]
        
        return self._create(self._path(), new)

    def delete_flavor(self, id):
        return self._delete(self._path(id))
