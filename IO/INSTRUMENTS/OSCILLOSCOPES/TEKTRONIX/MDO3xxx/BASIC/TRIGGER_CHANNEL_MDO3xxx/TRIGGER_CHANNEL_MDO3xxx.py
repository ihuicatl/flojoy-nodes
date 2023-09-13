from flojoy import flojoy, DataContainer, TextBlob
import pyvisa
from typing import Optional, Literal
from flojoy.instruments.tektronix.MDO30xx import TektronixMDO30xx


@flojoy(
    deps={
        "pyvisa": "1.13.0",
        "pyusb": "1.2.1",
        "zeroconf": "0.102.0",
        "pyvisa_py": "0.7.0",
        "qcodes": "0.39.1",
    }
)
def TRIGGER_CHANNEL_MDO3xxx(
    VISA_address: Optional[str],
    VISA_index: Optional[int] = 0,
    num_channels: int = 4,
    channel: int = 0,
    query_set: Literal["query", "set"] = "query",
    default: Optional[DataContainer] = None,
) -> Optional[DataContainer]:
    """The TRIGGER_CHANNEL_MDO3xxx node sets the triggering channel (or queries it).

    If the "VISA_address" parameter is not specified the VISA_index will be
    used to find the address. The LIST_VISA node can be used to show the
    indicies of all available VISA instruments.

    This node should also work with compatible Tektronix scopes (untested):
    MDO4xxx, MSO4xxx, and DPO4xxx.

    Parameters
    ----------
    VISA_address: str
        The VISA address to query.
    VISA_index: int
        The address will be found from LIST_VISA node list with this index.
    num_channels: int
        The number of channels on the instrument that are currently in use.
    channel: int
        The channel to set as the triggering channel (used if setting).
    query_set: str
        Whether to query or set the triggering channel.

    Returns
    -------
    DataContainer
        TextBlob: The triggering channel (e.g. CH1).
    """

    assert channel < num_channels, "Channel must be less than num_channels."

    rm = pyvisa.ResourceManager("@py")
    if VISA_address == "":
        VISA_addresses = rm.list_resources()
        VISA_address = VISA_addresses[int(VISA_index)]

    tek = TektronixMDO30xx(
        "MDO30xx",
        VISA_address,
        visalib="@py",
        device_clear=False,
        number_of_channels=num_channels,
    )

    match query_set:
        case "query":
            s = tek.trigger.source()
        case "set":
            tek.trigger.source(f"CH{1 + channel}")
            s = f"CH{1 + channel}"

    tek.close()

    return TextBlob(text_blob=s)
