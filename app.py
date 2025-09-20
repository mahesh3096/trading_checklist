
import streamlit as st

#list of Market direction
st.set_page_config(page_title="Trading Checklist", layout="centered")
st.title("Trading Checklist ✅")
market_dir ={
    f'price > Open',
    f'price > VWAP',
    f'price > EMA20,STRND(3,5)'
    }
#engine = create_engine('sqlite:///example.db')  # Replace with your DB connection string
market_dir_vars = {}
for item in market_dir:
    market_dir_vars[item] = st.checkbox(item, key=item)
market_phase=''
market_img=""
if (market_dir_vars['price > Open']==True and market_dir_vars['price > VWAP']==True and market_dir_vars['price > EMA20,STRND(3,5)']==True):
    market_phase="Bullish market !"
    market_img='bull.jpg'
elif (market_dir_vars['price > Open']==False and market_dir_vars['price > VWAP']==False and market_dir_vars['price > EMA20,STRND(3,5)']==False):
    market_phase="Bearish market !"
    market_img='bear.jpg'
    
else:
    market_phase="Reversal phase !"
    market_img='pig.jpg'
st.markdown(f"<h1 style='color: #FF6347;'>{market_phase}</h1>", unsafe_allow_html=True)
st.image(market_img, width=200)


# Define the fixed A+ option
a_plus_option = "💯 🎯 ✅ A+ (BOF, BOT)"

# Define the full list of options (excluding the A+ option)
full_options_list = [
    "😎 I’m a risk manager first, and a trader second",
    "✅ Tzone",
    "💪 Strend (5,3,1)",
    "💫 Ema20(3)",
    "🎯 Spot 🎯",
    "🎯 Future 🎯",
    "🎯 Option 🎯",
    "💫DPoc,Strnd,vwap(opt)",
    "💫RSI,OI",
    "👍 Ccandle closed & <40",
    "👍 No pre BO & OBS (TL/IL)",
    "👍 No inside CPR, ORB Rectangle entry",
    "👍 Max 1,2 Tcandle before Ccandle",
    "👍 Rev only @ interval not @ Rectangle",
]

# Initialize session state for options if they don't exist, ensuring all options are present
if 'unchecked_options' not in st.session_state:
    st.session_state.unchecked_options = full_options_list.copy()
if 'checked_options' not in st.session_state:
    st.session_state.checked_options = []

if 'a_plus_checked' not in st.session_state:
    st.session_state.a_plus_checked = False


# Function to move option to checked list
def check_option(option):
    if option in st.session_state.unchecked_options:
        st.session_state.unchecked_options.remove(option)
        st.session_state.checked_options.append(option)

# Function to move option to unchecked list
def uncheck_option(option):
    if option in st.session_state.checked_options:
        st.session_state.checked_options.remove(option)
        st.session_state.unchecked_options.append(option)

# Function to move all checked items back to unchecked
def restore_all():
    st.session_state.unchecked_options.extend(st.session_state.checked_options)
    st.session_state.checked_options = []

# Function to toggle A+ option
def toggle_a_plus():
    st.session_state.a_plus_checked = not st.session_state.a_plus_checked


# Calculate counts
total_options = len(full_options_list)
checked_count = len(st.session_state.checked_options) + (1 if st.session_state.a_plus_checked else 0)


# Determine status based on unchecked options and A+ option
all_ok = not st.session_state.unchecked_options and st.session_state.a_plus_checked
failure= st.session_state.unchecked_options
# --- Dynamic page background color and styling ---
if all_ok:
    bg_color = "#d4edda"  # Light green
elif failure:
    bg_color = "#f8d7da"  # Light red
else:
    bg_color = "#FFDB58 "  # Light yellow

page_bg = f"""
<style>
    .stApp {{
        background-color: {bg_color};
        font-size: 25px; /* Increased font size for the entire app */
        color: black; /* Set text color to black */
    }}
    .stApp * {{ /* Apply font size and color to all elements within stApp */
        font-size: 25px !important;
        color: black !important;
    }}
    .stCheckbox label {{
        font-size: 25px !important;
    }}
    /* Style for Streamlit buttons */
    div.stButton > button:first-child {{
        background-color: white;
        color: black;
    }}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Display checked count
st.subheader(f"Checked: {checked_count}/{total_options + 1}") # +1 for the A+ option

# Display A+ option separately
st.checkbox(a_plus_option, value=st.session_state.a_plus_checked, on_change=toggle_a_plus)


# Status message
if all_ok:
    st.success("🎉 SUCCESSFUL ✅ A+ Entry ")
elif st.session_state.unchecked_options :
    st.error("⚠️ FAILURE FOMO Entry ❌ Definetly fail 💯 ")
else:
    st.info("Partial successful ✅ B Entry")

# Display unchecked options
st.subheader("Unchecked Items")
if st.session_state.unchecked_options:
    for option in st.session_state.unchecked_options:
        if st.button(option, key=f"unchecked_{option}"):
            check_option(option)
            st.rerun()
else:
    st.info("All items in the main checklist are checked!")

st.markdown("---") # Add a horizontal rule for visual separation

# Display checked options
st.subheader("Checked Items")
if st.session_state.checked_options:
    for option in st.session_state.checked_options:
        if st.button(option, key=f"checked_{option}"):
            uncheck_option(option)
            st.rerun()
    st.button("Restore All to Unchecked", on_click=restore_all)
else:

    st.info("No items are checked yet.")


