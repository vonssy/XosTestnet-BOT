from web3 import Web3
from web3.exceptions import TransactionNotFound
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_abi.abi import encode
from eth_utils import to_hex
from dotenv import load_dotenv
from aiohttp import ClientResponseError, ClientSession, ClientTimeout, BasicAuth
from aiohttp_socks import ProxyConnector
from fake_useragent import FakeUserAgent
from datetime import datetime
from colorama import *
import asyncio, random, time, json, re, os, pytz

load_dotenv()

wib = pytz.timezone('Asia/Jakarta')

class XOS:
    def __init__(self) -> None:
        self.BASE_API = "https://api.x.ink/v1"
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
        self.POOL_ROUTER_ADDRESS = "0x55a4669cd6895EA25C174F13E1b49d69B4481704"
        self.QUOTER_ROUTER_ADDRESS = "0xE9b889C12A10f35B1b6b37764cd939988d465B85"
        self.ERC20_CONTRACT_ABI = json.loads('''[
            {"type":"function","name":"balanceOf","stateMutability":"view","inputs":[{"name":"address","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},
            {"type":"function","name":"allowance","stateMutability":"view","inputs":[{"name":"owner","type":"address"},{"name":"spender","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},
            {"type":"function","name":"approve","stateMutability":"nonpayable","inputs":[{"name":"spender","type":"address"},{"name":"amount","type":"uint256"}],"outputs":[{"name":"","type":"bool"}]},
            {"type":"function","name":"decimals","stateMutability":"view","inputs":[],"outputs":[{"name":"","type":"uint8"}]},
            {"type":"function","name":"deposit","stateMutability":"payable","inputs":[],"outputs":[]},
            {"type":"function","name":"withdraw","stateMutability":"nonpayable","inputs":[{"name":"wad","type":"uint256"}],"outputs":[]},
            {"type":"function","name":"multicall","stateMutability":"nonpayable","inputs":[{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"outputs":[{"internalType":"bytes[]","name":"","type":"bytes[]"}]}
        ]''')
        self.QUOTER_CONTRACT_ABI = [
            {
                "type": "function",
                "name": "quoteExactInput",
                "stateMutability": "nonpayable",
                "inputs": [
                    { "internalType": "bytes", "name": "path", "type": "bytes" },
                    { "internalType": "uint256", "name": "amountIn", "type": "uint256" }
                ],
                "outputs": [
                    { "internalType": "uint256", "name": "amountOut", "type": "uint256" }
                ]
            }
        ]
        self.SWAP_CONTRACT_ABI = [
            {
                "type": "function",
                "name": "multicall",
                "stateMutability": "payable",
                "inputs": [
                    { "internalType": "uint256", "name": "deadline", "type": "uint256" }, 
                    { "internalType": "bytes[]", "name": "data", "type": "bytes[]" }
                ],
                "outputs": [
                    { "internalType": "bytes[]", "name": "", "type": "bytes[]" }
                ]
            }
        ]
        self.LIQUIDITY_CONTRACT_ABI = [
            {
                "type": "function",
                "name": "multicall",
                "stateMutability": "payable",
                "inputs": [
                    { "internalType": "bytes[]", "name": "data", "type": "bytes[]" }
                ],
                "outputs": [
                    { "internalType": "bytes[]", "name": "results", "type": "bytes[]" }
                ]
            },
            {
                "type": "function",
                "name": "mint",
                "stateMutability": "nonpayable",
                "inputs": [
                    {
                        "type": "tuple",
                        "name": "params",
                        "internalType": "struct INonfungiblePositionManager.MintParams",
                        "components": [
                            { "internalType": "address", "name": "token0", "type": "address" },
                            { "internalType": "address", "name": "token1", "type": "address" },
                            { "internalType": "uint24", "name": "fee", "type": "uint24" },
                            { "internalType": "int24", "name": "tickLower", "type": "int24" },
                            { "internalType": "int24", "name": "tickUpper", "type": "int24" },
                            { "internalType": "uint256", "name": "amount0Desired", "type": "uint256" },
                            { "internalType": "uint256", "name": "amount1Desired", "type": "uint256" },
                            { "internalType": "uint256", "name": "amount0Min", "type": "uint256" },
                            { "internalType": "uint256", "name": "amount1Min", "type": "uint256" },
                            { "internalType": "address", "name": "recipient", "type": "address" },
                            { "internalType": "uint256", "name": "deadline", "type": "uint256" }
                        ]
                    }
                ],
                "outputs": [
                    { "internalType": "uint256", "name": "tokenId", "type": "uint256" },
                    { "internalType": "uint128", "name": "liquidity", "type": "uint128" },
                    { "internalType": "uint256", "name": "amount0", "type": "uint256" },
                    { "internalType": "uint256", "name": "amount1", "type": "uint256" }
                ]
            }
        ]
        self.REF_CODE = "1V7NKQ" # U can change it with yours.
        self.HEADERS = {}
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.access_tokens = {}
        self.used_nonce = {}
        self.wrap_option = None
        self.wrap_amount = float(os.getenv("WRAP_AMOUNT"))
        self.swap_count = int(os.getenv("SWAP_COUNT"))
        self.xos_swap_amount = float(os.getenv("XOS_SWAP_AMOUNT"))
        self.wxos_swap_amount = float(os.getenv("WXOS_SWAP_AMOUNT"))
        self.bnb_swap_amount = float(os.getenv("BNB_SWAP_AMOUNT"))
        self.bonk_swap_amount = float(os.getenv("BONK_SWAP_AMOUNT"))
        self.jup_swap_amount = float(os.getenv("JUP_SWAP_AMOUNT"))
        self.pengu_swap_amount = float(os.getenv("PENGU_SWAP_AMOUNT"))
        self.ray_swap_amount = float(os.getenv("RAY_SWAP_AMOUNT"))
        self.sol_swap_amount = float(os.getenv("SOL_SWAP_AMOUNT"))
        self.trump_swap_amount = float(os.getenv("TRUMP_SWAP_AMOUNT"))
        self.tst_swap_amount = float(os.getenv("TST_SWAP_AMOUNT"))
        self.usdc_swap_amount = float(os.getenv("USDC_SWAP_AMOUNT"))
        self.usdt_swap_amount = float(os.getenv("USDT_SWAP_AMOUNT"))
        self.wif_swap_amount = float(os.getenv("WIF_SWAP_AMOUNT"))
        self.liquidity_count = int(os.getenv("LIQUIDITY_COUNT"))
        self.xos_liquidity_amount = float(os.getenv("XOS_LIQUIDITY_AMOUNT"))
        self.wxos_liquidity_amount = float(os.getenv("WXOS_LIQUIDITY_AMOUNT"))
        self.bnb_liquidity_amount = float(os.getenv("BNB_LIQUIDITY_AMOUNT"))
        self.bonk_liquidity_amount = float(os.getenv("BONK_LIQUIDITY_AMOUNT"))
        self.jup_liquidity_amount = float(os.getenv("JUP_LIQUIDITY_AMOUNT"))
        self.pengu_liquidity_amount = float(os.getenv("PENGU_LIQUIDITY_AMOUNT"))
        self.ray_liquidity_amount = float(os.getenv("RAY_LIQUIDITY_AMOUNT"))
        self.sol_liquidity_amount = float(os.getenv("SOL_LIQUIDITY_AMOUNT"))
        self.trump_liquidity_amount = float(os.getenv("TRUMP_LIQUIDITY_AMOUNT"))
        self.usdc_liquidity_amount = float(os.getenv("USDC_LIQUIDITY_AMOUNT"))
        self.usdt_liquidity_amount = float(os.getenv("USDT_LIQUIDITY_AMOUNT"))
        self.wif_liquidity_amount = float(os.getenv("WIF_LIQUIDITY_AMOUNT"))
        self.min_delay = int(os.getenv("MIN_DELAY"))
        self.max_delay = int(os.getenv("MAX_DELAY"))

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
        {Fore.GREEN + Style.BRIGHT}XOS Testnet {Fore.BLUE + Style.BRIGHT} Auto BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    async def load_proxies(self, use_proxy_choice: bool):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                async with ClientSession(timeout=ClientTimeout(total=30)) as session:
                    async with session.get("https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/all.txt") as response:
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

    def get_next_proxy_for_account(self, token):
        if token not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[token] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[token]

    def rotate_proxy_for_account(self, token):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[token] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def build_proxy_config(self, proxy=None):
        if not proxy:
            return None, None, None

        if proxy.startswith("socks"):
            connector = ProxyConnector.from_url(proxy)
            return connector, None, None

        elif proxy.startswith("http"):
            match = re.match(r"http://(.*?):(.*?)@(.*)", proxy)
            if match:
                username, password, host_port = match.groups()
                clean_url = f"http://{host_port}"
                auth = BasicAuth(username, password)
                return None, clean_url, auth
            else:
                return None, proxy, None

        raise Exception("Unsupported Proxy Type.")
        
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
        token_data = {
            "XOS": (self.WXOS_CONTRACT_ADDRESS, self.xos_swap_amount),
            "WXOS": (self.WXOS_CONTRACT_ADDRESS, self.wxos_swap_amount),
            "BNB": (self.BNB_CONTRACT_ADDRESS, self.bnb_swap_amount),
            "BONK": (self.BONK_CONTRACT_ADDRESS, self.bonk_swap_amount),
            "JUP": (self.JUP_CONTRACT_ADDRESS, self.jup_swap_amount),
            "PENGU": (self.PENGU_CONTRACT_ADDRESS, self.pengu_swap_amount),
            "RAY": (self.RAY_CONTRACT_ADDRESS, self.ray_swap_amount),
            "SOL": (self.SOL_CONTRACT_ADDRESS, self.sol_swap_amount),
            "TRUMP": (self.TRUMP_CONTRACT_ADDRESS, self.trump_swap_amount),
            "TST": (self.TST_CONTRACT_ADDRESS, self.tst_swap_amount),
            "USDC": (self.USDC_CONTRACT_ADDRESS, self.usdc_swap_amount),
            "USDT": (self.USDT_CONTRACT_ADDRESS, self.usdt_swap_amount),
            "WIF": (self.WIF_CONTRACT_ADDRESS, self.wif_swap_amount)
        }

        tickers = list(token_data.keys())

        while True:
            from_ticker = random.choice(tickers)
            to_ticker = random.choice(tickers)

            if from_ticker == to_ticker:
                continue

            if (from_ticker == "XOS" and to_ticker == "WXOS") or (from_ticker == "WXOS" and to_ticker == "XOS"):
                continue

            if from_ticker == "XOS":
                swap_type = "native to erc20"
            elif to_ticker == "XOS":
                swap_type = "erc20 to native"
            else:
                swap_type = "erc20 to erc20"

            from_token, amount_in = token_data[from_ticker]
            to_token, _ = token_data[to_ticker]

            return swap_type, from_ticker, to_ticker, from_token, to_token, amount_in
        
    def generate_liquidity_option(self):
        self.WXOS_CONTRACT_ADDRESS = "0x0AAB67cf6F2e99847b9A95DeC950B250D648c1BB"
        self.BONK_CONTRACT_ADDRESS = "0x00309602f7977D45322279c4dD5cf61D16FD061B"
        self.PENGU_CONTRACT_ADDRESS = "0x9573577927d3AbECDa9C69F5E8C50bc88b1e26EE"
        self.TST_CONTRACT_ADDRESS = "0xD1194D2D06EDFBD815574383aeD6A9D76Cd568dA"
        self.USDC_CONTRACT_ADDRESS = "0xb2C1C007421f0Eb5f4B3b3F38723C309Bb208d7d"
        self.USDT_CONTRACT_ADDRESS = "0x2CCDB83a043A32898496c1030880Eb2cB977CAbc"
        self.WIF_CONTRACT_ADDRESS = "0x9c6eEc453821d12B8dfea20b6FbdDB47f7bc500d"
        self.JUP_CONTRACT_ADDRESS = "0x26b597804318824a2E88Cd717376f025E6bb2219"
        self.RAY_CONTRACT_ADDRESS = "0x4A79C7Fdb6d448b3f8F643010F4CdE8b2363EFD6"
        self.SOL_CONTRACT_ADDRESS = "0x0c8a3D1fE7E40a39D3331D5Fa4B9fee1EcA1926A"
        self.TRUMP_CONTRACT_ADDRESS = "0xC09a5026d9244d482Fb913609Aeb7347B7F12800"
        self.BNB_CONTRACT_ADDRESS = "0x83DFbE02dc1B1Db11bc13a8Fc7fd011E2dBbd7c0"

        swap_options = [
            ("native", "XOS", "BONK", self.WXOS_CONTRACT_ADDRESS, self.BONK_CONTRACT_ADDRESS, self.xos_liquidity_amount),
            ("native", "XOS", "PENGU", self.WXOS_CONTRACT_ADDRESS, self.PENGU_CONTRACT_ADDRESS, self.xos_liquidity_amount),
            ("native", "XOS", "TST", self.WXOS_CONTRACT_ADDRESS, self.TST_CONTRACT_ADDRESS, self.xos_liquidity_amount),
            ("native", "XOS", "USDC", self.WXOS_CONTRACT_ADDRESS, self.USDC_CONTRACT_ADDRESS, self.xos_liquidity_amount),
            ("native", "XOS", "USDT", self.WXOS_CONTRACT_ADDRESS, self.USDT_CONTRACT_ADDRESS, self.xos_liquidity_amount),
            ("native", "XOS", "WIF", self.WXOS_CONTRACT_ADDRESS, self.WIF_CONTRACT_ADDRESS, self.xos_liquidity_amount),
            ("native", "XOS", "JUP", self.WXOS_CONTRACT_ADDRESS, self.JUP_CONTRACT_ADDRESS, self.xos_liquidity_amount),
            ("native", "XOS", "RAY", self.WXOS_CONTRACT_ADDRESS, self.RAY_CONTRACT_ADDRESS, self.xos_liquidity_amount),
            ("native", "XOS", "SOL", self.WXOS_CONTRACT_ADDRESS, self.SOL_CONTRACT_ADDRESS, self.xos_liquidity_amount),
            ("native", "XOS", "TRUMP", self.WXOS_CONTRACT_ADDRESS, self.TRUMP_CONTRACT_ADDRESS, self.xos_liquidity_amount),
            ("native", "XOS", "BNB", self.WXOS_CONTRACT_ADDRESS, self.BNB_CONTRACT_ADDRESS, self.xos_liquidity_amount),
            ("erc20", "WXOS", "PENGU", self.WXOS_CONTRACT_ADDRESS, self.PENGU_CONTRACT_ADDRESS, self.wxos_liquidity_amount),
            ("erc20", "WXOS", "TST", self.WXOS_CONTRACT_ADDRESS, self.TST_CONTRACT_ADDRESS, self.wxos_liquidity_amount),
            ("erc20", "WXOS", "USDC", self.WXOS_CONTRACT_ADDRESS, self.USDC_CONTRACT_ADDRESS, self.wxos_liquidity_amount),
            ("erc20", "WXOS", "USDT", self.WXOS_CONTRACT_ADDRESS, self.USDT_CONTRACT_ADDRESS, self.wxos_liquidity_amount),
            ("erc20", "WXOS", "WIF", self.WXOS_CONTRACT_ADDRESS, self.WIF_CONTRACT_ADDRESS, self.wxos_liquidity_amount),
            ("erc20", "WXOS", "JUP", self.WXOS_CONTRACT_ADDRESS, self.JUP_CONTRACT_ADDRESS, self.wxos_liquidity_amount),
            ("erc20", "WXOS", "RAY", self.WXOS_CONTRACT_ADDRESS, self.RAY_CONTRACT_ADDRESS, self.wxos_liquidity_amount),
            ("erc20", "WXOS", "SOL", self.WXOS_CONTRACT_ADDRESS, self.SOL_CONTRACT_ADDRESS, self.wxos_liquidity_amount),
            ("erc20", "WXOS", "TRUMP", self.WXOS_CONTRACT_ADDRESS, self.TRUMP_CONTRACT_ADDRESS, self.wxos_liquidity_amount),
            ("erc20", "WXOS", "BNB", self.WXOS_CONTRACT_ADDRESS, self.BNB_CONTRACT_ADDRESS, self.wxos_liquidity_amount),
            ("erc20", "BONK", "WXOS", self.BONK_CONTRACT_ADDRESS, self.WXOS_CONTRACT_ADDRESS, self.bonk_liquidity_amount),
            ("erc20", "BONK", "PENGU", self.BONK_CONTRACT_ADDRESS, self.PENGU_CONTRACT_ADDRESS, self.bonk_liquidity_amount),
            ("erc20", "BONK", "TST", self.BONK_CONTRACT_ADDRESS, self.TST_CONTRACT_ADDRESS, self.bonk_liquidity_amount),
            ("erc20", "BONK", "USDC", self.BONK_CONTRACT_ADDRESS, self.USDC_CONTRACT_ADDRESS, self.bonk_liquidity_amount),
            ("erc20", "BONK", "USDT", self.BONK_CONTRACT_ADDRESS, self.USDT_CONTRACT_ADDRESS, self.bonk_liquidity_amount),
            ("erc20", "BONK", "WIF", self.BONK_CONTRACT_ADDRESS, self.WIF_CONTRACT_ADDRESS, self.bonk_liquidity_amount),
            ("erc20", "BONK", "JUP", self.BONK_CONTRACT_ADDRESS, self.JUP_CONTRACT_ADDRESS, self.bonk_liquidity_amount),
            ("erc20", "BONK", "RAY", self.BONK_CONTRACT_ADDRESS, self.RAY_CONTRACT_ADDRESS, self.bonk_liquidity_amount),
            ("erc20", "BONK", "TRUMP", self.BONK_CONTRACT_ADDRESS, self.TRUMP_CONTRACT_ADDRESS, self.bonk_liquidity_amount),
            ("erc20", "BONK", "BNB", self.BONK_CONTRACT_ADDRESS, self.BNB_CONTRACT_ADDRESS, self.bonk_liquidity_amount),
            ("erc20", "PENGU", "TST", self.PENGU_CONTRACT_ADDRESS, self.TST_CONTRACT_ADDRESS, self.pengu_liquidity_amount),
            ("erc20", "PENGU", "USDC", self.PENGU_CONTRACT_ADDRESS, self.USDC_CONTRACT_ADDRESS, self.pengu_liquidity_amount),
            ("erc20", "PENGU", "WIF", self.PENGU_CONTRACT_ADDRESS, self.WIF_CONTRACT_ADDRESS, self.pengu_liquidity_amount),
            ("erc20", "PENGU", "TRUMP", self.PENGU_CONTRACT_ADDRESS, self.TRUMP_CONTRACT_ADDRESS, self.pengu_liquidity_amount),
            ("erc20", "USDC", "TST", self.USDC_CONTRACT_ADDRESS, self.TST_CONTRACT_ADDRESS, self.usdc_liquidity_amount),
            ("erc20", "USDC", "TRUMP", self.USDC_CONTRACT_ADDRESS, self.TRUMP_CONTRACT_ADDRESS, self.usdc_liquidity_amount),
            ("erc20", "USDT", "PENGU", self.USDT_CONTRACT_ADDRESS, self.PENGU_CONTRACT_ADDRESS, self.usdt_liquidity_amount),
            ("erc20", "USDT", "TST", self.USDT_CONTRACT_ADDRESS, self.TST_CONTRACT_ADDRESS, self.usdt_liquidity_amount),
            ("erc20", "USDT", "USDC", self.USDT_CONTRACT_ADDRESS, self.USDC_CONTRACT_ADDRESS, self.usdt_liquidity_amount),
            ("erc20", "USDT", "WIF", self.USDT_CONTRACT_ADDRESS, self.WIF_CONTRACT_ADDRESS, self.usdt_liquidity_amount),
            ("erc20", "USDT", "TRUMP", self.USDT_CONTRACT_ADDRESS, self.TRUMP_CONTRACT_ADDRESS, self.usdt_liquidity_amount),
            ("erc20", "USDT", "BNB", self.USDT_CONTRACT_ADDRESS, self.BNB_CONTRACT_ADDRESS, self.usdt_liquidity_amount),
            ("erc20", "WIF", "TST", self.WIF_CONTRACT_ADDRESS, self.TST_CONTRACT_ADDRESS, self.wif_liquidity_amount),
            ("erc20", "WIF", "USDC", self.WIF_CONTRACT_ADDRESS, self.USDC_CONTRACT_ADDRESS, self.wif_liquidity_amount),
            ("erc20", "WIF", "TRUMP", self.WIF_CONTRACT_ADDRESS, self.TRUMP_CONTRACT_ADDRESS, self.wif_liquidity_amount),
            ("erc20", "JUP", "PENGU", self.JUP_CONTRACT_ADDRESS, self.PENGU_CONTRACT_ADDRESS, self.jup_liquidity_amount),
            ("erc20", "JUP", "USDC", self.JUP_CONTRACT_ADDRESS, self.USDC_CONTRACT_ADDRESS, self.jup_liquidity_amount),
            ("erc20", "JUP", "USDT", self.JUP_CONTRACT_ADDRESS, self.USDT_CONTRACT_ADDRESS, self.jup_liquidity_amount),
            ("erc20", "JUP", "WIF", self.JUP_CONTRACT_ADDRESS, self.WIF_CONTRACT_ADDRESS, self.jup_liquidity_amount),
            ("erc20", "JUP", "RAY", self.JUP_CONTRACT_ADDRESS, self.RAY_CONTRACT_ADDRESS, self.jup_liquidity_amount),
            ("erc20", "RAY", "PENGU", self.RAY_CONTRACT_ADDRESS, self.PENGU_CONTRACT_ADDRESS, self.ray_liquidity_amount),
            ("erc20", "RAY", "TST", self.RAY_CONTRACT_ADDRESS, self.TST_CONTRACT_ADDRESS, self.ray_liquidity_amount),
            ("erc20", "RAY", "USDC", self.RAY_CONTRACT_ADDRESS, self.USDC_CONTRACT_ADDRESS, self.ray_liquidity_amount),
            ("erc20", "RAY", "BNB", self.RAY_CONTRACT_ADDRESS, self.BNB_CONTRACT_ADDRESS, self.ray_liquidity_amount),
            ("erc20", "TRUMP", "TST", self.TRUMP_CONTRACT_ADDRESS, self.TST_CONTRACT_ADDRESS, self.trump_liquidity_amount),
            ("erc20", "SOL", "PENGU", self.SOL_CONTRACT_ADDRESS, self.PENGU_CONTRACT_ADDRESS, self.sol_liquidity_amount),
            ("erc20", "SOL", "USDC", self.SOL_CONTRACT_ADDRESS, self.USDC_CONTRACT_ADDRESS, self.sol_liquidity_amount),
            ("erc20", "SOL", "USDT", self.SOL_CONTRACT_ADDRESS, self.USDT_CONTRACT_ADDRESS, self.sol_liquidity_amount),
            ("erc20", "SOL", "WIF", self.SOL_CONTRACT_ADDRESS, self.WIF_CONTRACT_ADDRESS, self.sol_liquidity_amount),
            ("erc20", "SOL", "JUP", self.SOL_CONTRACT_ADDRESS, self.JUP_CONTRACT_ADDRESS, self.sol_liquidity_amount),
            ("erc20", "SOL", "RAY", self.SOL_CONTRACT_ADDRESS, self.RAY_CONTRACT_ADDRESS, self.sol_liquidity_amount),
            ("erc20", "SOL", "TRUMP", self.SOL_CONTRACT_ADDRESS, self.TRUMP_CONTRACT_ADDRESS, self.sol_liquidity_amount),
            ("erc20", "SOL", "BNB", self.SOL_CONTRACT_ADDRESS, self.BNB_CONTRACT_ADDRESS, self.sol_liquidity_amount),
            ("erc20", "BNB", "PENGU", self.BNB_CONTRACT_ADDRESS, self.PENGU_CONTRACT_ADDRESS, self.bnb_liquidity_amount),
            ("erc20", "BNB", "TST", self.BNB_CONTRACT_ADDRESS, self.TST_CONTRACT_ADDRESS, self.bnb_liquidity_amount),
            ("erc20", "BNB", "USDC", self.BNB_CONTRACT_ADDRESS, self.USDC_CONTRACT_ADDRESS, self.bnb_liquidity_amount),
            ("erc20", "BNB", "WIF", self.BNB_CONTRACT_ADDRESS, self.WIF_CONTRACT_ADDRESS, self.bnb_liquidity_amount)
            
        ]

        token_type, ticker0, ticker1, token0, token1, amount0 = random.choice(swap_options)

        liquidity_option = f"{ticker0}/{ticker1}"

        amount0_desired = int(amount0 * (10 ** 18))

        return liquidity_option, token_type, ticker0, ticker1, token0, token1, amount0_desired
        
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
            
    async def send_raw_transaction_with_retries(self, account, web3, tx, retries=5):
        for attempt in range(retries):
            try:
                signed_tx = web3.eth.account.sign_transaction(tx, account)
                raw_tx = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
                tx_hash = web3.to_hex(raw_tx)
                return tx_hash
            except TransactionNotFound:
                pass
            except Exception as e:
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}     Message :{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} [Attempt {attempt + 1}] Send TX Error: {str(e)} {Style.RESET_ALL}"
                )
            await asyncio.sleep(2 ** attempt)
        raise Exception("Transaction Hash Not Found After Maximum Retries")

    async def wait_for_receipt_with_retries(self, web3, tx_hash, retries=5):
        for attempt in range(retries):
            try:
                receipt = await asyncio.to_thread(web3.eth.wait_for_transaction_receipt, tx_hash, timeout=300)
                return receipt
            except TransactionNotFound:
                pass
            except Exception as e:
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}     Message :{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} [Attempt {attempt + 1}] Wait for Receipt Error: {str(e)} {Style.RESET_ALL}"
                )
            await asyncio.sleep(2 ** attempt)
        raise Exception("Transaction Receipt Not Found After Maximum Retries")
        
    async def get_token_balance(self, address: str, contract_address: str, use_proxy: bool, retries=5):
        for attempt in range(retries):
            try:
                web3 = await self.get_web3_with_check(address, use_proxy)

                if contract_address == "XOS":
                    balance = web3.eth.get_balance(address)
                    decimals = 18
                else:
                    token_contract = web3.eth.contract(address=web3.to_checksum_address(contract_address), abi=self.ERC20_CONTRACT_ABI)
                    balance = token_contract.functions.balanceOf(address).call()
                    decimals = token_contract.functions.decimals().call()

                token_balance = balance / (10 ** decimals)

                return token_balance
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(3)
                    continue
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Message :{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )
                return None
            
    async def get_amount_out_min(self, address: str, path: str, amount_in_wei: int, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            contract = web3.eth.contract(address=web3.to_checksum_address(self.QUOTER_ROUTER_ADDRESS), abi=self.QUOTER_CONTRACT_ABI)

            amount_out = contract.functions.quoteExactInput(path, amount_in_wei).call()
            
            return amount_out
        except Exception as e:
            return None

    async def perform_wrap(self, account: str, address: str, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            contract_address = web3.to_checksum_address(self.WXOS_CONTRACT_ADDRESS)
            token_contract = web3.eth.contract(address=contract_address, abi=self.ERC20_CONTRACT_ABI)

            amount_to_wei = web3.to_wei(self.wrap_amount, "ether")
            wrap_data = token_contract.functions.deposit()
            estimated_gas = wrap_data.estimate_gas({"from": address, "value": amount_to_wei})

            max_priority_fee = web3.to_wei(11.25, "gwei")
            max_fee = max_priority_fee

            wrap_tx = wrap_data.build_transaction({
                "from": address,
                "value": amount_to_wei,
                "gas": int(estimated_gas * 1.2),
                "maxFeePerGas": int(max_fee),
                "maxPriorityFeePerGas": int(max_priority_fee),
                "nonce": self.used_nonce[address],
                "chainId": web3.eth.chain_id,
            })

            tx_hash = await self.send_raw_transaction_with_retries(account, web3, wrap_tx)
            receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
            block_number = receipt.blockNumber
            self.used_nonce[address] += 1

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

            max_priority_fee = web3.to_wei(11.25, "gwei")
            max_fee = max_priority_fee

            unwrap_tx = unwrap_data.build_transaction({
                "from": address,
                "gas": int(estimated_gas * 1.2),
                "maxFeePerGas": int(max_fee),
                "maxPriorityFeePerGas": int(max_priority_fee),
                "nonce": self.used_nonce[address],
                "chainId": web3.eth.chain_id,
            })

            tx_hash = await self.send_raw_transaction_with_retries(account, web3, unwrap_tx)
            receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
            block_number = receipt.blockNumber
            self.used_nonce[address] += 1

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

                max_priority_fee = web3.to_wei(11.25, "gwei")
                max_fee = max_priority_fee

                approve_tx = approve_data.build_transaction({
                    "from": address,
                    "gas": int(estimated_gas * 1.2),
                    "maxFeePerGas": int(max_fee),
                    "maxPriorityFeePerGas": int(max_priority_fee),
                    "nonce": self.used_nonce[address],
                    "chainId": web3.eth.chain_id,
                })

                tx_hash = await self.send_raw_transaction_with_retries(account, web3, approve_tx)
                receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
                block_number = receipt.blockNumber
                self.used_nonce[address] += 1

                explorer = f"https://testnet.xoscan.io/tx/{tx_hash}"
                
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Approve   :{Style.RESET_ALL}"
                    f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Block     :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {block_number} {Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Tx Hash   :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {tx_hash} {Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Explorer  :{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {explorer} {Style.RESET_ALL}"
                )
                await self.print_timer()

            return True
        except Exception as e:
            raise Exception(f"Approving Token Contract Failed: {str(e)}")
        
    def generate_multicall_bytes_data(self, address: str, swap_type: str, fee: int, from_token: str, to_token: str, amount_in_wei: int, amount_out_min_wei: int):
        try:
            if swap_type in ["native to erc20", "erc20 to erc20"]:
                exact_input_single_prefix = bytes.fromhex('04e45aaf')
                exact_input_single_bytes = encode(
                    ['address', 'address', 'uint24', 'address', 'uint256', 'uint256', 'uint160'],
                    [
                        from_token,
                        to_token,
                        fee,
                        address,
                        amount_in_wei,
                        amount_out_min_wei,
                        0
                    ]
                )
                
                data_bytes = [exact_input_single_prefix + exact_input_single_bytes]

            elif swap_type == "erc20 to native":
                exact_input_single_prefix = bytes.fromhex('04e45aaf')
                exact_input_single_bytes = encode(
                    ['address', 'address', 'uint24', 'address', 'uint256', 'uint256', 'uint160'],
                    [
                        from_token,
                        to_token,
                        fee,
                        "0x0000000000000000000000000000000000000002",
                        amount_in_wei,
                        amount_out_min_wei,
                        0
                    ]
                )

                unwrap_weth_9_prefix = bytes.fromhex('49404b7c')
                unwrap_weth_9_bytes = encode(
                    ['uint256', 'address'],
                    [
                        amount_out_min_wei,
                        address
                    ]
                )
                
                data_bytes = [exact_input_single_prefix + exact_input_single_bytes, unwrap_weth_9_prefix + unwrap_weth_9_bytes ]

            return data_bytes
        except Exception as e:
            raise Exception(f"Generate Multicall Bytes Data Failed: {str(e)}")
        
    async def perform_swap(self, account: str, address: str, swap_type: str, from_token: str, to_token: str, amount_in: float, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            amount_in_wei = web3.to_wei(amount_in, "ether")

            fee = 100 if swap_type == "erc20 to native" else 500

            if swap_type != "native to erc20":
                await self.approving_token(account, address, self.SWAP_ROUTER_ADDRESS, from_token, amount_in_wei, use_proxy)

            path = bytes.fromhex(from_token[2:]) + (fee).to_bytes(3, "big") + bytes.fromhex(to_token[2:])

            amount_out_wei = await self.get_amount_out_min(address, path, amount_in_wei, use_proxy)
            if not amount_out_wei:
                raise Exception("Fetch Amount Out Min Failed")
            
            amount_out_min_wei = (amount_out_wei * (10000 - 50)) // 10000

            deadline = int(time.time()) + 600

            data_bytes = self.generate_multicall_bytes_data(address, swap_type, fee, from_token, to_token, amount_in_wei, amount_out_min_wei)

            max_priority_fee = web3.to_wei(11.25, "gwei")
            max_fee = max_priority_fee

            if swap_type == "native to erc20":
                token_contract = web3.eth.contract(address=web3.to_checksum_address(self.SWAP_ROUTER_ADDRESS), abi=self.SWAP_CONTRACT_ABI)
                swap_data = token_contract.functions.multicall(deadline, data_bytes)
                estimated_gas = swap_data.estimate_gas({"from": address, "value":amount_in_wei})
                swap_tx = swap_data.build_transaction({
                    "from": address,
                    "value": amount_in_wei,
                    "gas": int(estimated_gas * 1.2),
                    "maxFeePerGas": int(max_fee),
                    "maxPriorityFeePerGas": int(max_priority_fee),
                    "nonce": self.used_nonce[address],
                    "chainId": web3.eth.chain_id
                })

            else:
                token_contract = web3.eth.contract(address=web3.to_checksum_address(self.SWAP_ROUTER_ADDRESS), abi=self.ERC20_CONTRACT_ABI)
                swap_data = token_contract.functions.multicall(deadline, data_bytes)
                estimated_gas = swap_data.estimate_gas({"from": address})
                swap_tx = swap_data.build_transaction({
                    "from": address,
                    "gas": int(estimated_gas * 1.2),
                    "maxFeePerGas": int(max_fee),
                    "maxPriorityFeePerGas": int(max_priority_fee),
                    "nonce": self.used_nonce[address],
                    "chainId": web3.eth.chain_id
                })

            tx_hash = await self.send_raw_transaction_with_retries(account, web3, swap_tx)
            receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
            block_number = receipt.blockNumber
            self.used_nonce[address] += 1

            return tx_hash, block_number
        except Exception as e:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Message :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None, None
        
    def generate_liquidity_calldata(self, address: str, token_type: str, token0: str, token1: str, amount0_desired: int, amount1_desired: int):
        try:
            amount0_min = (amount0_desired * (10000 - 100)) // 10000
            amount1_min = (amount1_desired * (10000 - 100)) // 10000
            deadline = int(time.time()) + 600

            if token_type == "native":
                mint_prefix = bytes.fromhex("88316456")
                mint_params = encode(
                    [
                        'address', 'address', 'uint24', 'int24', 'int24', 'uint256', 
                        'uint256', 'uint256', 'uint256', 'address', 'uint256'
                    ],
                    [
                        token0, token1, 500, -887220, 887220, amount0_desired,
                        amount1_desired, amount0_min, amount1_min, address, deadline
                    ]
                )
                refund_eth_prefix = bytes.fromhex("12210e8a")

                calldata = [mint_prefix + mint_params, refund_eth_prefix]

            elif token_type == "erc20":
                calldata = (
                    token0, token1, 500, -887220, 887220, amount0_desired, 
                    amount1_desired, amount0_min, amount1_min, address, deadline
                )

            return calldata
        except Exception as e:
            raise Exception(f"Generate Liquidity Calldata Failed: {str(e)}")
        
    async def perform_liquidity(self, account: str, address: str, token_type: str, token0: str, token1: str, amount0_desired: int, amount1_desired: int, use_proxy: bool):
        try:
            web3 = await self.get_web3_with_check(address, use_proxy)

            if token_type == "erc20":
                await self.approving_token(account, address, self.POOL_ROUTER_ADDRESS, token0, amount0_desired, use_proxy)
            
            await self.approving_token(account, address, self.POOL_ROUTER_ADDRESS, token1, amount1_desired, use_proxy)

            token_contract = web3.eth.contract(address=web3.to_checksum_address(self.POOL_ROUTER_ADDRESS), abi=self.LIQUIDITY_CONTRACT_ABI)

            calldata = self.generate_liquidity_calldata(address, token_type, token0, token1, amount0_desired, amount1_desired)

            max_priority_fee = web3.to_wei(11.25, "gwei")
            max_fee = max_priority_fee

            if token_type == "native":
                liquidity_data = token_contract.functions.multicall(calldata)
                estimated_gas = liquidity_data.estimate_gas({"from": address, "value":amount1_desired})
                liquidity_tx = liquidity_data.build_transaction({
                    "from": address,
                    "value": amount1_desired,
                    "gas": int(estimated_gas * 1.2),
                    "maxFeePerGas": int(max_fee),
                    "maxPriorityFeePerGas": int(max_priority_fee),
                    "nonce": self.used_nonce[address],
                    "chainId": web3.eth.chain_id
                })

            elif token_type == "erc20":
                liquidity_data = token_contract.functions.mint(calldata)
                estimated_gas = liquidity_data.estimate_gas({"from": address})
                liquidity_tx = liquidity_data.build_transaction({
                    "from": address,
                    "gas": int(estimated_gas * 1.2),
                    "maxFeePerGas": int(max_fee),
                    "maxPriorityFeePerGas": int(max_priority_fee),
                    "nonce": self.used_nonce[address],
                    "chainId": web3.eth.chain_id
                })

            tx_hash = await self.send_raw_transaction_with_retries(account, web3, liquidity_tx)
            receipt = await self.wait_for_receipt_with_retries(web3, tx_hash)
            block_number = receipt.blockNumber
            self.used_nonce[address] += 1

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

    def print_wrap_option_question(self):
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
                        "Unwrap WXOS to XOS" if wrap_option == 2 else 
                        "Skipped"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}{wrap_type} Selected.{Style.RESET_ALL}")
                    self.wrap_option = wrap_option
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

    def print_question(self):
        while True:
            try:
                print(f"{Fore.GREEN + Style.BRIGHT}Select Option:{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}1. Check-In - Draw{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Wrap XOS to WXOS{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Unwrap WXOS to XOS{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}4. Random Swap{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}5. Add Liquidity{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}6. Run All Features{Style.RESET_ALL}")
                option = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3/4/5] -> {Style.RESET_ALL}").strip())

                if option in [1, 2, 3, 4, 5, 6]:
                    option_type = (
                        "Check-In - Draw" if option == 1 else 
                        "Wrap XOS to WXOS" if option == 2 else 
                        "Unwrap WXOS to XOS" if option == 3 else 
                        "Random Swap" if option == 4 else 
                        "Add Liquidity" if option == 5 else 
                        "Run All Features"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}{option_type} Selected.{Style.RESET_ALL}")
                    if option == 6:
                        self.print_wrap_option_question()
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2, 3, 4, 5 or 6.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2, 3, 4, 5 or 6).{Style.RESET_ALL}")
            
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
    
    async def check_connection(self, proxy_url=None):
        connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=10)) as session:
                async with session.get(url="https://api.ipify.org?format=json", proxy=proxy, proxy_auth=proxy_auth) as response:
                    response.raise_for_status()
                    return True
        except (Exception, ClientResponseError) as e:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Status  :{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Connection Not 200 OK {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
            )
            return None

    async def get_message(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/get-sign-message2?walletAddress={address}"
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=self.HEADERS[address], proxy=proxy, proxy_auth=proxy_auth) as response:
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
    
    async def verify_signature(self, account: str, address: str, message: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/verify-signature2"
        data = json.dumps(self.generate_payload(account, address, message))
        headers = {
            **self.HEADERS[address],
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
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
    
    async def user_data(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/me"
        headers = {
            **self.HEADERS[address],
            "Authorization": f"Bearer {self.access_tokens[address]}"
        }
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, proxy=proxy, proxy_auth=proxy_auth) as response:
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
            
    async def claim_checkin(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/check-in"
        headers = {
            **self.HEADERS[address],
            "Authorization": f"Bearer {self.access_tokens[address]}",
            "Content-Length": "2",
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, json={}, proxy=proxy, proxy_auth=proxy_auth) as response:
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
            
    async def perform_draw(self, address: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/draw"
        headers = {
            **self.HEADERS[address],
            "Authorization": f"Bearer {self.access_tokens[address]}",
            "Content-Length": "2",
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, json={}, proxy=proxy, proxy_auth=proxy_auth) as response:
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
    
    async def process_check_connection(self, address: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}Proxy   :{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {proxy} {Style.RESET_ALL}"
            )

            is_valid = await self.check_connection(proxy)
            if not is_valid:
                if rotate_proxy:
                    proxy = self.rotate_proxy_for_account(address)
                    continue

                return False
            
            return True
            
    async def process_get_nonce(self, address: str, use_proxy: bool, rotate_proxy: bool):
        is_valid = await self.process_check_connection(address, use_proxy, rotate_proxy)
        if is_valid:

            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            nonce = await self.get_message(address, proxy)
            if not nonce: return False
            
            return nonce["message"]
            
    async def process_verify_signature(self, account: str, address: str, use_proxy: bool, rotate_proxy: bool):
        message = await self.process_get_nonce(address, use_proxy, rotate_proxy)
        if message:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            verify = await self.verify_signature(account, address, message, proxy)
            if not verify: return False

            self.access_tokens[address] = verify["token"]

            self.log(
                f"{Fore.CYAN + Style.BRIGHT}Status  :{Style.RESET_ALL}"
                f"{Fore.GREEN + Style.BRIGHT} Login Success {Style.RESET_ALL}"
            )
            return True
        
    async def process_perform_wrap(self, account: str, address: str, use_proxy: bool):
        tx_hash, block_number = await self.perform_wrap(account, address, use_proxy)
        if tx_hash and block_number:
            explorer = f"https://testnet.xoscan.io/tx/{tx_hash}"
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Status  :{Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
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
                f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
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

    async def process_perform_swap(self, account: str, address: str, swap_type: str, from_token: str, to_token: str, amount_in: float, use_proxy: bool):
        tx_hash, block_number = await self.perform_swap(account, address, swap_type, from_token, to_token, amount_in, use_proxy)
        if tx_hash and block_number:
            explorer = f"https://testnet.xoscan.io/tx/{tx_hash}"

            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Status  :{Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
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

    async def process_perform_liquidity(self, account: str, address: str, token_type: str, token0: str, token1: str, amount0_desired: int, amount1_desired: int, use_proxy: bool):
        tx_hash, block_number = await self.perform_liquidity(account, address, token_type, token0, token1, amount0_desired, amount1_desired, use_proxy)
        if tx_hash and block_number:
            explorer = f"https://testnet.xoscan.io/tx/{tx_hash}"
            
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Status  :{Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT} Success {Style.RESET_ALL}"
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

    async def process_option_2(self, account: str, address: str, use_proxy: bool):
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

    async def process_option_2(self, account: str, address: str, use_proxy: bool):
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
        await self.print_timer()
        
    async def process_option_3(self, account: str, address: str, use_proxy: bool):
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
        await self.print_timer()

    async def process_option_4(self, account: str, address: str, use_proxy: bool):
        self.log(f"{Fore.CYAN+Style.BRIGHT}Swap    :{Style.RESET_ALL}                       ")
        for i in range(self.swap_count):
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}   ● {Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT}Swap{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {i+1} / {self.swap_count} {Style.RESET_ALL}                           "
            )

            swap_type, from_ticker, to_ticker, from_token, to_token, amount_in = self.generate_swap_option()

            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Option  :{Style.RESET_ALL}"
                f"{Fore.BLUE+Style.BRIGHT} {from_ticker} to {to_ticker} {Style.RESET_ALL}"
            )

            if swap_type != "native to erc20":
                balance = await self.get_token_balance(address, from_token, use_proxy)
            else:
                balance = await self.get_token_balance(address, "XOS", use_proxy)

            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Balance :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {balance} {from_ticker} {Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Amount  :{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {amount_in} {from_ticker} {Style.RESET_ALL}"
            )

            if not balance or balance <= amount_in:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Status  :{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} Insufficient {from_ticker} Token Balance {Style.RESET_ALL}"
                )
                continue

            await self.process_perform_swap(account, address, swap_type, from_token, to_token, amount_in, use_proxy)
            await self.print_timer()

    async def process_option_5(self, account: str, address: str, use_proxy):
        self.log(f"{Fore.CYAN+Style.BRIGHT}Add LP  :{Style.RESET_ALL}                       ")
        for i in range(self.liquidity_count):
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}   ● {Style.RESET_ALL}"
                f"{Fore.GREEN+Style.BRIGHT}Liquidity{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {i+1} / {self.liquidity_count} {Style.RESET_ALL}                           "
            )

            liquidity_option, token_type, ticker0, ticker1, token0, token1, amount0_desired = self.generate_liquidity_option()

            self.log(
                f"{Fore.CYAN+Style.BRIGHT}     Option  :{Style.RESET_ALL}"
                f"{Fore.BLUE+Style.BRIGHT} {liquidity_option} {Style.RESET_ALL}"
            )

            if token_type == "native":
                balance0 = await self.get_token_balance(address, "XOS", use_proxy)

            elif token_type == "erc20":
                balance0 = await self.get_token_balance(address, token0, use_proxy)
            
            balance1 = await self.get_token_balance(address, token1, use_proxy)

            self.log(f"{Fore.CYAN+Style.BRIGHT}     Balance :{Style.RESET_ALL}")
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}        ● {Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT}{balance0} {ticker0}{Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}        ● {Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT}{balance1} {ticker1}{Style.RESET_ALL}"
            )

            path = bytes.fromhex(token0[2:]) + (500).to_bytes(3, "big") + bytes.fromhex(token1[2:])
            amount1_desired = await self.get_amount_out_min(address, path, amount0_desired, use_proxy)
            if not amount1_desired:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Status  :{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} Fetch {ticker0} per {ticker1} Current Price Failed {Style.RESET_ALL}"
                )
                continue

            amount0 = amount0_desired / (10 ** 18)
            amount1 = amount1_desired / (10 ** 18)

            self.log(f"{Fore.CYAN+Style.BRIGHT}     Amount  :{Style.RESET_ALL}")
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}        ● {Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT}{amount0} {ticker0}{Style.RESET_ALL}"
            )
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}        ● {Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT}{amount1} {ticker1}{Style.RESET_ALL}"
            )

            if not balance0 or balance0 <=  amount0:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Status  :{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} Insufficient {ticker0} Token Balance {Style.RESET_ALL}"
                )
                continue
            
            if not balance1 or balance1 <=  amount1:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}     Status  :{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} Insufficient {ticker1} Token Balance {Style.RESET_ALL}"
                )
                continue
            
            await self.process_perform_liquidity(account, address, token_type, token0, token1, amount0_desired, amount1_desired, use_proxy)
            await self.print_timer()

    async def process_accounts(self, account: str, address, option: int, use_proxy: bool, rotate_proxy: bool):
        verifed = await self.process_verify_signature(account, address, use_proxy, rotate_proxy)
        if verifed:
            try:
                web3 = await self.get_web3_with_check(address, use_proxy)
                if not web3: return
                
                self.used_nonce[address] = web3.eth.get_transaction_count(address, "pending")

            except Exception as e:
                return self.log(
                    f"{Fore.CYAN+Style.BRIGHT}Status  :{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} {str(e)} {Style.RESET_ALL}"
                )
            
            if option == 1:
                await self.process_option_1(address, use_proxy)

            elif option == 2:
                await self.process_option_2(account, address, use_proxy)

            elif option == 3:
                await self.process_option_3(account, address, use_proxy)

            elif option == 4:
                await self.process_option_4(account, address, use_proxy)

            elif option == 5:
                    await self.process_option_5(account, address, use_proxy)

            elif option == 6:
                await self.process_option_1(address, use_proxy)
                await asyncio.sleep(5)

                if self.wrap_option == 1:
                    await self.process_option_2(account, address, use_proxy)
                elif self.wrap_option == 2:
                    await self.process_option_3(account, address, use_proxy)

                await asyncio.sleep(5)

                await self.process_option_4(account, address, use_proxy)
                await asyncio.sleep(5)

                await self.process_option_5(account, address, use_proxy)
                await asyncio.sleep(5)

    async def main(self):
        try:
            with open('accounts.txt', 'r') as file:
                accounts = [line.strip() for line in file if line.strip()]

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

                        self.HEADERS[address] = {
                            "Accept": "application/json, text/plain, */*",
                            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                            "Origin": "https://x.ink",
                            "Referer": "https://x.ink/",
                            "Sec-Fetch-Dest": "empty",
                            "Sec-Fetch-Mode": "cors",
                            "Sec-Fetch-Site": "same-site",
                            "User-Agent": FakeUserAgent().random
                        }

                        await self.process_accounts(account, address, option, use_proxy, rotate_proxy)
                        await asyncio.sleep(3)

                self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*72)
                
                delay = 24 * 60 * 60
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
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] XOS Testnet - BOT{Style.RESET_ALL}                                       "                              
        )