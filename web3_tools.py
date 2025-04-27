from dotenv import load_dotenv
from web3 import Web3
from eth_typing import Address
from web3.exceptions import InvalidAddress
from typing import Union
import os
from langchain_core.tools import tool

load_dotenv()
# Initialize Web3 with an Ethereum node (you'll need to replace this with your own node URL)
w3eth = Web3(Web3.HTTPProvider(os.getenv("ETH_MAINNET_RPC")))
w3op = Web3(Web3.HTTPProvider(os.getenv("OP_MAINNET_RPC")))
w3base = Web3(Web3.HTTPProvider(os.getenv("BASE_MAINNET_RPC")))


@tool
def get_ERC20_balance(address: str, contract_address: str, network: str) -> Union[float, None]:
    """
    Get the balance of an ERC20 token for an address

    Args:
        address (str): The wallet address to check
        contract_address (str): The ERC20 token contract address
        network (str): The network to use, available options are "eth", "op", "base"
    Returns:
        float: The token balance, or None if there was an error
    """
    if network == "eth":
        w3 = w3eth
    elif network == "op":
        w3 = w3op
    elif network == "base":
        w3 = w3base
    else:
        raise ValueError("Invalid network provided")
    try:
        # Validate addresses
        if not w3.is_address(address) or not w3.is_address(contract_address):
            raise InvalidAddress("Invalid address provided")

        # Standard ERC20 ABI for balanceOf function
        erc20_abi = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "type": "function"
            }
        ]

        # Create contract instance
        contract = w3.eth.contract(
            address=w3.to_checksum_address(contract_address), abi=erc20_abi)

        # Get balance and decimals
        balance = contract.functions.balanceOf(
            w3.to_checksum_address(address)).call()
        decimals = contract.functions.decimals().call()

        # Convert balance to decimal form
        return balance / (10 ** decimals)

    except Exception as e:
        print(f"Error getting ERC20 balance: {str(e)}")
        return None


@tool
def get_ETH_balance(address: str, network: str) -> Union[float, None]:
    """
    Get the balance of an ETH address

    Args:
        address (str): The wallet address to check
        network (str): The network to use, available options are "eth", "op", "base"
    Returns:
        float: The ETH balance in ETH (not Wei), or None if there was an error
    """
    if network == "eth":
        w3 = w3eth
    elif network == "op":
        w3 = w3op
    elif network == "base":
        w3 = w3base
    try:
        # Validate address
        if not w3.is_address(address):
            raise InvalidAddress("Invalid address provided")

        # Get balance in Wei and convert to ETH
        balance_wei = w3.eth.get_balance(w3.to_checksum_address(address))
        return w3.from_wei(balance_wei, 'ether')

    except Exception as e:
        print(f"Error getting ETH balance: {str(e)}")
        return None
