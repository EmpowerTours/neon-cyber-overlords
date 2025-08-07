# app.py

import streamlit as st
import random
import time
from web3 import Web3
import altair as alt
import pandas as pd

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

# Monad Testnet RPC (provided by user)
RPC_URL = 'https://monad-testnet.g.alchemy.com/v2/kgLrnOrgMfbKihXEBsjt9'
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Contract address (provided by user)
CONTRACT_ADDRESS = '0x24c97ccB47ee7b041E581AE49dE1535A85835B70'

# ABI (provided by user)
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
        history = contract.functions.getActionHistory().call()
        st.session_state.action_history = history
    except Exception as e:
        st.error(f"Error fetching history: {str(e)}")

def plot_activity_graph():
    if not st.session_state.action_history:
        st.info("No activities yet.")
        return
    data = []
    for event in st.session_state.action_history:
        data.append({'Time': event[3], 'Action': 1})  # Timestamp, count 1 per action
    df = pd.DataFrame(data)
    df = df.groupby('Time').sum().reset_index()  # Aggregate counts per time
    chart = alt.Chart(df).mark_line(point=True).encode(
        x='Time:T',
        y='Action:Q',
        tooltip=['Time', 'Action']
    ).properties(title='Network Activity (Actions Over Time)')
    st.altair_chart(chart, use_container_width=True)

# Main App
st.title("Neon Cyber Overlords v1 - Testing Monad Limits")
st.markdown("Connect, register, and perform actions against players. Hacks spam tiny tMONAD to test tx throughput. Push Monad's limits with frequent actions, queries, and multiplayer interactions!")

# Wallet Connection
st.components.v1.html("""
    <button onclick="connectWallet()" style="background-color: #00ffff; color: black; border: none; border-radius: 5px; padding: 8px 16px;">Connect Wallet</button>
    <p id="account" style="font-size: 12px; word-break: break-all;"></p>
    <script>
    async function connectWallet() {
      if (window.ethereum) {
        try {
          const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
          document.getElementById('account').innerHTML = 'Connected: ' + accounts[0];
          parent.window.postMessage({type: 'wallet_connected', address: accounts[0]}, '*');
        } catch (error) {
          console.error(error);
          alert('Connection failed: ' + error.message);
        }
      } else {
        alert('MetaMask not detected! Install from metamask.io or enable extension.');
      }
    }
    let web3 = new Web3(window.ethereum);
    const contractAddress = '%s';
    const abi = %s;
    window.addEventListener('message', async (event) => {
      if (event.data.type === 'perform_action') {
        const { method, params } = event.data;
        try {
          const contract = new web3.eth.Contract(abi, contractAddress);
          const tx = await contract.methods[method](...params).send({from: ethereum.selectedAddress});
          console.log('Tx hash:', tx.transactionHash);
        } catch (error) {
          console.error(error);
          alert('Action failed: ' + error.message);
        }
      }
    });
    </script>
""" % (CONTRACT_ADDRESS, ABI), height=150)

# Listen for connection (set address)
connected_address = st.text_input("Enter your connected address (for testing):", value=st.session_state.connected_address or "")
if connected_address:
    st.session_state.connected_address = connected_address

# Refresh Button to test query limits
if st.button("Refresh Game (Test Query Load)"):
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

# Power Progress (test UI updates)
st.progress(st.session_state.my_data["power"] / 1000)
st.caption(f"Power: {st.session_state.my_data['power']}/1000 - Reach 1000 to win!")

# Game Log (test frequent updates)
st.subheader("Game Log")
st.markdown('<div class="game-log">' + '<br>'.join(st.session_state.game_output) + '</div>', unsafe_allow_html=True)

# Live Graph (test data fetching/processing limits)
st.subheader("Live Blockchain Activity Graph (Test Query/Render Load)")
plot_activity_graph()

# Players List (test list fetching)
st.subheader("Online Players (Test Multiplayer Scale)")
for p in st.session_state.players:
    st.write(p)

# Actions Sidebar (test tx limits with spam)
with st.sidebar:
    st.header("Actions (Push Tx Limits)")
    if st.button("Register (One-Time)"):
        st.components.v1.html("""<script>parent.window.postMessage({type: 'perform_action', method: 'register', params: []}, '*');</script>""", height=0)
        st.info("Registration tx sent - check explorer for confirmation.")
    target = st.selectbox("Select Target (for Attacks)", st.session_state.players)
    if st.button("Hack (Spam Tiny tMONAD to Test Throughput)"):
        st.components.v1.html("""<script>parent.window.postMessage({type: 'perform_action', method: 'hack', params: ['%s']}, '*');</script>""" % target, height=0)
        st.info("Hack tx sent - spams to test Monad TPS!")
    if st.button("Injection (Power Steal)"):
        st.components.v1.html("""<script>parent.window.postMessage({type: 'perform_action', method: 'injection', params: ['%s']}, '*');</script>""" % target, height=0)
    if st.button("Phishing (MON Steal)"):
        st.components.v1.html("""<script>parent.window.postMessage({type: 'perform_action', method: 'phishing', params: ['%s']}, '*');</script>""" % target, height=0)
    if st.button("Deploy Bot (Power Boost)"):
        st.components.v1.html("""<script>parent.window.postMessage({type: 'perform_action', method: 'deployBot', params: []}, '*');</script>""", height=0)

# Inventory (test data display)
with st.expander("Your Inventory"):
    st.json(st.session_state.my_data)

# Win Check
if st.session_state.my_data["power"] >= 1000:
    st.balloons()
    st.success("You've become the ultimate Neon Cyber Overlord! Game Won!")

# Leaderboard to add excitement (test sorting/large lists)
st.subheader("Leaderboard (Test Data Processing)")
leaderboard = []
for p in st.session_state.players:
    try:
        _, power, _ = contract.functions.getPlayer(p).call()
        leaderboard.append({"Player": p, "Power": power})
    except:
        pass
leaderboard_df = pd.DataFrame(leaderboard).sort_values("Power", ascending=False)
st.dataframe(leaderboard_df)

# Fun Element: Spam Test Button (to push Monad limits)
if st.button("Stress Test: Perform 10 Hacks in Loop (WARNING: Costs MON, Tests TPS)"):
    st.warning("This will send 10 hack tx in sequence - monitor explorer for Monad performance!")
    for _ in range(10):
        random_target = random.choice(st.session_state.players) if st.session_state.players else st.session_state.connected_address
        st.components.v1.html("""<script>parent.window.postMessage({type: 'perform_action', method: 'hack', params: ['%s']}, '*');</script>""" % random_target, height=0)
        time.sleep(1)  # Slight delay to avoid instant rejection
