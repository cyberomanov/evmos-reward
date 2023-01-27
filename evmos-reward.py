import re

import requests


ADDRESS = [
    'evmos1xxxx',
    'evmos1xxxx',
    'evmos1xxxx',
    'evmos1xxxx',
]


def get_account_set() -> list:
    url = "https://raw.githubusercontent.com/evmos/evmos/" \
          "828e700aab00abc1bbc2c18f330e20cf938d1f59/app/upgrades/v11/accounts.go"

    response = requests.get(url=url).content.decode('utf-8').split('\n\t\t')
    account_set = []

    for i, string in enumerate(response):
        try:
            if 'evmos' in response[i] and 'evmosval' in response[i + 2]:
                account_set.append(
                    {
                        'address': re.findall('(evmos[a-z0-9]+)', response[i])[0],
                        'amount': int(re.findall('\d+', response[i + 1])[0]),
                        'valoper': re.findall('(evmosvaloper[a-z0-9]+)', response[i + 2])[0],
                    }
                )
        except:
            pass
    return account_set


def get_reward(account_set: list, address: str) -> float:
    denom = 1_000_000_000_000_000_000
    for account in account_set:
        if account['address'] == address:
            return round(account['amount'] / denom, 2)


def get_valoper(account_set: list, address: str) -> str:
    for account in account_set:
        if account['address'] == address:
            return account['valoper']


if __name__ == '__main__':
    total_reward = 0.0

    account_set = get_account_set()

    for address in ADDRESS:
        reward = get_reward(account_set=account_set, address=address)
        total_reward += reward
        valoper = get_valoper(account_set=account_set, address=address)
        
        print(f"address >>>> {address}.\n"
              f"rewards >>>> {reward} $EVMOS.\n"
              f"staked_in >> https://www.mintscan.io/evmos/validators/{valoper}.\n")
        
    print(f"total: {total_reward} $EVMOS.\n\n"
          f"with love by @cyberomanov.\n")
