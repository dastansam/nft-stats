import eth_utils
from web3._utils.filters import construct_event_filter_params
from app.utils import format_address
from app.config import TRANSFER_TOPIC


def process_event(event):
    """
    Process an event, return arguments.
    TO-DO: Currently only decodes a Transfer event,
    should make it more generic.

    :param event: The event.
    :type event: dict
    """
    # topics contain the transactors addresses
    from_ = format_address(event['topics'][1])
    to = format_address(event['topics'][2])
    # data is hex encoded, is the amount of tokens transferred
    value = int(event['data'], 16)
    
    args = {
        'from': from_,
        'to': to,
        'value': value,
    }
    return {
        'args': args,
    }
    

def fetch_events(
    event,
    argument_filters=None,
    from_block=None,
    to_block="latest",
    address=None,
    topics=None
):
    """
    Fetch all events matching the given parameters.

    :param event: The event name.
    :type event: str
    :param argument_filters: The argument filters.
    :type argument_filters: dict
    :param from_block: The block number to start searching from.
    :type from_block: int
    :param to_block: The block number to stop searching at.
    :type to_block: int
    :param address: The contract address.
    :type address: str
    :param topics: The topics to filter by.
    :type topics: list(str)
    :return: The events.
    :rtype: list(dict)
    """
    if argument_filters is None:
        argument_filters = {}

    if address is None:
        address = event.contract_abi.address

    if topics is None:
        topics = []

    event_abi = event._get_event_abi()
    event_codec = event.web3.codec

    data_filter_set, event_filter_params = construct_event_filter_params(
        event_abi=event_abi,
        abi_codec=event_codec,
        contract_address=event.address,
        argument_filters=argument_filters,
        fromBlock=from_block,
        toBlock=to_block,
        address=address,
        topics=topics
    )
    
    events = event.web3.eth.getLogs(event_filter_params)
    
    for log in events:
        formatted_topic = eth_utils.to_bytes(log['topics'][0])
        if formatted_topic.hex() == TRANSFER_TOPIC:
            yield process_event(log)
