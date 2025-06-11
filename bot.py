from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
from aiohttp_socks import ProxyConnector
from fake_useragent import FakeUserAgent
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils import to_hex
from web3 import Web3
from datetime import datetime, timedelta
from colorama import *
import asyncio, random, time, json, os, pytz

wib = pytz.timezone('Asia/Jakarta')

class XOS:
    def __init__(self) -> None:
        self.base_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "https://x.ink",
            "Referer": "https://x.ink/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": FakeUserAgent().random
        }
        self.faucet_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Origin": "https://faucet.x.ink",
            "Referer": "https://faucet.x.ink/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": FakeUserAgent().random
        }
        self.BASE_API = "https://api.x.ink/v1"
        self.FAUCET_API = "https://faucet.x.ink/api/"
        self.PAGE_URL = "https://faucet.x.ink/"
        self.SITE_KEY = "0x4AAAAAABciOCyUzm5u0xOv"
        self.REF_CODE = "1V7NKQ" # U can change it with yours.
        self.CAPTCHA_KEY = None
        self.RPC_URL = "https://testnet-rpc.x.ink/"
        self.WXOS_CONTRACT_ADDRESS = "0x0AAB67cf6F2e99847b9A95DeC950B250D648c1BB"
        self.BNB_CONTRACT_ADDRESS = "0x83DFbE02dc1B1Db11bc13a8Fc7fd011E2dBbd7c0"
        self.BONK_CONTRACT_ADDRESS = "0x00309602f7977D45322279c4dD5cf61D16FD061B"
        self.JUP_CONTRACT_ADDRESS = "0x26b597804318824a2E88Cd717376f025E6bb2219"
        self.PENGU_CONTRACT_ADDRESS = "0x9573577927d3AbECDa9C69F5E8C50bc88b1e26EE"
        self.RAY_CONTRACT_ADDRESS = "0x4A79C7Fdb6d448b3f8F643010F4CdE8b2363EFD6"
        self.SOL_CONTRACT_ADDRESS = "0x0c8a3D1fE7E40a39D3331D5Fa4B9fee1EcA1926A"
        self.TRUMP_CONTRACT_ADDRESS = "0xC09a5026d9244d482Fb913609Aeb7347B7F12800"
        self.TST_CONTRACT_ADDRESS = "0xD1194D2D06EDFBD815574383aeD6A9D76Cd568dA"
        self.USDC_CONTRACT_ADDRESS = "0xb2C1C007421f0Eb5f4B3b3F38723C309Bb208d7d"
        self.USDT_CONTRACT_ADDRESS = "0x2CCDB83a043A32898496c1030880Eb2cB977CAbc"
        self.WIF_CONTRACT_ADDRESS = "0x9c6eEc453821d12B8dfea20b6FbdDB47f7bc500d"
        self.SWAP_ROUTER_ADDRESS = "0xdc7D6b58c89A554b3FDC4B5B10De9b4DbF39FB40"
        self.ERC20_CONTRACT_ABI = json.loads('''[
            {"type":"function","name":"balanceOf","stateMutability":"view","inputs":[{"name":"address","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},
            {"type":"function","name":"allowance","stateMutability":"view","inputs":[{"name":"owner","type":"address"},{"name":"spender","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},
            {"type":"function","name":"approve","stateMutability":"nonpayable","inputs":[{"name":"spender","type":"address"},{"name":"amount","type":"uint256"}],"outputs":[{"name":"","type":"bool"}]},
            {"type":"function","name":"decimals","stateMutability":"view","inputs":[],"outputs":[{"name":"","type":"uint8"}]},
            {"type":"function","name":"deposit","stateMutability":"payable","inputs":[],"outputs":[]},
            {"type":"function","name":"withdraw","stateMutability":"nonpayable","inputs":[{"name":"wad","type":"uint256"}],"outputs":[]}
        ]''')
        self.SWAP_CONTRACT_ABI = [
            {
                "inputs": [
                    {
                        "components": [
                            { "internalType": "address", "name": "tokenIn", "type": "address" },
                            { "internalType": "address", "name": "tokenOut", "type": "address" },
                            { "internalType": "uint24", "name": "fee", "type": "uint24" },
                            { "internalType": "address", "name": "recipient", "type": "address" },
                            { "internalType": "uint256", "name": "amountIn", "type": "uint256" },
                            { "internalType": "uint256", "name": "amountOutMinimum", "type": "uint256" },
                            { "internalType": "uint160", "name": "sqrtPriceLimitX96", "type": "uint160" },
                        ],
                        "internalType": "struct IV3SwapRouter.ExactInputSingleParams",
                        "name": "params",
                        "type": "tuple",
                    },
                ],
                "name": "exactInputSingle",
                "outputs": [
                    { "internalType": "uint256", "name": "amountOut", "type": "uint256" }
                ],
                "stateMutability": "payable",
                "type": "function",
            },
            {
                "inputs": [
                    {
                        "components": [
                            { "internalType": "bytes", "name": "path", "type": "bytes" },
                            { "internalType": "address", "name": "recipient", "type": "address" },
                            { "internalType": "uint256", "name": "amountIn", "type": "uint256" },
                            { "internalType": "uint256", "name": "amountOutMinimum", "type": "uint256" },
                        ],
                        "internalType": "struct IV3SwapRouter.ExactInputParams",
                        "name": "params",
                        "type": "tuple",
                    },
                ],
                "name": "exactInput",
                "outputs": [
                    { "internalType": "uint256", "name": "amountOut", "type": "uint256" }
                ],
                "stateMutability": "payable",
                "type": "function",
            },
            {
                "inputs": [
                    { "internalType": "uint256", "name": "deadline", "type": "uint256" },
                    { "internalType": "bytes[]", "name": "data", "type": "bytes[]" } 
                ], 
                "name": "multicall", 
                "outputs": [ 
                    { "internalType": "bytes[]", "name": "", "type": "bytes[]" } 
                ],
                "stateMutability": "payable",
                "type": "function"
            },
        ]
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.tokens = {}
        self.auto_faucet = True
        self.wrap_option = None
        self.wrap_amount = 0
        self.swap_count = 0
        self.min_swap_amount = 0
        self.max_swap_amount = 0
        self.min_delay = 0
        self.max_delay = 0

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto BOT {Fore.BLUE + Style.BRIGHT}Xos Testnet
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_2captcha_key(self):
        try:
            with open("2captcha_key.txt", 'r') as file:
                captcha_key = file.read().strip()

            return captcha_key
        except Exception as e:
            return None
    
    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                async with ClientSession(timeout=ClientTimeout(total=30)) as session:
                    async with session.get("https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text") as response:
                        response.raise_for_status()
                        content = await response.text()
                        with open(filename, 'w') as f:
                            f.write(content)
                        self.proxies = [line.strip() for line in content.splitlines() if line.strip()]
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[account] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
        
    def generate_address(self, account: str):
        try:
            account = Account.from_key(account)
            address = account.address

            return address
        except Exception as e:
            return None
    
    def generate_payload(self, account: str, address: str, message: str):
        try:
            encoded_message = encode_defunct(text=message)
            signed_message = Account.sign_message(encoded_message, private_key=account)
            signature = to_hex(signed_message.signature)

            payload = {
                "walletAddress":address,
                "signMessage":message,
                "signature":signature,
                "referrer":self.REF_CODE
            }
            
            return payload
        except Exception as e:
            raise Exception(f"Generate Req Payload Failed: {str(e)}")
    
    def mask_account(self, account):
        try:
            mask_account = account[:6] + '*' * 6 + account[-6:]
            return mask_account
        except Exception as e:
            return None
        
    def generate_swap_option(self):
        swap_option = random.choice([
            "WXOStoBNB", "WXOStoBONK", "WXOStoJUP", "WXOStoPENGU", "WXOStoRAY", 
            "WXOStoSOL", "WXOStoTRUMP", "WXOStoTST", "WXOStoUSDC", "WXOStoUSDT", 
            "WXOStoWIF", "BNBtoWXOS",  "BONKtoWXOS", "JUPtoWXOS", "PENGUtoWXOS", 
            "RAYtoWXOS", "SOLtoWXOS", "TRUMPtoWXOS", "TSTtoWXOS", "USDCtoWXOS",
            "USDTtoWXOS", "WIFtoWXOS",
        ])

        from_contract_address = (
            self.BNB_CONTRACT_ADDRESS if swap_option == "BNBtoWXOS" else
            self.BONK_CONTRACT_ADDRESS if swap_option == "BONKtoWXOS" else
            self.JUP_CONTRACT_ADDRESS if swap_option == "JUPtoWXOS" else
            self.PENGU_CONTRACT_ADDRESS if swap_option == "PENGUtoWXOS" else
            self.RAY_CONTRACT_ADDRESS if swap_option == "RAYtoWXOS" else
            self.SOL_CONTRACT_ADDRESS if swap_option == "SOLtoWXOS" else
            self.TRUMP_CONTRACT_ADDRESS if swap_option == "TRUMPtoWXOS" else
            self.TST_CONTRACT_ADDRESS if swap_option == "TSTtoWXOS" else
            self.USDC_CONTRACT_ADDRESS if swap_option == "USDCtoWXOS" else
            self.USDT_CONTRACT_ADDRESS if swap_option == "USDTtoWXOS" else
            self.WIF_CONTRACT_ADDRESS if swap_option == "WIFtoWXOS" else
            self.WXOS_CONTRACT_ADDRESS
        )

        to_contract_address = (
            self.BNB_CONTRACT_ADDRESS if swap_option == "WXOStoBNB" else
            self.BONK_CONTRACT_ADDRESS if swap_option == "WXOStoBONK" else
            self.JUP_CONTRACT_ADDRESS if swap_option == "WXOStoJUP" else
            self.PENGU_CONTRACT_ADDRESS if swap_option == "WXOStoPENGU" else
            self.RAY_CONTRACT_ADDRESS if swap_option == "WXOStoRAY" else
            self.SOL_CONTRACT_ADDRESS if swap_option == "WXOStoSOL" else
            self.TRUMP_CONTRACT_ADDRESS if swap_option == "WXOStoTRUMP" else
            self.TST_CONTRACT_ADDRESS if swap_option == "WXOStoTST" else
            self.USDC_CONTRACT_ADDRESS if swap_option == "WXOStoUSDC" else
            self.USDT_CONTRACT_ADDRESS if swap_option == "WXOStoUSDT" else
            self.WIF_CONTRACT_ADDRESS if swap_option == "WXOStoWIF" else
            self.WXOS_CONTRACT_ADDRESS
        )

        from_token = (
            "BNB" if swap_option == "BNBtoWXOS" else
            "BONK" if swap_option == "BONKtoWXOS" else
            "JUP" if swap_option == "JUPtoWXOS" else
            "PENGU" if swap_option == "PENGUtoWXOS" else
            "RAY" if swap_option == "RAYtoWXOS" else
            "SOL" if swap_option == "SOLtoWXOS" else
            "TRUMP" if swap_option == "TRUMPtoWXOS" else
            "TST" if swap_option == "TSTtoWXOS" else
            "USDC" if swap_option == "USDCtoWXOS" else
            "USDT" if swap_option == "USDTtoWXOS" else
            "WIF" if swap_option == "WIFtoWXOS" else
            "WXOS"
        )

        to_token = (
            "BNB" if swap_option == "WXOStoBNB" else
            "BONK" if swap_option == "WXOStoBONK" else
            "JUP" if swap_option == "WXOStoJUP" else
            "PENGU" if swap_option == "WXOStoPENGU" else
            "RAY" if swap_option == "WXOStoRAY" else
            "SOL" if swap_option == "WXOStoSOL" else
            "TRUMP" if swap_option == "WXOStoTRUMP" else
            "TST" if swap_option == "WXOStoTST" else
            "USDC" if swap_option == "WXOStoUSDC" else
            "USDT" if swap_option == "WXOStoUSDT" else
            "WIF" if swap_option == "WXOStoWIF" else
            "WXOS"
        )

        return from_contract_address, to_contract_address, from_token, to_token
        
    async def get_web3_with_check(self, address: str, use_proxy: bool, retries=3, timeout=60):
        request_kwargs = {"timeout": timeout}

        proxy = self.get_next_proxy_for_account(address) if use_proxy else None

        if use_proxy and proxy:
            request_kwargs["proxies"] = {"http": proxy, "https": proxy}

        for attempt in range(retries):
            try:
                web3 = Web3(Web3.HTTPProvider(self.RPC_URL, request_kwargs=request_kwargs))
                web3.eth.get_block_number()
                return web3
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(3)
                    continue
                raise Exception(f"Failed to Connect to RPC: {str(e)}")
        
    async def get_token_balance(self, address: str, contract_address: str, use_proxy: str):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            if contract_address == "XOS":
                balance = web3.eth.get_balance(address)
            else:
                token_contract = web3.eth.contract(address=web3.to_checksum_address(contract_address), abi=self.ERC20_CONTRACT_ABI)
                balance = token_contract.functions.balanceOf(address).call()

            token_balance = balance / (10 ** 18)

            return token_balance
        except Exception as e:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Message :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None

    async def perform_wrap(self, account: str, address: str, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            contract_address = web3.to_checksum_address(self.WXOS_CONTRACT_ADDRESS)
            token_contract = web3.eth.contract(address=contract_address, abi=self.ERC20_CONTRACT_ABI)

            amount_to_wei = web3.to_wei(self.wrap_amount, "ether")
            wrap_data = token_contract.functions.deposit()
            estimated_gas = wrap_data.estimate_gas({"from": address, "value": amount_to_wei})

            max_priority_fee = web3.to_wei(78.75, "gwei")
            max_fee = max_priority_fee

            wrap_tx = wrap_data.build_transaction({
                "from": address,
                "value": amount_to_wei,
                "gas": int(estimated_gas * 1.2),
                "maxFeePerGas": int(max_fee),
                "maxPriorityFeePerGas": int(max_priority_fee),
                "nonce": web3.eth.get_transaction_count(address, "pending"),
                "chainId": web3.eth.chain_id,
            })

            signed_tx = web3.eth.account.sign_transaction(wrap_tx, account)
            raw_tx = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            tx_hash = web3.to_hex(raw_tx)
            receipt = await asyncio.to_thread(web3.eth.wait_for_transaction_receipt, tx_hash, timeout=300)
            block_number = receipt.blockNumber

            return tx_hash, block_number
        except Exception as e:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Message :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None, None
        
    async def perform_unwrap(self, account: str, address: str, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            contract_address = web3.to_checksum_address(self.WXOS_CONTRACT_ADDRESS)
            token_contract = web3.eth.contract(address=contract_address, abi=self.ERC20_CONTRACT_ABI)

            amount_to_wei = web3.to_wei(self.wrap_amount, "ether")
            unwrap_data = token_contract.functions.withdraw(amount_to_wei)
            estimated_gas = unwrap_data.estimate_gas({"from": address})

            max_priority_fee = web3.to_wei(78.75, "gwei")
            max_fee = max_priority_fee

            unwrap_tx = unwrap_data.build_transaction({
                "from": address,
                "gas": int(estimated_gas * 1.2),
                "maxFeePerGas": int(max_fee),
                "maxPriorityFeePerGas": int(max_priority_fee),
                "nonce": web3.eth.get_transaction_count(address, "pending"),
                "chainId": web3.eth.chain_id,
            })

            signed_tx = web3.eth.account.sign_transaction(unwrap_tx, account)
            raw_tx = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            tx_hash = web3.to_hex(raw_tx)
            receipt = await asyncio.to_thread(web3.eth.wait_for_transaction_receipt, tx_hash, timeout=300)
            block_number = receipt.blockNumber

            return tx_hash, block_number
        except Exception as e:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Message :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None, None
        
    async def approving_token(self, account: str, address: str, spender_address: str, contract_address: str, amount: float, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            spender = web3.to_checksum_address(spender_address)
            token_contract = web3.eth.contract(address=web3.to_checksum_address(contract_address), abi=self.ERC20_CONTRACT_ABI)

            amount_to_wei = web3.to_wei(amount, "ether")

            allowance = token_contract.functions.allowance(address, spender).call()
            if allowance < amount_to_wei:
                approve_data = token_contract.functions.approve(spender, 2**256 - 1)
                estimated_gas = approve_data.estimate_gas({"from": address})

                max_priority_fee = web3.to_wei(78.75, "gwei")
                max_fee = max_priority_fee

                approve_tx = approve_data.build_transaction({
                    "from": address,
                    "gas": int(estimated_gas * 1.2),
                    "maxFeePerGas": int(max_fee),
                    "maxPriorityFeePerGas": int(max_priority_fee),
                    "nonce": web3.eth.get_transaction_count(address, "pending"),
                    "chainId": web3.eth.chain_id,
                })

                signed_tx = web3.eth.account.sign_transaction(approve_tx, account)
                raw_tx = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
                tx_hash = web3.to_hex(raw_tx)
                receipt = await asyncio.to_thread(web3.eth.wait_for_transaction_receipt, tx_hash, timeout=300)
                block_number = receipt.blockNumber

                await asyncio.sleep(5)

            return True
        except Exception as e:
            raise Exception(f"Approving Token Contract Failed: {str(e)}")
        
    async def perform_swap(self, account: str, address: str, from_contract_address: str, to_contract_address: str, swap_amount: float, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            await self.approving_token(account, address, self.SWAP_ROUTER_ADDRESS, from_contract_address, swap_amount, use_proxy)

            token_contract = web3.eth.contract(address=web3.to_checksum_address(self.SWAP_ROUTER_ADDRESS), abi=self.SWAP_CONTRACT_ABI)

            params = {
                "tokenIn": web3.to_checksum_address(from_contract_address),
                "tokenOut": web3.to_checksum_address(to_contract_address),
                "fee": 500,
                "recipient": address,
                "amountIn": web3.to_wei(swap_amount, "ether"),
                "amountOutMinimum": 0,
                "sqrtPriceLimitX96": 0,
            }

            multicall = token_contract.functions.exactInputSingle(params).build_transaction({
                "from": address,
                "nonce": web3.eth.get_transaction_count(address, "pending")
            })
            
            deadline = int(time.time()) + 300

            swap_data = token_contract.functions.multicall(deadline, [multicall["data"]])

            estimated_gas = swap_data.estimate_gas({"from": address})
            max_priority_fee = web3.to_wei(78.75, "gwei")
            max_fee = max_priority_fee

            swap_tx = swap_data.build_transaction({
                "from": address,
                "gas": int(estimated_gas * 1.2),
                "maxFeePerGas": int(max_fee),
                "maxPriorityFeePerGas": int(max_priority_fee),
                "nonce": web3.eth.get_transaction_count(address, "pending"),
                "chainId": web3.eth.chain_id,
            })

            signed_tx = web3.eth.account.sign_transaction(swap_tx, account)
            raw_tx = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            tx_hash = web3.to_hex(raw_tx)
            receipt = await asyncio.to_thread(web3.eth.wait_for_transaction_receipt, tx_hash, timeout=300)
            block_number = receipt.blockNumber

            return tx_hash, block_number
        except Exception as e:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Message :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None, None
    
    async def print_timer(self):
        for remaining in range(random.randint(self.min_delay, self.max_delay), 0, -1):
            print(
                f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                f"{Fore.BLUE + Style.BRIGHT}Wait For{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {remaining} {Style.RESET_ALL}"
                f"{Fore.BLUE + Style.BRIGHT}Seconds For Next Tx...{Style.RESET_ALL}",
                end="\r",
                flush=True
            )
            await asyncio.sleep(1)

    def print_question(self):
        while True:
            try:
                print(f"{Fore.GREEN + Style.BRIGHT}Select Option:{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}1. Check-In - Draw{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Claim Faucet{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Wrap - Unwrap{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}4. Swap{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}5. Run All Features{Style.RESET_ALL}")
                option = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3/4/5] -> {Style.RESET_ALL}").strip())

                if option in [1, 2, 3, 4, 5]:
                    option_type = (
                        "Check-In - Draw" if option == 1 else 
                        "Claim Faucet" if option == 2 else 
                        "Wrap - Unwrap" if option == 3 else 
                        "Swap" if option == 4 else 
                        "Run All Features"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}{option_type} Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2, 3, 4 or 5.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2, 3, 4 or 5).{Style.RESET_ALL}")

        if option == 3:
            while True:
                try:
                    print(f"{Fore.GREEN + Style.BRIGHT}Select Option:{Style.RESET_ALL}")
                    print(f"{Fore.WHITE + Style.BRIGHT}1. Wrap XOS to WXOS{Style.RESET_ALL}")
                    print(f"{Fore.WHITE + Style.BRIGHT}2. Unwrap WXOS to XOS{Style.RESET_ALL}")
                    wrap_option = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2] -> {Style.RESET_ALL}").strip())

                    if wrap_option in [1, 2]:
                        wrap_type = (
                            "Wrap XOS to WXOS" if wrap_option == 1 else 
                            "Unwrap WXOS to XOS"
                        )
                        print(f"{Fore.GREEN + Style.BRIGHT}{wrap_type} Selected.{Style.RESET_ALL}")
                        self.wrap_option = wrap_option
                        break
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}Please enter either 1 or 2.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1 or 2).{Style.RESET_ALL}")

            while True:
                try:
                    wrap_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Enter Amount [1 or 0.01 or 0.001, etc in decimals] -> {Style.RESET_ALL}").strip())
                    if wrap_amount > 0:
                        self.wrap_amount = wrap_amount
                        break
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}Amount must be greater than 0.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a float or decimal number.{Style.RESET_ALL}")

        elif option == 4:
            while True:
                try:
                    swap_count = int(input(f"{Fore.YELLOW + Style.BRIGHT}How Many Times Do You Want To Make a Swap? -> {Style.RESET_ALL}").strip())
                    if swap_count > 0:
                        self.swap_count =swap_count
                        break
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}Please enter positive number.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

            while True:
                try:
                    min_swap_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Min Swap Amount? [1 or 0.01 or 0.001, etc in decimals]-> {Style.RESET_ALL}").strip())
                    if min_swap_amount > 0:
                        self.min_swap_amount = min_swap_amount
                        break
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}Amount must be greater than 0.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

            while True:
                try:
                    max_swap_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Max Swap Amount? [1 or 0.01 or 0.001, etc in decimals]-> {Style.RESET_ALL}").strip())
                    if max_swap_amount >= min_swap_amount:
                        self.max_swap_amount = max_swap_amount
                        break
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}Amount must be >= Min Swap Amount.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

            while True:
                try:
                    min_delay = int(input(f"{Fore.YELLOW + Style.BRIGHT}Min Delay For Each Swap Tx -> {Style.RESET_ALL}").strip())
                    if min_delay >= 0:
                        self.min_delay = min_delay
                        break
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}Min Delay must be >= 0.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

            while True:
                try:
                    max_delay = int(input(f"{Fore.YELLOW + Style.BRIGHT}Max Delay For Each Swap Tx -> {Style.RESET_ALL}").strip())
                    if max_delay >= min_delay:
                        self.max_delay = max_delay
                        break
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}Min Delay must be >= Min Delay.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

        elif option == 5:
            while True:
                auto_faucet = input(f"{Fore.YELLOW + Style.BRIGHT}Auto Claim Faucet? [y/n] -> {Style.RESET_ALL}").strip()
                if auto_faucet in ["y", "n"]:
                    if auto_faucet == "n":
                        self.auto_faucet = auto_faucet
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either y or n.{Style.RESET_ALL}")

            while True:
                try:
                    print(f"{Fore.GREEN + Style.BRIGHT}Select Option:{Style.RESET_ALL}")
                    print(f"{Fore.WHITE + Style.BRIGHT}1. Wrap XOS to WXOS{Style.RESET_ALL}")
                    print(f"{Fore.WHITE + Style.BRIGHT}2. Unwrap WXOS to XOS{Style.RESET_ALL}")
                    print(f"{Fore.WHITE + Style.BRIGHT}3. Skipped{Style.RESET_ALL}")
                    wrap_option = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                    if wrap_option in [1, 2, 3]:
                        wrap_type = (
                            "Wrap XOS to WXOS" if wrap_option == 1 else 
                            "Unwrap WXOS to XOS" if wrap_option == 1 else 
                            "Skipped"
                        )
                        print(f"{Fore.GREEN + Style.BRIGHT}{wrap_type} Selected.{Style.RESET_ALL}")
                        self.wrap_option = wrap_option
                        break
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}Please enter either 1 or 2.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1 or 2).{Style.RESET_ALL}")

            if wrap_option in [1, 2]:
                while True:
                    try:
                        wrap_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Enter Amount [1 or 0.01 or 0.001, etc in decimals] -> {Style.RESET_ALL}").strip())
                        if wrap_amount > 0:
                            self.wrap_amount = wrap_amount
                            break
                        else:
                            print(f"{Fore.RED + Style.BRIGHT}Amount must be greater than 0.{Style.RESET_ALL}")
                    except ValueError:
                        print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a float or decimal number.{Style.RESET_ALL}")

            while True:
                try:
                    swap_count = int(input(f"{Fore.YELLOW + Style.BRIGHT}How Many Times Do You Want To Make a Swap? -> {Style.RESET_ALL}").strip())
                    if swap_count > 0:
                        self.swap_count =swap_count
                        break
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}Please enter positive number.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

            while True:
                try:
                    min_swap_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Min Swap Amount? [1 or 0.01 or 0.001, etc in decimals]-> {Style.RESET_ALL}").strip())
                    if min_swap_amount > 0:
                        self.min_swap_amount = min_swap_amount
                        break
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}Amount must be greater than 0.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

            while True:
                try:
                    max_swap_amount = float(input(f"{Fore.YELLOW + Style.BRIGHT}Max Swap Amount? [1 or 0.01 or 0.001, etc in decimals]-> {Style.RESET_ALL}").strip())
                    if max_swap_amount >= min_swap_amount:
                        self.max_swap_amount = max_swap_amount
                        break
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}Amount must be >= Min Swap Amount.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

            while True:
                try:
                    min_delay = int(input(f"{Fore.YELLOW + Style.BRIGHT}Min Delay For Each Swap Tx -> {Style.RESET_ALL}").strip())
                    if min_delay >= 0:
                        self.min_delay = min_delay
                        break
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}Min Delay must be >= 0.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

            while True:
                try:
                    max_delay = int(input(f"{Fore.YELLOW + Style.BRIGHT}Max Delay For Each Swap Tx -> {Style.RESET_ALL}").strip())
                    if max_delay >= min_delay:
                        self.max_delay = max_delay
                        break
                    else:
                        print(f"{Fore.RED + Style.BRIGHT}Min Delay must be >= Min Delay.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Free Proxyscrape Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run With Private Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Run Without Proxy{Style.RESET_ALL}")
                choose = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "With Free Proxyscrape" if choose == 1 else 
                        "With Private" if choose == 2 else 
                        "Without"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Proxy Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

        rotate = False
        if choose in [1, 2]:
            while True:
                rotate = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()

                if rotate in ["y", "n"]:
                    rotate = rotate == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return option, choose, rotate
    
    async def solve_cf_turnstile(self, proxy=None, retries=5):
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:

                    if self.CAPTCHA_KEY is None:
                        return None
                    
                    url = f"http://2captcha.com/in.php?key={self.CAPTCHA_KEY}&method=turnstile&sitekey={self.SITE_KEY}&pageurl={self.PAGE_URL}"
                    async with session.get(url=url) as response:
                        response.raise_for_status()
                        result = await response.text()

                        if 'OK|' not in result:
                            await asyncio.sleep(5)
                            continue

                        request_id = result.split('|')[1]

                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}   >{Style.RESET_ALL}"
                            f"{Fore.BLUE + Style.BRIGHT} Req Id  : {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{request_id}{Style.RESET_ALL}"
                        )

                        for _ in range(30):
                            res_url = f"http://2captcha.com/res.php?key={self.CAPTCHA_KEY}&action=get&id={request_id}"
                            async with session.get(url=res_url) as res_response:
                                res_response.raise_for_status()
                                res_result = await res_response.text()

                                if 'OK|' in res_result:
                                    turnstile_token = res_result.split('|')[1]
                                    return turnstile_token
                                elif res_result == "CAPCHA_NOT_READY":
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}   >{Style.RESET_ALL}"
                                        f"{Fore.BLUE + Style.BRIGHT} Message : {Style.RESET_ALL}"
                                        f"{Fore.YELLOW + Style.BRIGHT}Captcha Not Ready{Style.RESET_ALL}"
                                    )
                                    await asyncio.sleep(5)
                                    continue
                                else:
                                    break

            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                return None

    async def get_message(self, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/get-sign-message2?walletAddress={address}"
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=self.base_headers, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Status  :{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} GET Nonce Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def verify_signature(self, account: str, address: str, message: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/verify-signature2"
        data = json.dumps(self.generate_payload(account, address, message))
        headers = {
            **self.base_headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Status  :{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Login Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def user_data(self, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/me"
        headers = {
            **self.base_headers,
            "Authorization": f"Bearer {self.tokens[address]}"
        }
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Error   :{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} GET Balance & Draw Ticket Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
            
    async def claim_checkin(self, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/check-in"
        headers = {
            **self.base_headers,
            "Authorization": f"Bearer {self.tokens[address]}",
            "Content-Length": "2",
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, json={}, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Check-In:{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Not Claimed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
            
    async def perform_draw(self, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/draw"
        headers = {
            **self.base_headers,
            "Authorization": f"Bearer {self.tokens[address]}",
            "Content-Length": "2",
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, json={}, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Draw    :{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def check_info(self, address: str, proxy=None, retries=5):
        url = f"{self.FAUCET_API}/check-info?walletAddress={address}"
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=self.faucet_headers, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Faucet  :{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Check Info Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def check_eligibility(self, address: str, proxy=None, retries=5):
        url = f"{self.FAUCET_API}/checkAddressEligibility?address={address}"
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=self.faucet_headers, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Faucet  :{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Check Eligibility Failed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
    
    async def send_token(self, address: str, turnstile_token: str, proxy=None, retries=5):
        url = f"{self.FAUCET_API}/sendToken"
        data = json.dumps({"address":address, "turnstileToken":turnstile_token, "chain":"XOS", "couponId":""})
        headers = {
            **self.faucet_headers,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Faucet  :{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Not Claimed {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )

        return None
            
    async def process_get_nonce(self, address: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None
            self.log(
                f"{Fore.CYAN + Style.BRIGHT}Proxy   :{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {proxy} {Style.RESET_ALL}"
            )

            nonce = await self.get_message(address, proxy)
            if nonce:
                message = nonce["message"]
                return message
            
            if rotate_proxy:
                proxy = self.rotate_proxy_for_account(address)
                await asyncio.sleep(5)
                continue

            return False
            
    async def process_verify_signature(self, account: str, address: str, use_proxy: bool, rotate_proxy: bool):
        message = await self.process_get_nonce(address, use_proxy, rotate_proxy)
        if message:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            verify = await self.verify_signature(account, address, message, proxy)
            if verify:
                self.tokens[address] = verify["token"]

                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Status  :{Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT} Login Success {Style.RESET_ALL}"
                )
                return True
        
            return False
        
    async def process_perform_wrap(self, account: str, address: str, use_proxy: bool):
        tx_hash, block_number = await self.perform_wrap(account, address, use_proxy)
        if tx_hash and block_number:
            explorer = f"https://testnet.xoscan.io/tx/{tx_hash}"
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Status  :{Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT} Wrap {self.wrap_amount} XOS to WXOS Success {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Block   :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {block_number} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Tx Hash :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {tx_hash} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Explorer:{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {explorer} {Style.RESET_ALL}"
            )
        else:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Status  :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Perform On-Chain Failed {Style.RESET_ALL}"
            )

    async def process_perform_unwrap(self, account: str, address: str, use_proxy: bool):
        tx_hash, block_number = await self.perform_unwrap(account, address, use_proxy)
        if tx_hash and block_number:
            explorer = f"https://testnet.xoscan.io/tx/{tx_hash}"

            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Status  :{Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT} Unwrap {self.wrap_amount} WXOS to XOS Success {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Block   :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {block_number} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Tx Hash :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {tx_hash} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Explorer:{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {explorer} {Style.RESET_ALL}"
            )
        else:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Status  :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Perform On-Chain Failed {Style.RESET_ALL}"
            )

    async def process_perform_swap(self, account: str, address: str, from_contract_address: str, to_contract_address: str, from_token: str, to_token: str, swap_amount: float, use_proxy: bool):
        tx_hash, block_number = await self.perform_swap(account, address, from_contract_address, to_contract_address, swap_amount, use_proxy)
        if tx_hash and block_number:
            explorer = f"https://testnet.xoscan.io/tx/{tx_hash}"

            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Status  :{Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT} Swap {swap_amount} {from_token} to {to_token} Success {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Block   :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {block_number} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Tx Hash :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {tx_hash} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Explorer:{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {explorer} {Style.RESET_ALL}"
            )
        else:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Status  :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Perform On-Chain Failed {Style.RESET_ALL}"
            )

    async def process_option_1(self, address: str, use_proxy: bool):
        proxy = self.get_next_proxy_for_account(address) if use_proxy else None

        user = await self.user_data(address, proxy)
        if user:
            balance = user.get("data", {}).get("points", 0)

            self.log(
                f"{Fore.CYAN + Style.BRIGHT}Balance :{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {balance} PTS {Style.RESET_ALL}"
            )

        claim = await self.claim_checkin(address, proxy)
        if claim.get("success") == True:
            days = claim['check_in_count']
            reward = claim['pointsEarned']
            self.log(
                f"{Fore.CYAN + Style.BRIGHT}Check-In:{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} Day {days} {Style.RESET_ALL}"
                f"{Fore.GREEN + Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                f"{Fore.CYAN + Style.BRIGHT}Reward{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {reward} PTS{Style.RESET_ALL}"
            )
        elif claim.get("success") == False:
            if claim.get("error") == "Already checked in today":
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Check-In:{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Already Claimed {Style.RESET_ALL}"
                )
            elif claim.get("error") == "Please follow Twitter or join Discord first":
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Check-In:{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Not Eligible, {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}Connect Your X or Discord Account First{Style.RESET_ALL}"
                )
            else:
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Check-In:{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} Unknown Error {Style.RESET_ALL}"
                )

        user = await self.user_data(address, proxy)
        if user:
            current_draw = user.get("data", {}).get("currentDraws", 0)

            if current_draw > 0:
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Draw    :{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {current_draw} {Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT}Available{Style.RESET_ALL}"
                )

                count = 0
                while current_draw > 0:
                    count += 1

                    draw = await self.perform_draw(address, proxy)
                    if draw.get("message") == "Draw successful":
                        reward = draw['pointsEarned']
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}    >{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {count} {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}Success{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}Reward{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {reward} PTS {Style.RESET_ALL}"
                        )
                    else:
                        break
            else:
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}Draw    :{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} No Available {Style.RESET_ALL}"
                )

    async def process_option_2(self, address: str, use_proxy: bool):
        if self.auto_faucet:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            check = await self.check_info(address, proxy)
            if check and check.get("success") == True:
                invite_count = check.get("invitesCount", 0)
                points = check.get("points", 0)

                if invite_count > 0 or points >= 80:
                    eligibility = await self.check_eligibility(address, proxy)
                    if not eligibility:
                        return
                    
                    can_claim = eligibility.get("canClaim")

                    if can_claim:
                        self.log(f"{Fore.CYAN + Style.BRIGHT}Faucet  :{Style.RESET_ALL}")

                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}   >{Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT} Solving Cf Turnstile... {Style.RESET_ALL}"
                        )

                        turnstile_token = await self.solve_cf_turnstile(proxy)
                        if not turnstile_token:
                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}   >{Style.RESET_ALL}"
                                f"{Fore.BLUE + Style.BRIGHT} Status  : {Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT} Cf Turnstile Not Solved {Style.RESET_ALL}"
                            )
                            return
                        
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}   >{Style.RESET_ALL}"
                            f"{Fore.BLUE + Style.BRIGHT} Message : {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT} Solving Cf Turnstile Success {Style.RESET_ALL}"
                        )
                        
                        claim = await self.send_token(address, turnstile_token, proxy)
                        if claim and claim.get("message") == "Transaction successful on XOS Testnet!":
                            tx_hash = claim.get("txHash")

                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}   >{Style.RESET_ALL}"
                                f"{Fore.BLUE + Style.BRIGHT} Status  : {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}0.2 XOS Faucet Claimed Successfully{Style.RESET_ALL}"
                            )

                            self.log(
                                f"{Fore.MAGENTA + Style.BRIGHT}   >{Style.RESET_ALL}"
                                f"{Fore.BLUE + Style.BRIGHT} Explorer: {Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT}https://testnet.xoscan.io/tx/{tx_hash}{Style.RESET_ALL}"
                            )
                        
                    else:
                        next_claim_time = eligibility.get("nextClaimTime")
                        next_claim_wib = datetime.strptime(next_claim_time, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=7)
                        formatted_time = next_claim_wib.astimezone(wib).strftime('%x %X %Z')

                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}Faucet  :{Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT} Already Claimed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT} Next Claim at: {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{formatted_time}{Style.RESET_ALL}"
                        )

                else:
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}Faucet  :{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Not Eligible, {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}Need At Least 1 Invitation or 80+ Points{Style.RESET_ALL}"
                    )

            if check and check.get("success") == False:
                error = check.get("error")

                if error == "User not found, please login at X.ink":
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}Faucet  :{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Not Eligible, {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}Login at X.ink First{Style.RESET_ALL}"
                    )
                elif error == "You need to bind Twitter & Discord first.":
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}Faucet  :{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Not Eligible, {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}Connect Your X or Discord Account First{Style.RESET_ALL}"
                    )
                else:
                    self.log(
                        f"{Fore.CYAN + Style.BRIGHT}Faucet  :{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Not Eligible {Style.RESET_ALL}"
                    )
        else:
            self.log(
                f"{Fore.CYAN + Style.BRIGHT}Faucet  :{Style.RESET_ALL}"
                f"{Fore.YELLOW + Style.BRIGHT} Skipped {Style.RESET_ALL}"
            )

    async def process_option_3(self, account: str, address: str, use_proxy: bool):
        if self.wrap_option == 1:
            self.log(f"{Fore.CYAN+Style.BRIGHT}Wrap    :{Style.RESET_ALL}                      ")

            balance = await self.get_token_balance(address, "XOS", use_proxy)
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Balance :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {balance} XOS {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Amount  :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {self.wrap_amount} XOS {Style.RESET_ALL}"
            )

            if not balance or balance <= self.wrap_amount:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Status  :{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} Insufficient XOS Token Balance {Style.RESET_ALL}"
                )
                return
            
            await self.process_perform_wrap(account, address, use_proxy)
        
        elif self.wrap_option == 2:
            self.log(f"{Fore.CYAN+Style.BRIGHT}Unwrap  :{Style.RESET_ALL}                      ")

            balance = await self.get_token_balance(address, self.WXOS_CONTRACT_ADDRESS, use_proxy)
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Balance :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {balance} WXOS {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Amount  :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {self.wrap_amount} WXOS {Style.RESET_ALL}"
            )

            if not balance or balance <= self.wrap_amount:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Status  :{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} Insufficient WXOS Token Balance {Style.RESET_ALL}"
                )
                return
            
            await self.process_perform_unwrap(account, address, use_proxy)

    async def process_option_4(self, account: str, address: str, use_proxy: bool):
        self.log(f"{Fore.CYAN+Style.BRIGHT}Swap    :{Style.RESET_ALL}                       ")

        for i in range(self.swap_count):
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}   ● {Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT}Swap{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {i+1} / {self.swap_count} {Style.RESET_ALL}                           "
            )

            from_contract_address, to_contract_address, from_token, to_token = self.generate_swap_option()

            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Type    :{Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT} {from_token} {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT} {to_token} {Style.RESET_ALL}"
            )

            swap_amount = round(random.uniform(self.min_swap_amount, self.max_swap_amount), 6)

            balance = await self.get_token_balance(address, from_contract_address, use_proxy)
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Balance :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {balance} {from_token} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Amount  :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {swap_amount} {from_token} {Style.RESET_ALL}"
            )

            if not balance or balance <= swap_amount:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Status  :{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} Insufficient {from_token} Token Balance {Style.RESET_ALL}"
                )
                continue

            await self.process_perform_swap(account, address, from_contract_address, to_contract_address, from_token, to_token, swap_amount, use_proxy)
            await self.print_timer()

    async def process_accounts(self, account: str, address, option: int, use_proxy: bool, rotate_proxy: bool):
        verifed = await self.process_verify_signature(account, address, use_proxy, rotate_proxy)
        if verifed:
            
            if option == 1:
                await self.process_option_1(address, use_proxy)

            elif option == 2:
                await self.process_option_2(address, use_proxy)

            elif option == 3:
                await self.process_option_3(account, address, use_proxy)

            elif option == 4:
                await self.process_option_4(account, address, use_proxy)

            elif option == 5:
                await self.process_option_1(address, use_proxy)
                await asyncio.sleep(5)

                await self.process_option_2(address, use_proxy)
                await asyncio.sleep(5)

                await self.process_option_3(account, address, use_proxy)
                await asyncio.sleep(5)

                await self.process_option_4(account, address, use_proxy)
                await asyncio.sleep(5)
    

    async def main(self):
        try:
            with open('accounts.txt', 'r') as file:
                accounts = [line.strip() for line in file if line.strip()]

            captcha_key = self.load_2captcha_key()
            if captcha_key:
                self.CAPTCHA_KEY = captcha_key

            option, use_proxy_choice, rotate_proxy = self.print_question()

            use_proxy = False
            if use_proxy_choice in [1, 2]:
                use_proxy = True

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
                )

                if use_proxy:
                    await self.load_proxies(use_proxy_choice)

                separator = "=" * 25
                for account in accounts:
                    if account:
                        address = self.generate_address(account)
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}{separator}[{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(address)} {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}]{separator}{Style.RESET_ALL}"
                        )

                        if not address:
                            self.log(
                                f"{Fore.CYAN + Style.BRIGHT}Status   :{Style.RESET_ALL}"
                                f"{Fore.RED + Style.BRIGHT} Invalid Private Key or Library Version Not Supported {Style.RESET_ALL}"
                            )
                            continue

                        await self.process_accounts(account, address, option, use_proxy, rotate_proxy)
                        await asyncio.sleep(3)

                self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*72)
                
                delay = 12 * 60 * 60
                while delay > 0:
                    formatted_time = self.format_seconds(delay)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.BLUE+Style.BRIGHT}All Accounts Have Been Processed...{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    await asyncio.sleep(1)
                    delay -= 1

        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'accounts.txt' Not Found.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
            raise e

if __name__ == "__main__":
    try:
        bot = XOS()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Xos Testnet - BOT{Style.RESET_ALL}                                       "                              
        )