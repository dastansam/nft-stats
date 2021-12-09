from web3._utils.abi import get_constructor_abi, merge_args_and_kwargs
from web3._utils.events import get_event_data
from web3._utils.filters import construct_event_filter_params
from web3._utils.contracts import encode_abi


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

    event_abi = event.get_abi()
    event_topic = event_abi['topic']

    if event_topic not in topics:
        topics.append(event_topic)

    event_filter_params = construct_event_filter_params(
        event_abi=event_abi,
        argument_filters=argument_filters,
        from_block=from_block,
        to_block=to_block,
        address=address,
        topics=topics
    )

    return event.event_contract.call().getLogs(*event_filter_params)