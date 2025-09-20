
import streamlit as st
import pandas as pd
import random
from datetime import datetime
import os
import altair as alt

st.set_page_config(page_title="Trading Checklist", layout="wide")


# --- Sidebar Navigation ---
page = st.sidebar.radio("📌 Navigate", ["Checklist ✅", "Trade Journal 📒", "Stats Dashboard 📊", "Settings ⚙️"])

# --- Confetti Celebration ---
def confetti():
    st.balloons()

# --- Motivational Quotes ---
quotes = [
    "Protect your capital at all costs; profits will follow.",
    "The first rule of trading is not to lose money; the second rule is not to forget the first. – Warren Buffett",
    "Trade small, manage risk, survive to trade another day.",
    "Trading is not about being right all the time; it’s about managing probabilities.",
    "The market is never certain, but your preparation can be.",
    "Focus on the process, not the outcome; probability favors the disciplined.",
    "Discipline weighs ounces, regret weighs tons.",
    "Consistency beats brilliance in trading.",
    "Patience is not passive; it’s concentrated strength.",
    "Amateurs think about how much they can make. Professionals think about how much they can lose.",
    "Control your losses, and the wins will take care of themselves.",
    "Emotions are the enemy of consistent trading.",
    "Risk comes from not knowing what you are doing.",
    "Trade what you see, not what you think.",
    "Consistency is the key to trading success.",
    "Without discipline, a strategy is just a wish.",
    "Small losses protect big gains.",
    "A good trader focuses on probability, not certainty.",
    "Survival is the first step to profitability."
]


# ✅ Define checklist options globally
a_plus_option = "💯 🎯 ✅ A+ (BOF, BOT)"
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

# ========================== PAGE 1: CHECKLIST ==========================
if page == "Checklist ✅":
    st.title("📋 Entry Check")

    # --- Market Direction Section ---
    with st.container():
        market_dir = [
            "price > Open",
            "price > VWAP",
            "price > EMA20,STRND(3,5)"
        ]
        market_dir_vars = {}
        for item in market_dir:
            market_dir_vars[item] = st.checkbox(item, key=item)

        if all(market_dir_vars.values()):
            market_phase, market_img = "🟢 Bullish Market!", "bull.jpg"
        elif not any(market_dir_vars.values()):
            market_phase, market_img = "🔴 Bearish Market!", "bear.jpg"
        else:
            market_phase, market_img = "🟡 Reversal Phase!", "pig.jpg"

        st.markdown(f"<h2 style='text-align:center;color:#333;'>{market_phase}</h2>", unsafe_allow_html=True)
        st.image(market_img, width=220, use_container_width=False)

    # --- Checklist Section ---
    with st.container():
        # Initialize session_state
        for key in ["unchecked_options", "checked_options", "a_plus_checked"]:
            if key not in st.session_state:
                if key == "unchecked_options":
                    st.session_state.unchecked_options = full_options_list.copy()
                elif key == "checked_options":
                    st.session_state.checked_options = []
                else:
                    st.session_state.a_plus_checked = False

        def check_option(option):
            if option in st.session_state.unchecked_options:
                st.session_state.unchecked_options.remove(option)
                st.session_state.checked_options.append(option)

        def uncheck_option(option):
            if option in st.session_state.checked_options:
                st.session_state.checked_options.remove(option)
                st.session_state.unchecked_options.append(option)

        def restore_all():
            st.session_state.unchecked_options.extend(st.session_state.checked_options)
            st.session_state.checked_options = []

        def toggle_a_plus():
            st.session_state.a_plus_checked = not st.session_state.a_plus_checked

        total_options = len(full_options_list) + 1
        checked_count = len(st.session_state.checked_options) + (1 if st.session_state.a_plus_checked else 0)
        progress = checked_count / total_options
        st.progress(progress)
        st.caption(f"📊 Checklist Progress: **{checked_count}/{total_options}**")

        st.checkbox(a_plus_option, value=st.session_state.a_plus_checked, on_change=toggle_a_plus)

        # Status + confetti + tips
        if checked_count == total_options:
            st.markdown("<h3 style='color:green;text-align:center;'>🎉 SUCCESSFUL ✅ A+ Entry</h3>", unsafe_allow_html=True)
            confetti()
            st.info(random.choice(quotes))
        elif st.session_state.unchecked_options:
            st.markdown("<h3 style='color:red;text-align:center;'>⚠️ FAILURE ❌ Likely FOMO Entry</h3>", unsafe_allow_html=True)
            st.info(random.choice(quotes))
        else:
            st.markdown("<h3 style='color:orange;text-align:center;'>⚡ Partial Success: B Entry</h3>", unsafe_allow_html=True)
            st.info(random.choice(quotes))
            st.snow()

        
        # Two-column layout for checklist items
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🔴 Unchecked Items")
            for option in st.session_state.unchecked_options:
                st.button(option, key=f"unchecked_{option}", on_click=check_option, args=(option,))
            if not st.session_state.unchecked_options:
                st.info("All items checked!")

        # Mood Tracker
        st.subheader("📌 Mood Tracker")
        mood = st.radio("How do you feel?", ["HRule😃", "FOMO/Hope😐", "Revenge😡"], horizontal=True)

        # Notes + Profit Input
        notes = st.text_area("Notes", key="notes")
        profit_points = st.number_input("Profit/Loss Points", step=1)

        # Save Trade Button
        if st.button("💾 Save Trade"):
            # --- Grade Calculation ---
            if st.session_state.a_plus_checked and checked_count>=14:
                grade = "A+"
            elif checked_count < 13:
                grade = "Failure"
            else:
                grade = "B"

            record = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "market_phase": market_phase,
                "checklist_completion": f"{checked_count}/{total_options}",
                "mood": mood,
                "notes": notes,
                "profit_points": profit_points,
                "unchecked_items": ", ".join(st.session_state.unchecked_options),  # ✅ log unchecked
                "grade": grade  # ✅ new column
            }
            df = pd.DataFrame([record])
            file_exists = os.path.isfile("trades.csv")
            df.to_csv("trades.csv", mode="a", header=not file_exists, index=False)
            st.success("✅ Trade Record Saved!")

        with col2:
            st.subheader("🟢 Checked Items")
            for option in st.session_state.checked_options:
                st.button(option, key=f"checked_{option}", on_click=uncheck_option, args=(option,))
            st.button("♻️ Restore All", on_click=restore_all)
            if not st.session_state.checked_options:
                st.info("No items checked yet.")

# ========================== PAGE 2: TRADE JOURNAL ==========================
elif page == "Trade Journal 📒":
    st.title("📒 Trade Journal")
    try:
        df = pd.read_csv("trades.csv")
        st.dataframe(df)
        # 🔄 Reset option
        if st.button("🗑️ Reset Trades (Clear CSV)"):
            os.remove("trades.csv")
            st.success("✅ All trade records cleared!")
            st.rerun()
    except FileNotFoundError:
        st.info("No trades recorded yet.")

# ========================== PAGE 3: STATS DASHBOARD ==========================
elif page == "Stats Dashboard 📊":
    st.title("📊 Performance Dashboard")
    try:
        df = pd.read_csv("trades.csv")
        total_trades = len(df)
        
        # ✅ Success trades = profit > 0
        success_trades = len(df[df["profit_points"] > 0])
        
        st.metric("Total Trades", total_trades)
        st.metric("Profitable Trades", success_trades)
        
        if total_trades > 0:
            st.metric("Profit Ratio", f"{(success_trades/total_trades)*100:.2f}%")

            # ✅ Cumulative Profit Chart
            st.subheader("📈 Cumulative Profit Trend")
            df["cumulative_profit"] = df["profit_points"].cumsum()
            st.line_chart(df["cumulative_profit"])
            
             # Bar chart: Profit per Trade (wider bars & color-coded)
            st.subheader("📊 Profit per Trade")
            df["trade_number"] = range(1, len(df)+1)
            df["color"] = df["profit_points"].apply(lambda x: "green" if x >= 0 else "red")

            chart = alt.Chart(df).mark_bar(size=30).encode(  # size sets bar width
                x=alt.X("trade_number:O", title="Trade Number"),
                y=alt.Y("profit_points:Q", title="Profit/Loss Points"),
                color=alt.Color("color:N", scale=None, legend=None)
            ).properties(width=700, height=400)

            st.altair_chart(chart, use_container_width=True)
    except:
        st.info("No stats yet. Save some trades first.")

# ========================== PAGE 4: SETTINGS ==========================
elif page == "Settings ⚙️":
    st.title("⚙️ Settings & Tools")
    st.subheader("📈 Risk Calculator")
    capital = st.number_input("Capital (₹)", value=100000, step=1000)
    risk_pct = st.slider("Risk % per trade", 0.5, 5.0, 1.0)
    quantity = st.number_input("Quantity per lot", value=75)
    stop_loss = st.number_input("Stop-loss points", value=20)

    if st.button("🔢 Calculate Lot Size"):
        risk_amount = capital * (risk_pct/100)
        lot_size = risk_amount // (stop_loss * quantity)
        st.success(f"Allowed Risk: ₹{risk_amount:.2f}, Lot Size: {int(lot_size)} lots")
