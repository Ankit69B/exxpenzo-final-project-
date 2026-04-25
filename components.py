import streamlit as st
import os
import database

@st.dialog("Account Settings", width="large")
def settings_dialog():
    st.markdown("<div class='section-label'>⚙️  Configure Your Experience</div>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["👤  Profile", "🛠  Preferences", "🔐  Security"])

    with tab1:
        df_stats = database.get_user_expenses(st.session_state.username)
        c1,c2,c3 = st.columns(3)
        c1.metric("Total Entries", len(df_stats))
        c2.metric("Total Spent",   f"₹{df_stats['amount'].sum() if not df_stats.empty else 0}")
        c3.metric("Avg Spent",     f"₹{round(df_stats['amount'].mean(),2) if not df_stats.empty else 0}")
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🖼  Profile Photo"):
            uploaded = st.file_uploader("Upload image", type=["png","jpg","jpeg"])
            if uploaded:
                os.makedirs('profiles', exist_ok=True)
                with open(f"profiles/{st.session_state.username}.png","wb") as f:
                    f.write(uploaded.getbuffer())
                st.success("Profile photo updated!")
                st.rerun()
        with st.expander("✏️  Change Username"):
            with st.form("change_username"):
                new_un = st.text_input("New Username")
                if st.form_submit_button("Update", use_container_width=True):
                    if new_un and new_un != st.session_state.username:
                        if database.update_username(st.session_state.username, new_un):
                            old_p = f"profiles/{st.session_state.username}.png"
                            new_p = f"profiles/{new_un}.png"
                            if os.path.exists(old_p): os.rename(old_p, new_p)
                            st.session_state.username = new_un
                            st.success("Username updated!")
                            st.rerun()
                        else:
                            st.error("Username already taken.")

    with tab2:
        with st.expander("💰  Monthly Budget"):
            with st.form("budget_form"):
                cur_b = database.get_budget(st.session_state.username)
                nb = st.number_input("Budget (₹)", min_value=1, value=int(cur_b))
                if st.form_submit_button("Save", use_container_width=True):
                    database.update_budget(st.session_state.username, nb)
                    st.success(f"Budget set to ₹{nb}")
                    if f'budget_{st.session_state.username}' in st.session_state:
                         del st.session_state[f'budget_{st.session_state.username}']
        with st.expander("📥  Export CSV"):
            df_exp = database.get_user_expenses(st.session_state.username)
            st.download_button("⬇  Download CSV", data=df_exp.to_csv(index=False).encode(),
                file_name=f'{st.session_state.username}_expenses.csv', mime='text/csv', use_container_width=True)
        with st.expander("🗑  Reset All Data"):
            st.markdown("<p style='color:#ff4d6d;font-size:13px;'>⚠️ Permanently deletes all expenses.</p>", unsafe_allow_html=True)
            if st.button("Proceed with Reset", use_container_width=True):
                database.reset_user_data(st.session_state.username)
                st.success("Data reset.")
                st.rerun()

    with tab3:
        with st.expander("🔐  Change Password"):
            with st.form("change_pass"):
                np2 = st.text_input("New Password", type="password")
                cp2 = st.text_input("Confirm", type="password")
                if st.form_submit_button("Update Password", use_container_width=True):
                    if np2 == cp2 and np2:
                        database.change_password(st.session_state.username, np2)
                        st.success("Password updated!")
                    else:
                        st.error("Passwords don't match.")

@st.dialog("Transaction Ledger", width="large")
def manage_entries_dialog(df_current):
    if df_current.empty:
        st.info("No transactions found.")
        return
    emoji_map = {"Food":"🍔","Travel":"✈️","Shopping":"🛍️","Study":"📚","Other":"📦"}
    txn_opts = {}
    for _, row in df_current.iterrows():
        icon = emoji_map.get(row['category'], "💸")
        day_str = row.get('created_at', f"Day {row.get('day', '')}")
        if isinstance(day_str, str) and len(day_str) > 10:
             day_str = day_str[:10]
        txn_opts[f"{icon} {row['category']}  ·  ₹{row['amount']}  ({day_str})"] = row['id']
    
    sel_str = st.selectbox("Select Transaction", list(txn_opts.keys()), index=len(txn_opts)-1)
    sel_id  = txn_opts[sel_str]
    sel_row = df_current[df_current['id'] == sel_id].iloc[0]
    st.markdown("<hr style='border-color:var(--border,#141926);margin:16px 0;'>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.2, 1], gap="large")
    with c1:
        st.markdown("#### Edit Transaction")
        
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        photo_action = st.radio("Photo Action", ["Keep Current", "Capture", "Upload", "Remove"], horizontal=True, key=f"act_{sel_id}")
        
        img_bytes = None
        if photo_action == "Capture":
            new_img = st.camera_input("Record Item", label_visibility="collapsed", key=f"cam_{sel_id}")
            if new_img: img_bytes = new_img.getvalue()
        elif photo_action == "Upload":
            uploaded = st.file_uploader("Choose file", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed", key=f"upl_{sel_id}")
            if uploaded: img_bytes = uploaded.getvalue()
        elif photo_action == "Remove":
            img_bytes = "DELETE"

        with st.form(f"upd_form_{sel_id}"):
            cats = ["Food","Travel","Shopping","Study","Other"]
            try: ci = cats.index(sel_row['category'])
            except: ci = 4
            nc = st.selectbox("Category", cats, index=ci)
            na = st.number_input("Amount (₹)", min_value=1.0, value=float(sel_row['amount']), step=10.0)

            if st.form_submit_button("Save Changes", use_container_width=True):
                if photo_action == "Keep Current":
                    final_img = None
                elif photo_action == "Remove":
                    final_img = b""
                else:
                    final_img = img_bytes
                
                database.update_expense(sel_id, st.session_state.username, nc, na, final_img)
                st.success("Updated!")
                st.rerun()
    with c2:
        if sel_row.get('image'):
            st.markdown("#### Item Photo")
            st.image(sel_row['image'], use_container_width=True, caption="Captured Product/Receipt")
            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

        st.markdown("#### Delete Entry")
        st.markdown("<div class='danger-box'><h5>⚠️ Permanent Action</h5><p>This removes the entry from all charts and predictions permanently.</p></div>", unsafe_allow_html=True)
        with st.form(f"del_{sel_id}"):
            if st.form_submit_button("🚨 Delete Permanently", use_container_width=True):
                database.delete_expense(sel_id, st.session_state.username)
                st.success("Deleted.")
                st.rerun()
