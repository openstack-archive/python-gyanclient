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


class Host(base.Resource):
    def __repr__(self):
        return "<Host %s>" % self._info


class HostManager(base.Manager):
    resource_class = Host

    @staticmethod
    def _path(id=None):

        if id:
            return '/v1/hosts/%s' % id
        else:
            return '/v1/hosts'

    def list_hosts(self, **kwargs):
        """Retrieve a list of Hosts.

        :returns: A list of hosts.

        """

        return self._list_pagination(self._path(''),
                                     "hosts")

    def get(self, id):
        try:
            return self._list(self._path(id))[0]
        except IndexError:
            return None
