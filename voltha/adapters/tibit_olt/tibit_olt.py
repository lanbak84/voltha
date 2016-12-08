#
# Copyright 2016 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Tibit OLT device adapter
"""

import structlog
from zope.interface import implementer

from voltha.registry import registry
from voltha.adapters.interface import IAdapterInterface
from voltha.protos.adapter_pb2 import Adapter, AdapterConfig
from voltha.protos.device_pb2 import DeviceType, DeviceTypes
from voltha.protos.health_pb2 import HealthStatus
from voltha.protos.common_pb2 import LogLevel

log = structlog.get_logger()


@implementer(IAdapterInterface)
class TibitOltAdapter(object):

    name = 'tibit_olt'

    supported_device_types = [
        DeviceType(
            id='tibit_olt',
            adapter=name,
            accepts_bulk_flow_update=True
        )
    ]

    def __init__(self, adapter_agent, config):
        self.adapter_agent = adapter_agent
        self.config = config
        self.descriptor = Adapter(
            id=self.name,
            vendor='Tibit Communications Inc.',
            version='0.1',
            config=AdapterConfig(log_level=LogLevel.INFO)
        )
        self.interface = registry('main').get_args().interface

    def start(self):
        log.debug('starting', interface=self.interface)
        log.info('started', interface=self.interface)

    def stop(self):
        log.debug('stopping')
        log.info('stopped')

    def adapter_descriptor(self):
        return self.descriptor

    def device_types(self):
        return DeviceTypes(items=self.supported_device_types)

    def health(self):
        return HealthStatus(state=HealthStatus.HealthState.HEALTHY)

    def change_master_state(self, master):
        raise NotImplementedError()

    def adopt_device(self, device):
        log.info('adopt-device', device=device)
        return device

    def abandon_device(self, device):
        raise NotImplementedError(0
                                  )
    def deactivate_device(self, device):
        raise NotImplementedError()

    def update_flows_bulk(self, device, flows, groups):
        log.debug('bulk-flow-update', device_id=device.id,
                  flows=flows, groups=groups)

    def update_flows_incrementally(self, device, flow_changes, group_changes):
        raise NotImplementedError()

    def send_proxied_message(self, proxy_address, msg):
        log.debug('send-proxied-message',
                  proxy_address=proxy_address, msg=msg)

    def receive_proxied_message(self, proxy_address, msg):
        raise NotImplementedError()
