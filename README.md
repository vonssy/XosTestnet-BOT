# Xos Testnet BOT
Xos Testnet BOT

- Register Here: [Xos Testnet](X.ink/P4136T)
- Connect New EVM Wallet
- Claim [Faucet](https://faucet.x.ink/)
- [XOS Dex](https://dex.x.ink/swap)

## Features

  - Auto Get Account Information
  - Auto Run With [Proxyscrape Free Proxy](https://proxyscrape.com/free-proxy-list) - `Choose 1`
  - Auto Run With Private Proxy - `Choose 2`
  - Auto Run Without Proxy - `Choose 3`
  - Auto Rotate Invalid Proxies - `y` or `n`
  - Auto Claim Check-In
  - Auto Perform Draw
  - Auto Wrap XOS to WXOS
  - Auto Unwrap WXOS to XOS
  - Auto Make Random Swap
  - Auto Add Liquidity
  - Multi Accounts

## Requiremnets

- Make sure you have Python3.9 or higher installed and pip.

## Instalation

1. **Clone The Repositories:**
   ```bash
   git clone https://github.com/vonssy/XosTestnet-BOT.git
   ```
   ```bash
   cd XosTestnet-BOT
   ```

2. **Install Requirements:**
   ```bash
   pip install -r requirements.txt #or pip3 install -r requirements.txt
   ```

### Note: Check your web3, eth-account, eth-abi, and eth-utils library version first. If not same with version in requirements.txt, u must uninstall that library.
- **Check Library Version**
  ```bash
    pip show libary_name
  ```
- **Uninstall Library**
  ```bash
    pip uninstall libary_name
  ```
- **Install Library With Version**
  ```bash
    pip install libary_name==version
  ```

## Configuration

- **accounts.txt:** You will find the file `accounts.txt` inside the project directory. Make sure `accounts.txt` contains data that matches the format expected by the script. Here are examples of file formats:
  ```bash
    your_private_key_1
    your_private_key_2
  ```

- **proxy.txt:** You will find the file `proxy.txt` inside the project directory. Make sure `proxy.txt` contains data that matches the format expected by the script. Here are examples of file formats:
  ```bash
    ip:port # Default Protcol HTTP.
    protocol://ip:port
    protocol://user:pass@ip:port
  ```

## Run

```bash
python bot.py #or python3 bot.py
```

## Buy Me a Coffee

- **EVM:** 0xe3c9ef9a39e9eb0582e5b147026cae524338521a
- **TON:** UQBEFv58DC4FUrGqinBB5PAQS7TzXSm5c1Fn6nkiet8kmehB
- **SOL:** E1xkaJYmAFEj28NPHKhjbf7GcvfdjKdvXju8d8AeSunf
- **SUI:** 0xa03726ecbbe00b31df6a61d7a59d02a7eedc39fe269532ceab97852a04cf3347

Thank you for visiting this repository, don't forget to contribute in the form of follows and stars.
If you have questions, find an issue, or have suggestions for improvement, feel free to contact me or open an *issue* in this GitHub repository.

**vonssy**