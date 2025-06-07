import streamlit as st
from api import ArenaAPI
from streamlit_autorefresh import st_autorefresh
from user_lists import whitelisted

st.set_page_config(
    page_title="Token Polling",
    page_icon="⚔️",
)

if 'polling_active' not in st.session_state:
    st.session_state.polling_active = False
if 'seen_groups' not in st.session_state:
    st.session_state.seen_groups = {}
if 'token_logs' not in st.session_state:
    st.session_state.token_logs = []

st.title("📡 Polling")

col1, col2 = st.columns(2)
if col1.button("▶️ START"):
    st.session_state.polling_active = True
if col2.button("⏹️ STOP"):
    st.session_state.polling_active = False

if st.session_state.polling_active:
    st_autorefresh(interval=2000, limit=None, key="polling_refresh")

    arena = ArenaAPI()
    tokens = arena.get_groups_plus_recent()

    for tok in tokens:
        if tok.group_id not in st.session_state.seen_groups:
            st.session_state.seen_groups[tok.group_id] = tok
            nb_tokens = 0
            is_farmer = False
            is_in_whitelist = True if tok.twitter_handle in whitelisted else False

            if tok.twitter_handle:
                created = arena.get_groups_plus("creator_twitter_handle", tok.twitter_handle)
                nb_tokens = len(created) if created else 0
                is_farmer = nb_tokens > 5

            st.session_state.token_logs.insert(0, {
                "symbol": tok.symbol,
                "name": tok.name,
                "url": f"https://arena.trade/token/{tok.token_contract}",
                "twitter": tok.twitter_handle,
                "x_url": f"https://x.com/{tok.twitter_handle}",
                "followers": tok.twitter_followers,
                "market_cap": tok.market_cap_usd,
                "bonding_curve": tok.bonding_curve,
                "farmer": is_farmer,
                "whitelist": is_in_whitelist,
                "nb_tokens": nb_tokens
            })

st.markdown("### Logs")
for log in st.session_state.token_logs[:50]:
    with st.container():
        st.markdown(f"""
🪙 **{log['symbol']}** — *{log['name']}*  
🔗 [Voir sur Arena]({log['url']})  
👤 [@{log['twitter']}]({log['x_url']}) — {log['followers']} followers   
📈 Bonding Curve: **{log['bonding_curve']:.2f}%** — Market Cap: **${log['market_cap']:.2f}**
""")
        if log['farmer']:
            st.markdown(f"⚠️ **FARMER détecté** : {log['nb_tokens']} tokens créés", unsafe_allow_html=True)
        if log["whitelist"]:
            st.markdown(f"✅⁉️ ** {log['twitter']} est dans la whitelist**", unsafe_allow_html=True)
        st.markdown("---")
