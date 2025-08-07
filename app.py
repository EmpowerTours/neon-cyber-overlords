import streamlit as st
import random
import time
from web3 import Web3
import altair as alt
import pandas as pd
import ecdsa
import hashlib
import binascii
import threading

# Custom CSS for clean, neon-themed UI
st.markdown("""
    <style>
    /* Hide Streamlit menu and footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    /* Clean font and background */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f0f0;
    }
    .stButton > button {
        background-color: #00ffff; /* Neon cyan */
        color: black;
        border: none;
        border-radius: 5px;
        padding: 8px 16px;
    }
    .stButton > button:hover {
        background-color: #ff00ff; /* Neon magenta */
    }
    .stProgress > div > div > div > div {
        background-color: #00ff00; /* Neon green */
    }
    /* Game log styling */
    .game-log {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ddd;
        max-height: 400px;
        overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Monad Testnet RPC (Alchemy URL provided by user)
RPC_URL = 'https://monad-testnet.g.alchemy.com/v2/kgLrnOrgMfbKihXEBsjt9'
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Contract address (provided by user)
CONTRACT_ADDRESS = '0x24c97ccB47ee7b041E581AE49dE1535A85835B70'

# ABI (provided by user, with booleans as False/True)
ABI = [
  {
    "anonymous": False,
    "inputs": [
      {
        "indexed": True,
        "internalType": "address",
        "name": "from",
        "type": "address"
      },
      {
        "indexed": True,
        "internalType": "address",
        "name": "to",
        "type": "address"
      },
      {
        "indexed": False,
        "internalType": "string",
        "name": "action",
        "type": "string"
      },
      {
        "indexed": False,
        "internalType": "uint256",
        "name": "timestamp",
        "type": "uint256"
      }
    ],
    "name": "ActionPerformed",
    "type": "event"
  },
  {
    "inputs": [],
    "name": "deployBot",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "target",
        "type": "address"
      }
    ],
    "name": "hack",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "target",
        "type": "address"
      }
    ],
    "name": "injection",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "target",
        "type": "address"
      }
    ],
    "name": "phishing",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "register",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "actionHistory",
    "outputs": [
      {
        "internalType": "address",
        "name": "from",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "to",
        "type": "address"
      },
      {
        "internalType": "string",
        "name": "action",
        "type": "string"
      },
      {
        "internalType": "uint256",
        "name": "timestamp",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getActionHistory",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "from",
            "type": "address"
          },
          {
            "internalType": "address",
            "name": "to",
            "type": "address"
          },
          {
            "internalType": "string",
            "name": "action",
            "type": "string"
          },
          {
            "internalType": "uint256",
            "name": "timestamp",
            "type": "uint256"
          }
        ],
        "internalType": "struct CyberOverlords.ActionEvent[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "addr",
        "type": "address"
      }
    ],
    "name": "getPlayer",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "mon",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "power",
        "type": "uint256"
      },
      {
        "internalType": "string[]",
        "name": "nfts",
        "type": "string[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getPlayers",
    "outputs": [
      {
        "internalType": "address[]",
        "name": "",
        "type": "address[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "playerList",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "players",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "mon",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "power",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# Session state
if 'game_output' not in st.session_state:
    st.session_state.game_output = ["Connect wallet to start."]
    st.session_state.connected_address = None
    st.session_state.players = []
    st.session_state.my_data = {"mon": 0, "power": 0, "nfts": []}
    st.session_state.action_history = []
    st.session_state.ai_mode = False
    st.session_state.ai_opponents = []  # For AI mode
    st.session_state.attack_timer = 0  # For simulated attacks
    st.session_state.bots = []  # List of {'address': str, 'private_key': str}
    st.session_state.auto_refresh = False

# Generate Real Monad Wallet for Bot
def generate_wallet():
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    private_key = '0x' + sk.to_string().hex()
    vk = sk.verifying_key
    public_key = b'\x04' + vk.to_string()
    keccak = hashlib.sha3_256(public_key[1:]).digest()
    address = '0x' + keccak[-20:].hex()
    return {'address': address, 'private_key': private_key}

# Sign and Send Tx from Bot
def sign_and_send(method, params, private_key):
    account = w3.eth.account.from_key(private_key)
    nonce = w3.eth.get_transaction_count(account.address)
    tx = contract.functions[method](*params).build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': 200000,
        'gasPrice': w3.to_wei('1', 'gwei'),
        'chainId': 10143  # Monad Testnet Chain ID
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()

# AI Mode Functions
def generate_ai_opponent():
    bot = generate_wallet()  # Real wallet for bot
    st.session_state.bots.append(bot)
    ai_data = {"mon": random.randint(500, 1500), "power": random.randint(50, 200)}
    st.info(f"AI Bot created! Address: {bot['address']} Private Key: {bot['private_key']}. Fund with tMONAD to activate real tx.")
    return {"address": bot['address'], "data": ai_data, "private_key": bot['private_key']}

def simulate_ai_action(user_data):
    attack_type = random.choice(["hack", "injection", "phishing"])
    damage = random.randint(10, 50)
    if attack_type == "hack":
        user_data["mon"] = max(0, user_data["mon"] - damage)
    elif attack_type == "injection":
        user_data["power"] = max(0, user_data["power"] - damage)
    else:
        user_data["mon"] = max(0, user_data["mon"] - damage / 2)
        user_data["power"] = max(0, user_data["power"] - damage / 2)
    return attack_type, damage

def defend_simulation():
    boost = random.randint(20, 60)
    st.session_state.my_data["power"] += boost
    st.session_state.game_output.append(f"Defended successfully! Gained {boost} power.")

# Fetch Functions (real-time logs with tx hashes)
def fetch_players():
    try:
        st.session_state.players = contract.functions.getPlayers().call()
    except Exception as e:
        st.error(f"Error fetching players: {str(e)}")

def fetch_my_data():
    if st.session_state.connected_address:
        try:
            mon, power, nfts = contract.functions.getPlayer(st.session_state.connected_address).call()
            st.session_state.my_data = {"mon": mon, "power": power, "nfts": nfts}
        except Exception as e:
            st.error(f"Error fetching your data: {str(e)}")

def fetch_action_history():
    try:
        current_block = w3.eth.block_number
        logs = w3.eth.get_logs({'fromBlock': current_block - 100, 'toBlock': 'latest', 'address': CONTRACT_ADDRESS})
        data = []
        for log in logs:
            block = w3.eth.get_block(log.blockNumber)
            data.append({
                'Time': block['timestamp'],
                'Action': 1,
                'Tx Hash': log.transactionHash.hex()
            })
        st.session_state.action_history = data
    except Exception as e:
        st.error(f"Error fetching logs: {str(e)}")

def plot_activity_graph():
    if not st.session_state.action_history:
        st.info("No activities yet.")
        return
    df = pd.DataFrame(st.session_state.action_history)
    df = df.groupby('Time').sum().reset_index()  # Aggregate counts per time
    chart = alt.Chart(df).mark_line(point=True).encode(
        x='Time:T',
        y='Action:Q',
        tooltip=['Time', 'Action', 'Tx Hash']
    ).properties(title='Network Activity (Actions Over Time with Tx Hashes)')
    st.altair_chart(chart, use_container_width=True)

    # Table of recent tx
    st.subheader("Recent Tx Hashes")
    st.table(df[['Time', 'Tx Hash']])

# Auto Refresh Thread
def auto_refresh():
    while st.session_state.get('auto_refresh', False):
        fetch_action_history()
        time.sleep(5)
        st.rerun()

if 'auto_thread' not in st.session_state:
    st.session_state.auto_thread = None

if st.button("Toggle Auto Refresh (Every 5s for Real-Time Graph)"):
    st.session_state.auto_refresh = not st.session_state.get('auto_refresh', False)
    if st.session_state.auto_refresh:
        st.session_state.auto_thread = threading.Thread(target=auto_refresh)
        st.session_state.auto_thread.start()
    else:
        if st.session_state.auto_thread:
            st.session_state.auto_thread.join()  # Wait for thread to stop

# Main App
st.title("Neon Cyber Overlords v1 - Testing Monad Limits")
st.markdown("Connect, register, create bots with real wallets (fund via faucet), and perform actions. Hacks spam tiny tMONAD. Graph shows real-time tx from logs. Test limits with bot swarms!")

# Wallet Connection (native button with JS)
if st.button("Connect Wallet"):
    st.markdown("""
        <p id="account" style="font-size: 12px; word-break: break-all;"></p>
        <p id="debug" style="font-size: 12px; color: red;"></p>
        <script>
        async function connectWallet() {
          console.log('Attempting connection...');
          if (window.ethereum) {
            console.log('ethereum object detected');
            if (window.ethereum.isMetaMask) {
              console.log('isMetaMask true');
            } else {
              console.log('isMetaMask false');
            }
            try {
              const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
              document.getElementById('account').innerHTML = 'Connected: ' + accounts[0];
              parent.window.postMessage({type: 'wallet_connected', address: accounts[0]}, '*');
              document.getElementById('debug').innerHTML = 'Connection successful!';
            } catch (error) {
              console.error(error);
              document.getElementById('debug').innerHTML = 'Error: ' + error.message;
              alert('Connection failed: ' + error.message + '. Check console for details.');
            }
          } else {
            console.log('ethereum object not found');
            document.getElementById('debug').innerHTML = 'MetaMask not detected. Check extensions and reload.';
            alert('MetaMask not detected! Ensure it\'s enabled and reload the page.');
          }
        }
        connectWallet();  // Auto-call on button click
        </script>
    """, unsafe_allow_html=True)

# Bot Creation
if st.button("Create Bot (Generates Real Monad Wallet)"):
    bot = generate_wallet()
    st.session_state.bots.append(bot)
    st.info(f"Bot created! Address: {bot['address']} Private Key (keep secret): {bot['private_key']}")
    st.warning("Copy address, fund with tMONAD via faucet (e.g., faucet.monad.xyz), then use private key for bot actions below.")

# List Bots
st.subheader("Your Bots")
for bot in st.session_state.bots:
    st.write(f"Bot Address: {bot['address']}")

# Bot Actions (use private key to sign)
st.subheader("Bot Actions (Test Limits with Signed Tx)")
bot_target = st.text_input("Bot Target Address for Hack")
bot_private_key = st.text_input("Bot Private Key for Signing", type="password")
if st.button("Bot Hack (Sign and Send from Bot)"):
    try:
        tx_hash = sign_and_send('hack', [bot_target], bot_private_key)
        st.success(f"Bot hack tx sent: {tx_hash}")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Bot Swarm Test (create and register multiple, but fund manual)
if st.button("Create Bot Swarm (10 Bots for Limit Testing)"):
    for _ in range(10):
        bot = generate_wallet()
        st.session_state.bots.append(bot)
    st.info("10 Bots created! Fund each address via faucet, then register/activate individually.")

# AI Mode Toggle
st.session_state.ai_mode = st.checkbox("Enable AI Mode (Play Against Computer)", value=True)  # Default on for solo play

if st.session_state.ai_mode:
    if not st.session_state.ai_opponents:
        st.session_state.ai_opponents = [generate_ai_opponent() for _ in range(3)]  # 3 AI opponents with real wallets
    st.info("AI Mode Enabled: Interact with computer opponents. Simulate defenses from cyber attacks.")

# Simulated Attack Timer
if st.session_state.ai_mode:
    if st.button("Simulate Incoming Attack"):
        attack_type, damage = simulate_ai_action(st.session_state.my_data)
        st.session_state.game_output.append(f"AI Attack ({attack_type})! Lost {damage} resources.")
        st.error("Cyber Attack Simulated! Defend now.")

# Refresh Button
if st.button("Refresh Game"):
    fetch_players()
    fetch_my_data()
    fetch_action_history()
    st.rerun()

with st.expander("Monad Testnet Setup"):
    st.markdown("""
    Network Name: Monad Testnet
    RPC: https://monad-testnet.g.alchemy.com/v2/kgLrnOrgMfbKihXEBsjt9
    Chain ID: 10143
    Symbol: tMONAD
    Explorer: https://testnet.monad.xyz/explorer
    Get test tMONAD from faucet if needed.
    """)

# Power Progress (clamp to 0-1)
power_progress = max(0, min(1, st.session_state.my_data["power"] / 1000))
st.progress(power_progress)
st.caption(f"Power: {st.session_state.my_data['power']}/1000 - Reach 1000 to win!")

# Game Log
st.subheader("Game Log")
st.markdown('<div class="game-log">' + '<br>'.join(st.session_state.game_output) + '</div>', unsafe_allow_html=True)

# Live Graph with Tx Hashes
st.subheader("Live Blockchain Activity Graph")
plot_activity_graph()

# Players/AI
st.subheader("Online Players / AI Opponents")
for p in st.session_state.players:
    st.write(p)
if st.session_state.ai_mode:
    for ai in st.session_state.ai_opponents:
        st.write(f"{ai['address']} (AI) - Power: {ai['data']['power']}")

# Actions Sidebar
with st.sidebar:
    st.header("Actions")
    if st.button("Register"):
        st.markdown("""
            <script>parent.window.postMessage({type: 'perform_action', method: 'register', params: []}, '*');</script>
        """, unsafe_allow_html=True)
    target_options = st.session_state.players + [ai['address'] for ai in st.session_state.ai_opponents] if st.session_state.ai_mode else st.session_state.players
    target = st.selectbox("Select Target", target_options)
    if st.button("Hack (Spam Tiny tMONAD)"):
        if 'AI' in target:
            st.session_state.my_data["power"] += 10
            st.session_state.game_output.append(f"Simulated Hack on AI {target}! Gained 10 power.")
        else:
            st.markdown("""
                <script>parent.window.postMessage({type: 'perform_action', method: 'hack', params: ['%s']}, '*');</script>
            """ % target, unsafe_allow_html=True)
    if st.button("Injection"):
        if 'AI' in target:
            st.session_state.my_data["power"] += 20
            st.session_state.game_output.append(f"Simulated Injection on AI {target}! Gained 20 power.")
        else:
            st.markdown("""
                <script>parent.window.postMessage({type: 'perform_action', method: 'injection', params: ['%s']}, '*');</script>
            """ % target, unsafe_allow_html=True)
    if st.button("Phishing"):
        if 'AI' in target:
            st.session_state.my_data["mon"] += 50
            st.session_state.game_output.append(f"Simulated Phishing on AI {target}! Gained 50 MON.")
        else:
            st.markdown("""
                <script>parent.window.postMessage({type: 'perform_action', method: 'phishing', params: ['%s']}, '*');</script>
            """ % target, unsafe_allow_html=True)
    if st.button("Deploy Bot"):
        st.markdown("""
            <script>parent.window.postMessage({type: 'perform_action', method: 'deployBot', params: []}, '*');</script>
        """, unsafe_allow_html=True)
    if st.session_state.ai_mode:
        if st.button("Defend from AI Attack"):
            defend_simulation()

# Inventory
with st.expander("Your Inventory"):
    st.json(st.session_state.my_data)

# Leaderboard
st.subheader("Leaderboard")
leaderboard = []
for p in st.session_state.players:
    try:
        _, power, _ = contract.functions.getPlayer(p).call()
        leaderboard.append({"Player": p, "Power": power})
    except:
        pass
if st.session_state.ai_mode:
    for ai in st.session_state.ai_opponents:
        leaderboard.append({"Player": ai['address'] + " (AI)", "Power": ai['data']['power']})
if leaderboard:
    leaderboard_df = pd.DataFrame(leaderboard).sort_values("Power", ascending=False)
    st.dataframe(leaderboard_df)
else:
    st.info("No players or AI yet.")

if st.session_state.my_data["power"] >= 1000:
    st.success("You win!")
