import streamlit as st
import random
import time

# Monanimals list (text-based: name, base_color description, eye_color description, accessory_color description, stats)
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

# Initialize session state for game variables
if 'player_mon' not in st.session_state:
    st.session_state.player_mon = 1000  # Starting MON tokens
    st.session_state.player_nfts = random.sample(monanimals, 3)  # Start with 3 random Monanimal NFTs
    st.session_state.player_power = 100  # Starting power level
    st.session_state.crashed = False
    st.session_state.recovery_time = 10  # Simulated seconds for recovery
    st.session_state.game_output = []  # List to store game messages

def describe_monanimal(mon):
    name, base, eyes, acc, stats = mon
    return f"{name}: A fierce cyber beast with {base}, {eyes}, and {acc}. Stats: {stats}"

def display_inventory():
    output = [
        "\nYour Inventory:",
        f"MON Tokens: {st.session_state.player_mon}",
        f"Power Level: {st.session_state.player_power}",
        "Monanimal NFTs:"
    ]
    for mon in st.session_state.player_nfts:
        output.append(f"- {describe_monanimal(mon)}")
    return output

def simulate_transaction(action):
    # In web app, simulate with a button confirm
    st.write(f"Simulating Monad transaction for {action}...")
    if st.button("Sign Transaction"):
        st.write("Transaction signed and confirmed on Monad blockchain!")
        return True
    else:
        st.write("Awaiting signature...")
        return False

def hack_action():
    target = random.choice(["Low-Security Node", "High-Risk Vault", "Rival Overlord"])
    st.session_state.game_output.append(f"\nHacking {target}...")
    success_chance = 50 + (st.session_state.player_power // 10)
    if random.randint(1, 100) <= success_chance:
        reward = random.randint(100, 500)
        st.session_state.player_mon += reward
        st.session_state.player_power += 10
        st.session_state.game_output.append(f"Success! Gained {reward} MON and 10 power.")
    else:
        st.session_state.game_output.append("Hack failed! System crashing...")
        st.session_state.crashed = True

def recover_from_crash():
    if simulate_transaction("system recovery"):
        cost = 200
        if st.session_state.player_mon >= cost:
            st.session_state.player_mon -= cost
            st.session_state.game_output.append(f"Invested {cost} MON from liquidity pool. Waiting for recovery timer...")
            time.sleep(st.session_state.recovery_time)  # Note: time.sleep may not work well in Streamlit; simulate with message
            st.session_state.crashed = False
            st.session_state.game_output.append("System rebuilt! Back online.")
        else:
            st.session_state.game_output.append("Insufficient MON! Liquidating an NFT...")
            if st.session_state.player_nfts:
                liquidated = st.session_state.player_nfts.pop(random.randint(0, len(st.session_state.player_nfts)-1))
                st.session_state.player_mon += 300
                st.session_state.game_output.append(f"Liquidated {liquidated[0]} for 300 MON.")
            else:
                st.session_state.game_output.append("No NFTs to liquidate. Game over!")
                return True  # End game
    return False

def stake_action(amount):
    if amount <= st.session_state.player_mon and simulate_transaction("staking"):
        st.session_state.player_mon -= amount
        yield_bonus = amount // 10
        st.session_state.player_power += yield_bonus
        st.session_state.game_output.append(f"Staked {amount} MON. Gained {yield_bonus} power yield.")

# Main Streamlit App
st.title("Neon Cyber Overlords v1 - Text RPG")
st.write("Rule the cyber metropolis with your Monanimal NFTs on Monad blockchain.")
st.write("Click buttons to perform actions. Game state persists across interactions.")

# Display game output
for msg in st.session_state.game_output:
    st.write(msg)

if st.session_state.crashed:
    if recover_from_crash():
        st.write("Game Over!")
        st.stop()
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Hack"):
            hack_action()
            st.rerun()  # Refresh to show updates
    with col2:
        stake_amount = st.number_input("MON to Stake", min_value=1, max_value=st.session_state.player_mon)
        if st.button("Stake"):
            stake_action(stake_amount)
            st.rerun()
    with col3:
        if st.button("View Inventory"):
            inventory = display_inventory()
            st.session_state.game_output.extend(inventory)
            st.rerun()

    # Random event
    if random.random() < 0.2:
        event = random.choice(["Airdrop! +100 MON", "Burn event: -50 MON", "Pool yield: +20 power"])
        st.session_state.game_output.append(f"\nRandom Event: {event}")
        if "Airdrop" in event:
            st.session_state.player_mon += 100
        elif "Burn" in event:
            st.session_state.player_mon -= 50
        elif "yield" in event:
            st.session_state.player_power += 20
        st.rerun()

    # Win condition
    if st.session_state.player_power >= 1000:
        st.write("\nYou've amassed ultimate power! You are the Neon Cyber Overlord!")
        st.stop()

# Reset game button
if st.button("Reset Game"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
