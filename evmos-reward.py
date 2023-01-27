import re

import requests

ADDRESS = [
    'evmos1xxxx',
    'evmos1xxxx',
    'evmos1xxxx',
    'evmos1xxxx',
]

VALOPER = [
    'evmosvaloperxxxx',
    'evmosvaloperxxxx',
]

DENOM = 1_000_000_000_000_000_000


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


def get_address_reward(account_set: list, address: str) -> float:
    for account in account_set:
        if account['address'] == address:
            return round(account['amount'] / DENOM, 2)


def get_address_valoper(account_set: list, address: str) -> str:
    for account in account_set:
        if account['address'] == address:
            return account['valoper']


def get_valoper_delegation(account_set: list, valoper: str) -> float:
    total_delegation = 0.0
    for account in account_set:
        if account['valoper'] == valoper:
            total_delegation += account['amount']

    return round(total_delegation / DENOM, 2)


if __name__ == '__main__':
    total_reward = 0.0
    total_delegation = 0.0

    account_set = get_account_set()

    for address in ADDRESS:
        if address != '' and address != 'evmos1xxxx':
            reward = get_address_reward(account_set=account_set, address=address)
            total_reward += reward
            valoper = get_address_valoper(account_set=account_set, address=address)

            print(f"address >>>> {address}.\n"
                  f"rewards >>>> {reward} $EVMOS.\n"
                  f"staked_in >> https://www.mintscan.io/evmos/validators/{valoper}.\n")

    if total_reward:
        print(f"total_reward: {total_reward} $EVMOS.\n")

    for valoper in VALOPER:
        if valoper != '' and valoper != 'evmosvaloperxxxx':
            delegation = get_valoper_delegation(account_set=account_set, valoper=valoper)
            total_delegation += delegation

            print(f"valoper: {valoper}.")
            print(f"delegation: {delegation} $EVMOS.\n")

    if total_delegation:
        print(f"total_delegation: {total_delegation} $EVMOS.\n")

    print(f"with love by @cyberomanov.\n")
