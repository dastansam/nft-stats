import eth_utils
from web3._utils.filters import construct_event_filter_params
from app.utils import format_address
from app.config import TRANSFER_TOPIC
import pandas as pd


def process_event(event, erc721=False):
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
    block_number = int(event['blockNumber'])
    
    if erc721:
        # tokenID is the last topic
        token_id = int(event['topics'][3].hex(), 16)
        return {
            'from': from_,
            'to': to,
            'tokenId': token_id,
            'block_number': block_number
        }

    # data is hex encoded, is the amount of tokens transferred
    value = int(event['data'], 16)
    
    return {
        'from': from_,
        'to': to,
        'value': value,
        'block_number': block_number
    }
    

def fetch_events(
    event,
    argument_filters=None,
    from_block=None,
    to_block="latest",
    address=None,
    topics=None,
    erc721=False
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
        topics = ["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"]

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
            yield process_event(log, erc721)


def update_balances(holders, events, erc721=False):
    """
    Updates the balance of a holder
    Args:
        holders ([type]): [description]
        events ([type]): [description]
    """
    if erc721:
        for index, transfer_event in events.iterrows():
            # remove tokenId from from holder if transfer_event['from']                
            holders[transfer_event['to']]['tokens'].append(transfer_event['tokenId'])
            
            initial_from_tokens = holders[transfer_event['from']]['tokens']
            filtered_from_tokens = [token for token in initial_from_tokens if token != transfer_event['tokenId']]
            holders[transfer_event['from']]['tokens'] = filtered_from_tokens
            
        return holders
                     
    for index, transfer_event in events.iterrows():
        holders[transfer_event['from']]['balance'] -= transfer_event['value']
        holders[transfer_event['to']]['balance'] += transfer_event['value']
        
    return holders


def do_record_transactions(
    address,
    web3_contract, 
    file_name, 
    initial_from_block, 
    initial_to_block,
    erc721=False
):
    """
    Records all transactions of a contract in csv file
    Infura only allows to fetch events in the span of 1000 blocks
    Therefore, we need to fetch the events in batches
    and stop the loop when we have zero events in 1000 blocks
    """
    transactions = pd.DataFrame(columns=[
        'from', 
        'to', 
        'value' 
        if not erc721 else 'tokenId',
        'block_number',
    ])
    
    events = list(fetch_events(
        web3_contract.events.Transfer, 
        from_block=initial_from_block, 
        to_block=initial_to_block,
        address=address,
        erc721=erc721)
    )
    
    transactions_count = len(events)
    print("{} events found".format(transactions_count))
    
    # add events to transactions
    transactions = transactions.append(events)
    
    initial_block_range = 5000
    
    while True:
        initial_to_block = initial_from_block + 1
        initial_from_block = initial_to_block - initial_block_range
        
        if initial_from_block < 0:
            break
        
        try:
            events = list(fetch_events(
                web3_contract.events.Transfer, 
                from_block=initial_from_block, 
                to_block=initial_to_block,
                address=address,
                erc721=erc721)
            )
            
            transactions_count = len(events)
            print('Applying {} events'.format(transactions_count))
            transactions = transactions.append(events)
            
        except Exception as e:
            print(e)
            break

        if transactions_count == 0:
            break
    
    print('Writing to file {}'.format(file_name))
    transactions.to_csv('app/data/{}.csv'.format(file_name), index=False)
