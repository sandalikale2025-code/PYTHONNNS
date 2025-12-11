import streamlit as st

# Title
st.title("🎵 SPOTIFY LIKED SONGS")
st.write("=" * 40)

# Initial list
liked_songs = ["Here With Me", "Ordinary", "her", "Love You So", "If the World was ending"]

st.subheader("💚 Current Liked Songs")
st.write(liked_songs)
st.write("=" * 40)

# Add an item
add_item = "My Love"
liked_songs.append(add_item)

st.subheader("➕ Added Song")
st.write(f"Added: **{add_item}**")
st.write(liked_songs)
st.write("=" * 40)

# Remove an item
remove_item = "Love You So"
liked_songs.remove(remove_item)

st.subheader("🗑️ Removed Song")
st.write(f"Removed: **{remove_item}**")
st.write(liked_songs)
st.write("=" * 40)
