# Generated by sila2.code_generator; sila2.__version__: 0.9.2

from typing import Optional
from uuid import UUID

from sila2.server import SilaServer

from NN_SiLA.example_server.sila2_example_server.feature_implementations.datatypeprovider_impl import DataTypeProviderImpl
from NN_SiLA.example_server.sila2_example_server.feature_implementations.delayprovider_impl import DelayProviderImpl
from NN_SiLA.example_server.sila2_example_server.feature_implementations.greetingprovider_impl import GreetingProviderImpl
from NN_SiLA.example_server.sila2_example_server.feature_implementations.timerprovider_impl import TimerProviderImpl
from NN_SiLA.example_server.sila2_example_server.generated.datatypeprovider import DataTypeProviderFeature
from NN_SiLA.example_server.sila2_example_server.generated.delayprovider import DelayProviderFeature
from NN_SiLA.example_server.sila2_example_server.generated.greetingprovider import GreetingProviderFeature
from NN_SiLA.example_server.sila2_example_server.generated.timerprovider import TimerProviderFeature

class Server(SilaServer):
    def __init__(self, server_uuid: Optional[UUID] = None):
        super().__init__(
            server_name="ExampleServer",
            server_type="ExampleServer",
            server_version="0.1",
            server_description="An example SiLA2 server",
            server_vendor_url="https://gitlab.com/SiLA2/sila_python",
            server_uuid=server_uuid,
        )

        self.datatypeprovider = DataTypeProviderImpl(self)
        self.delayprovider = DelayProviderImpl(self)
        self.greetingprovider = GreetingProviderImpl(self)
        self.timerprovider = TimerProviderImpl(self)

        self.set_feature_implementation(DataTypeProviderFeature, self.datatypeprovider)
        self.set_feature_implementation(DelayProviderFeature, self.delayprovider)
        self.set_feature_implementation(GreetingProviderFeature, self.greetingprovider)
        self.set_feature_implementation(TimerProviderFeature, self.timerprovider)
