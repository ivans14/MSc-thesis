# Generated by sila2.code_generator; sila2.__version__: 0.9.2

from typing import Optional
from uuid import UUID

from sila2.server import SilaServer

from .feature_implementations.datatypeprovider_impl import DataTypeProviderImpl
from .feature_implementations.delayprovider_impl import DelayProviderImpl
from .feature_implementations.greetingprovider_impl import GreetingProviderImpl
from .feature_implementations.timerprovider_impl import TimerProviderImpl
from .generated.datatypeprovider import DataTypeProviderFeature
from .generated.delayprovider import DelayProviderFeature
from .generated.greetingprovider import GreetingProviderFeature
from .generated.timerprovider import TimerProviderFeature


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
