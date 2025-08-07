# README.md

# Neon Cyber Overlords v1 - Monad Testnet Game

A multiplayer text-based RPG to test Monad blockchain's limits: high TPS via spam tx in hacks, frequent queries for live graph/leaderboard, scalable multiplayer data fetching, and exciting cryptonomics mechanics.

## Purpose
- **Fun & Exciting Gameplay**: Connect wallet, register on-chain, target players or AI for hacks (with spam for thrill), injections, phishing, or bot deploys. Build power to 1000 to win! AI mode for solo play with simulated attacks/defenses.
- **Test Monad Limits**: Stress parallel execution with tx bursts (hacks spam 0.000001 tMONAD to 10 players), query loads (action history graph with real tx hashes, leaderboard), and scalability (player lists, events).
- **Web3 Integration**: All data on Monad Testnet—real tx for actions, NFTs as strings, MON/power as uints. Bots use real generated wallets (fund via faucet).

## Setup
1. Clone repo or edit on GitHub.
2. Update `app.py` with your Alchemy RPC (free tier) and contract address.
3. Run locally: `pip install -r requirements.txt` then `streamlit run app.py`.
4. Deploy on Railway: Follow previous instructions—free tier handles basic load.

## Monad Testnet Config
- RPC: Use Alchemy free tier[](https://monad-testnet.g.alchemy.com/v2/YOUR_KEY).
- Chain ID: 10143
- Faucet for tMONAD: Search Monad docs for testnet faucet.

## Features to Test Monad
- **TPS/Throughput**: Hack action spams multiple micro-tx—use "Stress Test" button for bursts.
- **Query Scalability**: Graph fetches/aggregates logs with tx hashes; leaderboard polls all players.
- **Parallel Execution**: Multiplayer actions run concurrently; observe in explorer.
- **EVM Compatibility**: Standard Solidity contract with events, mappings.
- **AI Mode**: Solo play with simulated opponents and attacks for interaction when no players.
- **Bots**: Generate real Monad wallets for bots—fund and use for automated actions to test limits.

Built to push boundaries—report Monad performance in issues!

Date: August 07, 2025
