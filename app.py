
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
    "The market is never certain, but your preparation can be.",
    "Focus on the process, not the outcome; probability favors the disciplined.",
    "Consistency beats brilliance in trading.",
    "Patience is not passive; it’s concentrated strength.",
    "Control your losses, and the wins will take care of themselves.",
    "Emotions are the enemy of consistent trading.",
    "Trade what you see, not what you think."
]

# ✅ Define checklist options globally
a_plus_option = "💯✅ A+(BOF,BOT)(2/3/4🎂)"
full_options_list = [
    "💪 C🕯️< 40 BOF/BOT/TOB/COB @Ilevel",
    "💪 Strend (5,3,1) 💪 Ema20(3) 💪 BB(3,1)",
    "💪 BNIFTY Strend(3)",
    "🎯 Fut Vol > AVG Vol",
    "🎯 Fut High Vol Delta & DPoc",
    "❤️ OPT Bold Candle",
    "❤️ OPT DPoc,Strnd,BB, vwap(opt)",
    "❤️ OPT RSI,OI",
    "😎 I’m a risk manager. Max risk is 2 Lot",
    """ 👍 Rev only @ interval not @ Rectangle👍 No after 3pm, ATR&ADX < T entry👍 No inside CPR, ORB, Rectangle entry👍 No pre BO & OBS (TL/IL)👍 Ccandle closed & <40👍 Max 1,2 Tcandle before Ccandle """
]

# ========================== PAGE 1: CHECKLIST ==========================
if page == "Checklist ✅":
    st.title("📋 Entry Check")

    # --- Market Direction Section ---
    with st.container():
        market_dir = ["price > Open", "price > VWAP", "price > EMA20,STRND(3,5)"]
        market_dir_vars = {}
        for item in market_dir:
            market_dir_vars[item] = st.checkbox(item, key=item)

        if all(market_dir_vars.values()):
            market_phase, market_img = "🟢 Bullish Market!", "bullg.gif"
        elif not any(market_dir_vars.values()):
            market_phase, market_img = "🔴 Bearish Market!", "bearg.gif"
        else:
            market_phase, market_img = "🟡 Reversal Phase!", "pig.jpg"

        st.markdown(f"<h2 style='text-align:center;color:#333;'>{market_phase}</h2>", unsafe_allow_html=True)
        #st.image(market_img, width=120, use_container_width=False)
        import base64

        with open(market_img, "rb") as f:
          data = f.read()
          b64_data = base64.b64encode(data).decode("utf-8")

        st.markdown(
        f'<img src="data:image/gif;base64,{b64_data}" width="150" style="display:block; margin:auto;">',
        unsafe_allow_html=True
        )
    # --- Checklist Section ---
    with st.container():
        # Initialize session_state
        for key in ["unchecked_options", "checked_options", "a_plus_checked",
                    "tzone_clicked", "tzone_mode", "final_clicked", "common_selected",
                    "qcheck_clicked"]:
            if key not in st.session_state:
                if key == "unchecked_options":
                    st.session_state.unchecked_options = full_options_list.copy()
                elif key == "checked_options":
                    st.session_state.checked_options = []
                elif key == "a_plus_checked":
                    st.session_state.a_plus_checked = False
                elif key == "common_selected":
                    st.session_state.common_selected = []
                else:
                    st.session_state[key] = False if "clicked" in key or "final" in key else None

        def check_option(option):
            if option in st.session_state.unchecked_options:
                st.session_state.unchecked_options.remove(option)
                st.session_state.checked_options.append(option)

        def uncheck_option(option):
            if option in st.session_state.checked_options:
                st.session_state.checked_options.remove(option)
                st.session_state.unchecked_options.append(option)

        # --- TZone + Mode + ILevel ---
        tzone_checked = st.checkbox("✅ Tzone", value=st.session_state.tzone_clicked, key="tzone")
        st.session_state.tzone_clicked = tzone_checked
        if not tzone_checked:
            st.session_state.tzone_mode = None
            st.session_state.final_clicked = False

        # Callback functions
        def select_continuous():
            st.session_state.mode_cont = True
            st.session_state.mode_rev = False
            st.session_state.tzone_mode = "Continuous"

        def select_reverse():
            st.session_state.mode_rev = True
            st.session_state.mode_cont = False
            st.session_state.tzone_mode = "Reverse"

        # Initialize keys
        if "mode_cont" not in st.session_state:
            st.session_state.mode_cont = False
        if "mode_rev" not in st.session_state:
            st.session_state.mode_rev = False
        if "tzone_mode" not in st.session_state:
            st.session_state.tzone_mode = None
        if tzone_checked:
          # Render checkboxes with callbacks
          col1, col2 = st.columns(2)
          col1.checkbox("Continuous", value=st.session_state.mode_cont, key="mode_cont", on_change=select_continuous)
          col2.checkbox("Reverse", value=st.session_state.mode_rev, key="mode_rev", on_change=select_reverse)
        # ILevel selection
        if st.session_state.tzone_mode:
            if st.session_state.tzone_mode == "Continuous":
                st.session_state.final_clicked = st.checkbox("Open, ORB, PDH/PDL, Interval, CPR,TLine,DH/DL", value=st.session_state.final_clicked, key="final_cont")
            else:
                st.session_state.final_clicked = st.checkbox("Interval", value=st.session_state.final_clicked, key="final_rev")
        total_options = len(full_options_list) + 1
        checked_count = len(st.session_state.checked_options) + (1 if st.session_state.a_plus_checked else 0)
        progress = checked_count / total_options
        st.progress(progress)
        st.caption(f"📊 Checklist Progress: **{checked_count}/{total_options}**")

        
        if tzone_checked and checked_count == total_options:
          st.markdown(
              "<h3 style='color:green;text-align:center;'>🎉 SUCCESSFUL ✅ A+ Entry</h3>",
              unsafe_allow_html=True
          )
          st.info("💫 Lot size: 2")
          st.markdown(
              """
              <style>
              .stApp {
                  background-color: #d4edda;  /* light green */
              }
              </style>
              """,
              unsafe_allow_html=True
          )
          confetti()

        elif tzone_checked and checked_count == (total_options-1) and not st.session_state.a_plus_checked:
            st.markdown(
                "<h3 style='color:orange;text-align:center;'>⚡ Partial Success: B Entry</h3>",
                unsafe_allow_html=True
            )
            st.info("💫 Lot size: 1")
            st.markdown(
                """
                <style>
                .stApp {
                    background-color: #fff3cd;  /* light yellow/orange */
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            st.snow()

        else:
            st.markdown(
                "<h3 style='color:red;text-align:center;'>⚠️ FAILURE ❌ Likely FOMO Entry</h3>",
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <style>
                .stApp {
                    background-color: #f8d7da;  /* light red */
                }
                </style>
                """,
                unsafe_allow_html=True
            )

        st.info(random.choice(quotes))
        # Only show checklist if TZone + Mode + ILevel selected
        show_checklist_content = st.session_state.tzone_clicked and st.session_state.tzone_mode and st.session_state.final_clicked
        # --- A+ Checkbox & Progress ---
        if show_checklist_content:
            st.checkbox(a_plus_option, value=st.session_state.a_plus_checked, key="a_plus", on_change=lambda: st.session_state.__setitem__("a_plus_checked", not st.session_state.a_plus_checked))
        
       

        # --- Failure / Success / B Entry ---
    
        # Two-column layout for unchecked/checked
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🔴 Unchecked Items")
            if show_checklist_content:
                for option in st.session_state.unchecked_options:
                    checked = st.checkbox(option, key=f"check_{option}"
                    if checked:
                        check_option(option)
            else:
                st.info("✅ Select TZone, Mode, and ILevel to see checklist.")

        with col2:
            st.subheader("🟢 Checked Items")
            if show_checklist_content:
                for option in st.session_state.checked_options:
                    st.button(option, key=f"checked_{option}", on_click=uncheck_option, args=(option,))
                st.button("♻️ Restore All", on_click=lambda: st.session_state.unchecked_options.extend(st.session_state.checked_options) or st.session_state.checked_options.clear())
                if not st.session_state.checked_options:
                    st.info("No items checked yet.")

        
        # --- Mood Tracker, Notes, Profit Input, Save Trade ---
        if show_checklist_content:
            st.subheader("📌 Mood Tracker")
            mood = st.radio("How do you feel?", ["HRule😃", "FOMO/Hope😐", "Revenge😡","Boredom😡"], horizontal=True)

            notes = st.text_area("Notes", key="notes")
            profit_points = st.number_input("Profit/Loss Points", step=1)

            if st.button("💾 Save Trade"):
                if st.session_state.a_plus_checked and checked_count == total_options:
                    grade = "A+"
                elif checked_count == (total_options-1) and not st.session_state.a_plus_checked:
                    grade = "B"
                else:
                    grade = "Failure"

                record = {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "market_phase": market_phase,
                    "checklist_completion": f"{checked_count}/{total_options}",
                    "mood": mood,
                    "notes": notes,
                    "profit_points": profit_points,
                    "unchecked_items": ", ".join(st.session_state.unchecked_options),
                    "grade": grade
                }
                df = pd.DataFrame([record])
                file_exists = os.path.isfile("trades.csv")
                df.to_csv("trades.csv", mode="a", header=not file_exists, index=False)
                st.success("✅ Trade Record Saved!")

# Pages 2,3,4 remain same as before


# ========================== PAGE 2: TRADE JOURNAL ==========================
elif page == "Trade Journal 📒":
    st.title("📒 Trade Journal")
    try:
        df = pd.read_csv("trades.csv")
        st.dataframe(df)
        if st.button("🗑️ Reset Trades (Clear CSV)"):
            os.remove("trades.csv")
            st.success("✅ All trade records cleared!")
            st.experimental_rerun()
    except FileNotFoundError:
        st.info("No trades recorded yet.")

# ========================== PAGE 3: STATS DASHBOARD ==========================
elif page == "Stats Dashboard 📊":
    st.title("📊 Performance Dashboard")
    try:
        df = pd.read_csv("trades.csv")
        total_trades = len(df)
        success_trades = len(df[df["profit_points"] > 0])
        st.metric("Total Trades", total_trades)
        st.metric("Profitable Trades", success_trades)
        if total_trades > 0:
            st.metric("Profit Ratio", f"{(success_trades/total_trades)*100:.2f}%")
            st.subheader("📈 Cumulative Profit Trend")
            df["cumulative_profit"] = df["profit_points"].cumsum()
            st.line_chart(df["cumulative_profit"])
            st.subheader("📊 Profit per Trade")
            df["trade_number"] = range(1, len(df)+1)
            df["color"] = df["profit_points"].apply(lambda x: "green" if x >= 0 else "red")
            chart = alt.Chart(df).mark_bar(size=30).encode(
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












