import streamlit as st
import random
import time

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

# Monanimals list (text-based)
monanimals = [
    ("VoidDrake", "Deep purple scales", "Glowing red eyes", "Golden circuits", "Level: 1, Bonus: 15% NFT Liquidation Resistance"),
    ("Molandak", "Vibrant green hide", "Pitch black eyes", "Golden circuits", "Level: 1, Bonus: 5% Stake APY Boost"),
    ("Chog", "Earthy brown fur", "Pitch black eyes", "Golden circuits", "Level: 1, Bonus: 8% Pool Contribution Yield"),
    ("Moyaki", "Electric blue skin", "Bright white eyes", "Golden circuits", "Level: 1, Bonus: 7% Burn Token Efficiency"),
    ("Mouch", "Sleek gray armor", "Pitch black eyes", "Golden circuits", "Level: 1, Bonus: 6% NFT Yield Farming"),
    ("Salmonad", "Soft pink glow", "Pitch black eyes", "Golden circuits", "Level: 1, Bonus: 9% DAO Governance Power"),
    ("Purple Frens", "Vivid purple aura", "Bright white eyes", "Golden circuits", "Level: 1, Bonus: 4% Alliance NFT Sharing"),
    ("Monad Nomads", "Sunny yellow nomadic form", "Pitch black eyes", "Golden circuits", "Level: 1, Bonus: 5% Oracle Recovery Speed"),
    ("Skrumpeys", "Fiery orange spikes", "Pitch black eyes", "Golden circuits", "Level: 1, Bonus: 6% Bridge NFT Security"),
    ("Spikynads", "Crimson red thorns", "Bright white eyes", "Golden circuits", "Level: 1, Bonus: 7% Mint NFT Speed"),
    ("The Boo DAO", "Shadowy black void", "Glowing red eyes", "Golden circuits", "Level: 1, Bonus: 8% Airdrop NFT Chance"),
    ("BlockNads", "Deep blue blocks", "Bright white eyes", "Golden circuits", "Level: 1, Bonus: 9% Wallet NFT Balance"),
    ("Monadians", "Lush green essence", "Pitch black eyes", "Golden circuits", "Level: 1, Bonus: 10% Swap Fee Reduction"),
    ("Monega", "Cyan energy waves", "Magenta eyes", "Golden circuits", "Level: 1, Bonus: 12% Recovery Time Reduction")
]

# Initialize session state
if 'player_mon' not in st.session_state:
    st.session_state.player_mon = 1000
    st.session_state.player_nfts = random.sample(monanimals, 3)
    st.session_state.player_power = 100
    st.session_state.crashed = False
    st.session_state.recovery_time = 5  # Reduced for better UX (simulated seconds)
    st.session_state.game_output = ["Welcome! Start hacking or staking to build power."]

def describe_monanimal(mon):
    name, base, eyes, acc, stats = mon
    return f"{name}: A fierce cyber beast with {base}, {eyes}, and {acc}. Stats: {stats}"

def display_inventory():
    output = [
        f"MON Tokens: {st.session_state.player_mon}",
        f"Power Level: {st.session_state.player_power}",
        "Monanimal NFTs:"
    ]
    for mon in st.session_state.player_nfts:
        output.append(f"- {describe_monanimal(mon)}")
    return "\n".join(output)

def simulate_transaction(action):
    st.info(f"Simulating Monad transaction for {action}...")
    if st.sidebar.button("Sign Transaction", key=f"sign_{action}"):
        st.success("Transaction signed and confirmed!")
        return True
    return False

def hack_action():
    target = random.choice(["Low-Security Node", "High-Risk Vault", "Rival Overlord"])
    st.session_state.game_output.append(f"Hacking {target}...")
    success_chance = 50 + (st.session_state.player_power // 10)
    if random.randint(1, 100) <= success_chance:
        reward = random.randint(100, 500)
        st.session_state.player_mon += reward
        st.session_state.player_power += 10
        st.session_state.game_output.append(f"Success! Gained {reward} MON and 10 power.")
        st.success("Hack successful!")
    else:
        st.session_state.game_output.append("Hack failed! System crashing...")
        st.session_state.crashed = True
        st.error("System crashed!")

def recover_from_crash():
    if simulate_transaction("system recovery"):
        cost = 200
        if st.session_state.player_mon >= cost:
            st.session_state.player_mon -= cost
            st.session_state.game_output.append(f"Invested {cost} MON from liquidity pool.")
            with st.spinner("Recovering system..."):
                time.sleep(st.session_state.recovery_time)
            st.session_state.crashed = False
            st.session_state.game_output.append("System rebuilt! Back online.")
            st.success("Recovery complete!")
        else:
            st.session_state.game_output.append("Insufficient MON! Liquidating an NFT...")
            if st.session_state.player_nfts:
                liquidated = st.session_state.player_nfts.pop(random.randint(0, len(st.session_state.player_nfts)-1))
                st.session_state.player_mon += 300
                st.session_state.game_output.append(f"Liquidated {liquidated[0]} for 300 MON.")
                st.warning("NFT liquidated.")
            else:
                st.session_state.game_output.append("No NFTs to liquidate. Game over!")
                st.error("Game over!")
                return True
    return False

def stake_action(amount):
    if amount > 0 and amount <= st.session_state.player_mon and simulate_transaction("staking"):
        st.session_state.player_mon -= amount
        yield_bonus = amount // 10
        st.session_state.player_power += yield_bonus
        st.session_state.game_output.append(f"Staked {amount} MON. Gained {yield_bonus} power yield.")
        st.success("Stake successful!")

# Main App
st.title("Neon Cyber Overlords v1")
st.markdown("Rule the cyber metropolis with your Monanimal NFTs on Monad. Hack, stake, and recover wisely!")

# Power Progress Bar
st.progress(st.session_state.player_power / 1000)
st.caption(f"Power: {st.session_state.player_power}/1000 - Reach 1000 to win!")

# Game Log Container
with st.container():
    st.subheader("Game Log")
    log_container = st.container()
    with log_container:
        st.markdown('<div class="game-log">' + '<br>'.join(st.session_state.game_output) + '</div>', unsafe_allow_html=True)

# Crash Handling
if st.session_state.crashed:
    st.error("System Crashed! Recover to continue.")
    recover_from_crash()
else:
    # Random Event (triggered occasionally)
    if random.random() < 0.1:  # Lower chance for cleaner UX
        event = random.choice(["Airdrop! +100 MON", "Burn event: -50 MON", "Pool yield: +20 power"])
        st.session_state.game_output.append(f"Random Event: {event}")
        if "Airdrop" in event:
            st.session_state.player_mon += 100
            st.info("Airdrop received!")
        elif "Burn" in event:
            st.session_state.player_mon -= 50
            st.warning("Tokens burned!")
        elif "yield" in event:
            st.session_state.player_power += 20
            st.success("Yield gained!")

    # Win Check
    if st.session_state.player_power >= 1000:
        st.balloons()
        st.success("You've become the ultimate Neon Cyber Overlord! Game Won!")

# Sidebar for Actions
with st.sidebar:
    st.header("Actions")
    if st.button("Hack", key="hack_btn"):
        hack_action()
        st.rerun()
    stake_amount = st.number_input("MON to Stake", min_value=1, max_value=st.session_state.player_mon, value=100)
    if st.button("Stake", key="stake_btn"):
        stake_action(stake_amount)
        st.rerun()
    if st.button("Reset Game", key="reset_btn"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Inventory Expander
with st.expander("View Inventory"):
    st.text(display_inventory())
