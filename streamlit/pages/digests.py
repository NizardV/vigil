import streamlit as st
import httpx
import os
from auth import get_cookies

API_URL = os.getenv("API_URL", "http://vigil_backend:8000/api")

st.set_page_config(page_title="Digests - Vigil", layout="wide")
st.title("Digests")

try:
    with httpx.Client() as client:
        themes = client.get(f"{API_URL}/themes/", cookies=get_cookies()).json()
        digests = client.get(f"{API_URL}/digests/", cookies=get_cookies()).json()
except Exception as e:
    st.error(f"Could not reach the API: {e}")
    st.stop()

theme_map = {t["name"]: t["id"] for t in themes}
theme_map_by_id = {t["id"]: t["name"] for t in themes}

# ── Déclenchement manuel ──────────────────────────────────
st.subheader("Trigger a digest")

if not themes:
    st.info("No themes configured yet.")
else:
    col1, col2 = st.columns([3, 1])
    selected_theme = col1.selectbox("Theme", list(theme_map.keys()))

    if col2.button("▶ Send now", use_container_width=True):
        with httpx.Client() as client:
            resp = client.post(
                f"{API_URL}/digests/trigger/{theme_map[selected_theme]}",
                cookies=get_cookies()
            )
        if resp.status_code == 200:
            st.success(f"Digest triggered for **{selected_theme}** — check your notifications!")
        else:
            st.error(f"Error: {resp.text}")

st.divider()

# ── Historique ────────────────────────────────────────────
st.subheader("History")

filter_options = ["All themes"] + [t["name"] for t in themes]
theme_filter = st.selectbox("Filter by theme", filter_options)

if theme_filter != "All themes":
    with httpx.Client() as client:
        digests = client.get(
            f"{API_URL}/digests/",
            params={"theme_id": theme_map[theme_filter]},
            cookies=get_cookies()
        ).json()

if not digests:
    st.info("No digests sent yet.")
else:
    for digest in digests:
        theme_name = theme_map_by_id.get(digest["theme_id"], "?")
        sent_at = digest["sent_at"][:16].replace("T", " ")
        st.markdown(f"**{theme_name}** — {sent_at} — `{digest['channel']}`")