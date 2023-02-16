# Generated by sila2.code_generator; sila2.__version__: 0.9.2
from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from sila2.server import MetadataDict

from ..generated.greetingprovider import GreetingProviderBase, SayHello_Responses

if TYPE_CHECKING:
    from ..server import Server


class GreetingProviderImpl(GreetingProviderBase):
    def __init__(self, parent_server: Server) -> None:
        super().__init__(parent_server=parent_server)
        self.__start_year = datetime.datetime.now().year

    def get_StartYear(self, *, metadata: MetadataDict) -> int:
        return self.__start_year

    def SayHello(self, Name: str, *, metadata: MetadataDict) -> SayHello_Responses:
        return SayHello_Responses(f"Hello SiLA 2 {Name}")