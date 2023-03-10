# Generated by sila2.code_generator; sila2.__version__: 0.7.3
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

from sila2.server import FeatureImplementationBase, MetadataDict, ObservableCommandInstance

from .labwaretransfercontroller_types import (
    GetLabware_Responses,
    HandoverPosition,
    LabwareDelivered_Responses,
    LabwareRemoved_Responses,
    PositionIndex,
    PrepareForInput_Responses,
    PrepareForOutput_Responses,
    PutLabware_Responses,
)

if TYPE_CHECKING:
    from ...server import Server


class LabwareTransferControllerBase(FeatureImplementationBase, ABC):
    parent_server: Server

    def __init__(self, parent_server: Server):
        """

        The Labware Transfer Controller feature provides commands to trigger the sub tasks of handing over a labware
        item, e.g. a microtiter plate, from one device to another in a standardized and generic way.

        For each transfer a defined sequence of commands has to be called on both involved devices, to ensure the proper
        synchronization of all necessary transfer actions without unwanted physical interferences and to optimize the
        transfer performance regarding the execution time. Using the generic commands labware transfers between any
        arbitrary labware handling devices can be controlled (a robot device has not necessarily be involved).

        A labware transfer is executed between a source and a destination device, where one of them is the active device
        (executing the actual handover actions) and the other one is the passive device.

        The sequence of issued commands is as follows:

        - Prior to the actual labware transfer a PrepareForOutput command is sent to the source device to execute all
        necessary actions to be ready to release a labware item (e.g. open a tray) and simultaneously a PrepareForInput
        command is sent to the destination device to execute all necessary actions to be ready to receive a labware
        item (e.g. position the robotic arm near the tray of the source device).
        Once, both devices have successfully finished their PrepareFor.. command execution, the next commands are
        issued.
        - If the source device is the active device it will receive a PutLabware command to execute all necessary
        actions to put the labware item to the destination device. After the transfer has been finished successfully
        the destination device receives a LabwareDelivered command, that triggers all actions to be done after
        the labware item has been transferred (e.g. close the opened tray).
        - If the destination device is the active device it will receive a GetLabware command to execute all necessary
        actions to get the labware from the source device (e.g. gripping the labware item). After that command has been
        finished successfully the source device receives a LabwareRemoved command, that triggers all actions to be done
        after the labware item has been transferred (e.g. close the opened tray).

        The command sequences for the involved devices with their respective roles have always to be as follows:
        - for an active source device:      PrepareForOutput - PutLabware.
        - for a passive source device:      PrepareForOutput - LabwareRemoved.
        - for an active destination device: PrepareForInput - GetLabware.
        - for a passive destination device: PrepareForInput - LabwareDelivered.
        If the commands issued by the client differ from the respective command sequences a InvalidCommandSequence error
        will be raised.

        To address the location, where a labware item can be handed over to or from other devices, every device must
        number its positions (handover positions). A robot usually has got at least one handover position for each other
        device it is interacting with, whereas the most none-transport devices will have only one handover position.
        In case of a position array (e.g. a rack) the position within the array is specified via the sub position of the
        handover position.

        To address the positions within a device (e.g. an incubator) where the transferred labware item has to be stored
        or is to be taken from, the internal position can be specified.

        All position information will be passed to the respective commands as index numbers.

        With the PrepareForInput command also information about the labware, like labware type or a unique labware
        identifier (e.g. a barcode), is transferred.

        The IntermediateActions parameter of the PutLabware and GetLabware command can be used to specify commands
        that have to be executed while a labware item is transferred to avoid unnecessary movements,
        e.g. if a robot has to get a plate from a just opened tray and a lid has to be put on the plate before it will
        be gripped, the lid handling actions have to be included in the GetLabware actions.
        The property AvailableIntermediateActions returns a list of commands that can be included in a PutLabware or
        GetLabware command.

        """
        super().__init__(parent_server=parent_server)

    @abstractmethod
    def get_AvailableIntermediateActions(self, *, metadata: MetadataDict) -> List[str]:
        """
        Returns all commands that can be be executed within a PutLabware or GetLabware command execution.

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Returns all commands that can be be executed within a PutLabware or GetLabware command execution.
        """
        pass

    @abstractmethod
    def PrepareForInput(
        self,
        HandoverPosition: HandoverPosition,
        InternalPosition: PositionIndex,
        LabwareType: str,
        LabwareUniqueID: str,
        *,
        metadata: MetadataDict,
        instance: ObservableCommandInstance,
    ) -> PrepareForInput_Responses:
        """
        Put the device into a state where it is ready to accept new labware at the specified handover position.


        :param HandoverPosition: Indicates the position where the labware will be handed over.

        :param InternalPosition: Indicates the position where the labware will stored at inside the device, e.g. a storage position within an incubator.

        :param LabwareType: Specifies the type of the labware that will be handed over to transfer information about the labware that the device might need to access it correctly.

        :param LabwareUniqueID: The labwareUniqueID represents the unique identification of a labware in the controlling system. It is assigned by the system and stays the same for the whole process.

        :param metadata: The SiLA Client Metadata attached to the call
        :param instance: The command instance, enabling sending status updates to subscribed clients

        """
        pass

    @abstractmethod
    def PrepareForOutput(
        self,
        HandoverPosition: HandoverPosition,
        InternalPosition: PositionIndex,
        *,
        metadata: MetadataDict,
        instance: ObservableCommandInstance,
    ) -> PrepareForOutput_Responses:
        """
        Put the device into a state where it is ready to release the labware at the specified handover position.


        :param HandoverPosition: Indicates the position where the labware will be handed over.

        :param InternalPosition: Indicates the position where the labware will be retrieved from inside the device, e.g. a storage position within an incubator.

        :param metadata: The SiLA Client Metadata attached to the call
        :param instance: The command instance, enabling sending status updates to subscribed clients

        """
        pass

    @abstractmethod
    def PutLabware(
        self,
        HandoverPosition: HandoverPosition,
        LabwareType: str,
        IntermediateActions: List[str],
        *,
        metadata: MetadataDict,
        instance: ObservableCommandInstance,
    ) -> PutLabware_Responses:
        """
        Place the currently processed labware item at the specified handover position (sent to the active source device after a "PrepareForOutput" command).


        :param HandoverPosition: Indicates the position where the labware will be moved to.

        :param LabwareType: Specifies the type of the labware that will be handed over to transfer information about the labware that the device might need to access it correctly.

        :param IntermediateActions: Specifies one ore more commands that have to be executed within the command sequence (e.g. removing a lid). Each entry must be one of the commands returned by the AvailableIntermediateCommandExecutions property.

        :param metadata: The SiLA Client Metadata attached to the call
        :param instance: The command instance, enabling sending status updates to subscribed clients

        """
        pass

    @abstractmethod
    def GetLabware(
        self,
        HandoverPosition: HandoverPosition,
        LabwareType: str,
        IntermediateActions: List[str],
        *,
        metadata: MetadataDict,
        instance: ObservableCommandInstance,
    ) -> GetLabware_Responses:
        """
        Retrieve a labware item from the specified handover position (sent to the active destination device after a "PrepareForInput" command).


        :param HandoverPosition: Indicates the position where the labware will be retrieved from.

        :param LabwareType: Specifies the type of the labware that will be handed over to transfer information about the labware that the device might need to access it correctly.

        :param IntermediateActions: Specifies one ore more commands that have to be executed within the command sequence (e.g. removing a lid). Each entry must be one of the commands returned by the AvailableIntermediateCommandExecutions property.

        :param metadata: The SiLA Client Metadata attached to the call
        :param instance: The command instance, enabling sending status updates to subscribed clients

        """
        pass

    @abstractmethod
    def LabwareDelivered(
        self, HandoverPosition: HandoverPosition, *, metadata: MetadataDict, instance: ObservableCommandInstance
    ) -> LabwareDelivered_Responses:
        """
        Notifies the passive destination device of a labware item that has been transferred to it (sent after a "PrepareForInput" command).


        :param HandoverPosition: Indicates the position the labware item has been delivered to.

        :param metadata: The SiLA Client Metadata attached to the call
        :param instance: The command instance, enabling sending status updates to subscribed clients

        """
        pass

    @abstractmethod
    def LabwareRemoved(
        self, HandoverPosition: HandoverPosition, *, metadata: MetadataDict, instance: ObservableCommandInstance
    ) -> LabwareRemoved_Responses:
        """
        Notifies the passive source device of a labware item that has been removed from it (sent after a "PrepareForOutput" command).


        :param HandoverPosition: Indicates the position the labware has been removed from.

        :param metadata: The SiLA Client Metadata attached to the call
        :param instance: The command instance, enabling sending status updates to subscribed clients

        """
        pass
