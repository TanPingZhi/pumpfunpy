# pumpfunpy

**The Bloomberg Terminal for Degenerates**

A Python client library for interacting with Pump.fun’s on-chain and off-chain APIs: stream live trades & coin listings, query market data, execute swaps, and transfer SPL tokens.

---

## 📦 Features

- **REST API wrappers** for Pump.fun Frontend, Advanced, and Swap endpoints  
- **WebSocket & NATS** streaming of:  
  - All trades  
  - New coins  
  - New replies  
  - Graduated-coin trade events via DexScreener  
- **On-chain trading & wallet** (coming soon!)  
- **Extensible** HTTP client & streamer factories  
- **Async & sync** support (plans to expand both)

---

## 🛣 Roadmap & Upcoming Features

We’re constantly improving pumpfunpy. Here’s what’s on the horizon:

1. **Comprehensive Documentation**  
   - Add detailed docstrings for every module, class, and method  
   - Generate API reference with Sphinx or MkDocs + autodoc  
   - Publish hosted docs (ReadTheDocs or GitHub Pages)

2. **Inline Commenting & Code Clarity**  
   - Audit and enhance inline comments for complex logic  
   - Standardize docstring style (Google or NumPy style)  
   - Add usage examples in docstrings

3. **Refactoring & Modularization**  
   - Extract common base classes for endpoint wrappers  
   - Introduce Pydantic models or dataclasses for responses  
   - Centralize retry/backoff logic in HTTPClient  
   - Implement dependency injection for HTTP/Solana clients and streamers

4. **Solana On-Chain Trading Integration**  
   - **SolanaClient**: wrapper around `solana-py` or JSON-RPC  
   - **TradingAPI**: support swaps via Jupiter, Raydium, Serum  
   - **WalletAPI**: SPL token transfers, account management  
   - Key management: local Keypair, env-vars, hardware wallet support  
   - Configurable RPC endpoints: support Mainnet-Beta, Helius, QuickNode

5. **Testing & CI Improvements**  
   - Unit tests for new modules, mocking network calls  
   - Integration tests against Devnet or a local validator  
   - GitHub Actions workflows for build, test, lint, and publish

---

## 🚀 Installation

```bash
pip install pumpfunpy
```

Or install the latest development version:

```bash
git clone https://github.com/TanPingZhi/pumpfunpy.git
cd pumpfunpy
pip install .
```

---

## ⚡ Quickstart

```python
from pumpfunpy import api

# List the newest coins
resp = api.list_new_coins(last_score=0)
print(resp["coins"][:5])

# Get SOL price
sol = api.get_sol_price()
print(f"SOL price: ${sol}")

# Stream live trades (async)
import asyncio

async def main():
    async for trade in api.stream_all_trades():
        print(trade)

asyncio.run(main())
```

---

## 🔧 Configuration

By default, `pumpfunpy` picks up API endpoints from `pumpfunpy/config.py`. You can override:

```python
from pumpfunpy import PumpFunAPI, HTTPClient

# Custom Frontend URL & headers
frontend_client = HTTPClient(
    base_url="https://my-custom-endpoint.com",
    headers={"X-Api-Key": "MY_KEY"}
)
api = PumpFunAPI(_frontend_client=frontend_client)
```

Future versions will include Solana RPC, key-management, and swap configuration.

---

## 🤝 Contributing

1. Fork the repo  
2. Create a feature branch:  
   ```bash
   git checkout -b feature/my-feature
   ```  
3. Commit your changes & push:  
   ```bash
   git commit -am "Add awesome feature"
   git push origin feature/my-feature
   ```  
4. Open a Pull Request

Please run `pytest` for existing tests and add coverage for new features.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 📬 Contact

Have questions, ideas, or want to report an issue?  
✉️ Email: [pumpfunpy@gmail.com](mailto:pumpfunpy@gmail.com)
