from thirdweb import ThirdwebSDK
from web3 import Web3
from config import Config
from my_simple_log import log_this

MMContractAdd = Web3.toChecksumAddress("0x436fbf52faf705b6f82404bd06fb637bc4cc44ae")

MMStakingAdd = Config.MM_STAKING_ADD
MMABI = Config.MMABI
MMSABI = Config.MMSABI

sdk = ThirdwebSDK("mainnet")
token_contract = sdk.get_contract_from_abi(MMContractAdd, MMABI)
staking_contract = sdk.get_contract_from_abi(MMStakingAdd, MMSABI)


def get_owner(mecha_id: int):
    try:
        owner_of = token_contract.call("ownerOf", mecha_id)
    except:
        log_this("get_owner exception when invoking ownerOf")
        return None
    return owner_of

def deposits_of(wallet: str):
    try:
        deposits = staking_contract.call("depositsOf", wallet)
    except:
        log_this("deposits_of exception when invoking depositsOf")
        return None
    return deposits
