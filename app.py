import streamlit as st
import pandas as pd
import numpy as np
import os
import base64

import database
import styles
import components
import charts

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Expenzo · Smart Expense OS", layout="wide", page_icon="💎")

styles.apply_global_styles()
# styles.apply_custom_cursor(enable=True) # Un-comment to enable custom js cursor

database.create_tables()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# ════════════════════════════════════════════
#  LOGIN
# ════════════════════════════════════════════
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.3, 1])
    with col:
        st.markdown("""
        <div class='login-card'>
            <div class='login-logo'>💎 Expenzo</div>
            <div class='login-headline'>Your Finance OS</div>
            <div class='login-sub'>Track, predict, and master your spending</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:1px;background:var(--border,#1c2333);margin:-1px 0 0;border-radius:0 0 24px 24px;'></div>", unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔐  Sign In", "✨  Create Account"])

        with tab1:
            with st.form("login_form"):
                user = st.text_input("Username", placeholder="Enter username")
                pwd  = st.text_input("Password", type="password", placeholder="Enter password")
                if st.form_submit_button("Sign In →", use_container_width=True):
                    if database.login_user(user, pwd):
                        st.session_state.logged_in = True
                        st.session_state.username  = user
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please try again.")

        with tab2:
            with st.form("signup_form", clear_on_submit=True):
                nu = st.text_input("Username", placeholder="Choose a username")
                np_pw = st.text_input("Password", type="password", placeholder="Min. 4 characters")
                cp = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
                if st.form_submit_button("Create Account →", use_container_width=True):
                    if np_pw != cp:
                        st.error("Passwords don't match.")
                    elif len(np_pw) < 4:
                        st.error("Password must be at least 4 characters.")
                    elif not nu.strip():
                        st.error("Username cannot be empty.")
                    else:
                        if database.add_user(nu, np_pw):
                            st.success("Account created! Switch to Sign In.")
                        else:
                            st.warning("Username already taken.")

# ════════════════════════════════════════════
#  MAIN APP
# ════════════════════════════════════════════
else:
    if "page" not in st.session_state or st.session_state.page == "Settings":
        st.session_state.page = "Dashboard"

    # ── App Header ──
    st.markdown("""
    <div style='display:flex;align-items:center;gap:12px;padding:24px 0 8px;'>
        <span style='font-family:"Space Mono",monospace;font-size:15px;font-weight:700;color:#00f5c4;letter-spacing:2px;'>💎 EXPENZO</span>
        <span style='flex:1;height:1px;background:rgba(255,255,255,0.06);'></span>
    </div>
    """, unsafe_allow_html=True)

    # ── Navigation ──
    st.markdown("<div class='nav-label'>Navigation</div>", unsafe_allow_html=True)
    _, nav_col, _ = st.columns([1, 10, 1])
    with nav_col:
        try:
            c1,c2,c3,c4,c5 = st.columns(5, gap="small", vertical_alignment="center")
        except TypeError:
            c1,c2,c3,c4,c5 = st.columns(5, gap="small")

        with c1:
            if st.button("📊  Dashboard", use_container_width=True): st.session_state.page = "Dashboard"
        with c2:
            if st.button("➕  Add Expense", use_container_width=True): st.session_state.page = "Add Expense"
        with c3:
            if st.button("📜  History", use_container_width=True): st.session_state.page = "History"
        with c4:
            if st.button("⚙️  Settings", use_container_width=True): components.settings_dialog()
        with c5:
            # Load and encode user avatar for CSS injection
            pic = f"profiles/{st.session_state.username}.png"
            if os.path.exists(pic):
                with open(pic,"rb") as img:
                    b64 = base64.b64encode(img.read()).decode()
                st.markdown(f"""
                <style>
                [data-testid="stPopover"] > div:first-child > button::before {{
                    content: "";
                    display: inline-block;
                    width: 20px;
                    height: 20px;
                    background-image: url('data:image/png;base64,{b64}');
                    background-size: cover;
                    border-radius: 50%;
                    margin-right: 10px;
                    vertical-align: middle;
                    border: 1px solid rgba(0,245,196,0.3);
                }}
                </style>
                """, unsafe_allow_html=True)
                av_html = f"<img src='data:image/png;base64,{b64}' style='width:60px;height:60px;border-radius:50%;margin-bottom:12px;border:2px solid var(--mint);object-fit:cover;'/>"
            else:
                av_html = "<div style='font-size:40px;margin-bottom:8px;'>👤</div>"
            
            with st.popover(f"{st.session_state.username}", use_container_width=True):
                st.markdown(f"<div style='text-align:center;'>{av_html}<br><b>{st.session_state.username}</b></div>", unsafe_allow_html=True)
                st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
                if st.button("🚪  Logout Session", use_container_width=True, type="primary"):
                    st.session_state.logged_in = False
                    st.session_state.username = None
                    st.rerun()

    choice = st.session_state.page
    st.markdown("---")

    # Fetch data: df_all for calculation, df for display limits
    df_all = database.get_user_expenses(st.session_state.username)
    df = df_all.tail(50)

    # ════════════════════════════════
    #  DASHBOARD
    # ════════════════════════════════
    if choice == "Dashboard":
        st.markdown(f"""
        <div class='page-title'>Good day, <span class='mint'>{st.session_state.username}</span> 👋</div>
        <div class='page-sub'>Here's your financial overview at a glance.</div>
        """, unsafe_allow_html=True)

        if 'v_mode' not in st.session_state:
            st.session_state['v_mode'] = 'Categories'

        if df_all.empty:
            st.warning("No expense data yet. Add your first entry to get started.")
            st.stop()

        # ── Stat Cards ──
        st.markdown("<div class='section-label'>Overview</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-label'>Total Spent</div>
                <div class='stat-value'><span class='stat-accent'>₹</span>{df_all['amount'].sum():,.0f}</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-label'>Average per Entry</div>
                <div class='stat-value'><span class='stat-accent'>₹</span>{df_all['amount'].mean():,.2f}</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-label'>Total Entries</div>
                <div class='stat-value' style='font-size:40px;'>{len(df_all)}</div>
            </div>""", unsafe_allow_html=True)
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            if st.button("⚙️  Manage Entries", use_container_width=True):
                components.manage_entries_dialog(df_all)

        st.markdown("---")

        # ── Charts ──
        h_col1, h_col2 = st.columns([4, 1])
        with h_col1:
            st.markdown("<div class='section-label'>Analytics</div>", unsafe_allow_html=True)
        with h_col2:
            st.session_state['v_mode'] = st.selectbox("View", ["Categories", "Frequency"], label_visibility="collapsed")
            
        st.caption(f"Currently viewing <b class='mint'>{st.session_state.v_mode}</b> profile — hover for deep details.")

        # Display chart based on mode using df_all
        if st.session_state['v_mode'] == "Categories":
            st.plotly_chart(charts.build_pie_chart(df), use_container_width=True, config={'displayModeBar': False})
        else:
            st.plotly_chart(charts.build_bar_chart(df), use_container_width=True, config={'displayModeBar': False})

        st.plotly_chart(charts.build_trend_chart(df), use_container_width=True, config={'displayModeBar': False})
        st.markdown("---")

        # ── ML Engine ──
        st.markdown("<div class='section-label'>🧠 ML Engine</div>", unsafe_allow_html=True)
        st.caption("Statistical modeling, outlier detection, and behavioral profiling.")

        if len(df_all) >= 3:
            t1,t2,t3,t4 = st.tabs(["🕵️ Anomaly Detector","🔮 Forecast","👤 Behavior Profile","📡 Telemetry"])

            with t1:
                mean_e = df_all['amount'].mean()
                std_e  = df_all['amount'].std() if not pd.isna(df_all['amount'].std()) else 0
                thr    = mean_e + (2.0 * std_e)
                anom   = df_all[df_all['amount'] > thr]
                ca, cs = st.columns([2.2,1])
                with cs:
                    st.markdown(f"""
                    <div class='stat-card'>
                        <div class='stat-label'>2σ Threshold</div>
                        <div class='stat-value' style='font-size:26px;color:#ff4d6d;'>₹{thr:,.0f}</div>
                        <div style='color:#6b7a99;font-size:12px;margin-top:8px;'>Current outlier boundary</div>
                    </div>""", unsafe_allow_html=True)
                    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
                    if not anom.empty:
                        st.error(f"Intercepted {len(anom)} anomalies.")
                    else:
                        st.success("Clean stream.")

                with ca:
                    st.plotly_chart(charts.build_anomaly_chart(df_all, thr), use_container_width=True, config={'displayModeBar': False})

            with t2:
                fp, momentum = charts.build_forecast_chart(df_all)
                c_f1, c_f2 = st.columns([1, 3])
                with c_f1:
                    m_col = "#00f5c4" if momentum < 0 else "#ff4d6d"
                    st.markdown(f"""
                    <div class='stat-card' style='height:100%; display:flex; flex-direction:column; justify-content:center;'>
                        <div class='stat-label'>Momentum</div>
                        <div class='stat-value' style='color:{m_col}; font-size:24px;'>{"+" if momentum > 0 else ""}{momentum:.1f}%</div>
                        <p style='color:#6b7a99; font-size:11px; margin-top:10px;'>{ "Projected Acceleration" if momentum > 0 else "Optimized Decay"}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with c_f2:
                    st.plotly_chart(fp, use_container_width=True, config={'displayModeBar': False})

            with t3:
                avg = df_all['amount'].mean()
                q75 = df_all['amount'].quantile(0.75)
                q25 = df_all['amount'].quantile(0.25)
                
                if avg > q75:
                    beh, desc, col = "Aggressive Spender 🚨", "High-velocity outflow detected. Consider activating budget limits.", "#ff4d6d"
                elif avg >= q25:
                    beh, desc, col = "Balanced Consumer ⚖️", "Spending equilibrium maintained. Low variance footprint.", "#f5a623"
                else:
                    beh, desc, col = "Optimized Saver 🏦", "Exceptional capital retention — operating well below thresholds.", "#00f5c4"
                st.markdown(f"""
                <div class='behavior-card' style='border-color:{col};background:rgba(255,255,255,0.03);'>
                    <div style='font-family:"Space Mono",monospace;font-size:11px;font-weight:700;letter-spacing:2px;color:{col};text-transform:uppercase;margin-bottom:12px;'>Behavioral Classification</div>
                    <div style='font-size:26px;font-weight:800;color:{col};margin-bottom:8px;'>{beh}</div>
                    <div style='font-family:"Space Mono",monospace;font-size:24px;font-weight:700;color:#e8ecf4;margin-bottom:12px;'>₹{avg:.2f} avg</div>
                    <div style='color:#6b7a99;font-size:14px;line-height:1.6;'>{desc}</div>
                </div>""", unsafe_allow_html=True)

            with t4:
                df_t = df_all.copy()
                df_t['Rolling'] = df_t['amount'].rolling(3).mean()
                roll = df_t['Rolling'].dropna()
                cs1, cs2, cs3 = st.columns(3)
                
                cur_budget = database.get_budget(st.session_state.username)
                total_spent = df_all['amount'].sum()
                
                with cs1:
                    if len(roll)>=2 and roll.iloc[-1] > roll.iloc[-2]:
                        st.markdown("<div class='signal-up'><div style='font-size:24px;'>📈</div><div style='font-weight:800;color:#ff4d6d;font-size:14px;margin:8px 0 2px;'>UP-TREND</div><div style='color:#6b7a99;font-size:11px;'>Momentum Up</div></div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='signal-ok'><div style='font-size:24px;'>📉</div><div style='font-weight:800;color:#00f5c4;font-size:14px;margin:8px 0 2px;'>STABLE</div><div style='color:#6b7a99;font-size:11px;'>Burn rate Low</div></div>", unsafe_allow_html=True)
                with cs2:
                    if total_spent > cur_budget:
                        st.markdown(f"<div class='signal-up'><div style='font-size:24px;'>🚨</div><div style='font-weight:800;color:#ff4d6d;font-size:14px;margin:8px 0 2px;'>BREACHED</div><div style='color:#6b7a99;font-size:11px;'>Cap ₹{cur_budget:,.0f}</div></div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='signal-ok'><div style='font-size:24px;'>✅</div><div style='font-weight:800;color:#00f5c4;font-size:14px;margin:8px 0 2px;'>SECURE</div><div style='color:#6b7a99;font-size:11px;'>Safe Budget</div></div>", unsafe_allow_html=True)
                with cs3:
                    volatility = (df_all['amount'].std() / df_all['amount'].mean()) * 100 if df_all['amount'].mean() > 0 else 0
                    if volatility > 50:
                        st.markdown("<div class='signal-up'><div style='font-size:24px;'>🌀</div><div style='font-weight:800;color:#ff4d6d;font-size:14px;margin:8px 0 2px;'>TURBULENT</div><div style='color:#6b7a99;font-size:11px;'>High Variance</div></div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='signal-ok'><div style='font-size:24px;'>💎</div><div style='font-weight:800;color:#00f5c4;font-size:14px;margin:8px 0 2px;'>STABLE</div><div style='color:#6b7a99;font-size:11px;'>Clear Pattern</div></div>", unsafe_allow_html=True)
        else:
            st.info("Add 3+ transactions to unlock the ML engine.")

        st.markdown("---")

        # ── Smart Analysis ──
        st.markdown("<div class='section-label'>Smart Analysis</div>", unsafe_allow_html=True)
        
        if len(df_all) > 1:
            mid = len(df_all)//2
            prev_df = df_all.iloc[:mid]
            curr_df = df_all.iloc[mid:]
            
            prev_cat = prev_df.groupby('category')['amount'].sum()
            curr_cat = curr_df.groupby('category')['amount'].sum()
            
            drift_df = pd.DataFrame({'Previous': prev_cat, 'Current': curr_cat}).fillna(0)
            drift_df['Drift'] = drift_df['Current'] - drift_df['Previous']
            drift_df = drift_df.reset_index()
            
            sa1, sa2 = st.columns([1.5, 1])
            with sa1:
                st.markdown("#### 🔄 Category Drift")
                st.plotly_chart(charts.build_drift_chart(drift_df), use_container_width=True, config={'displayModeBar': False})
                
            with sa2:
                st.markdown("#### ✨ Automated Insights")
                if not drift_df.empty:
                    growth = drift_df.loc[drift_df['Drift'].idxmax()]
                    savings = drift_df.loc[drift_df['Drift'].idxmin()]
                    
                    if growth['Drift'] > 0:
                        st.markdown(f"""
                        <div style='background: rgba(255,77,109,0.1); border-radius:12px; padding:15px; border:1px solid rgba(255,77,109,0.2); margin-bottom:12px;'>
                            <div style='font-size:11px; color:#ff4d6d; font-weight:700; letter-spacing:1px;'>🚀 RAPID GROWTH</div>
                            <div style='color:#e8ecf4; font-size:14px; margin-top:5px;'><b>{growth['category']}</b> spending surged by <b style='color:#ff4d6d;'>₹{growth['Drift']:.0f}</b>.</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if savings['Drift'] < 0:
                        st.markdown(f"""
                        <div style='background: rgba(0,245,196,0.1); border-radius:12px; padding:15px; border:1px solid rgba(0,245,196,0.2);'>
                            <div style='font-size:11px; color:#00f5c4; font-weight:700; letter-spacing:1px;'>📉 OPTIMIZED</div>
                            <div style='color:#e8ecf4; font-size:14px; margin-top:5px;'>Saved <b style='color:#00f5c4;'>₹{abs(savings['Drift']):.0f}</b> on <b>{savings['category']}</b> this period.</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("No significant savings detected this period.")
        else:
            st.info("Insufficient data for drift analysis.")

        st.markdown("---")

        # ── Budget Dynamics ──
        st.markdown("<div class='section-label'>🎯 Budget Telemetry</div>", unsafe_allow_html=True)
        
        now       = pd.Timestamp.now()
        day       = now.day
        days_m    = now.days_in_month
        days_rem  = max(1, days_m - day + 1)

        spent     = df_all['amount'].sum()
        cur_b     = database.get_budget(st.session_state.username)
        
        b_col1, b_col2 = st.columns([1, 2.5])
        with b_col1:
            budget = st.select_slider("Budget Cap (₹)", options=[500, 1000, 2000, 5000, 10000, 20000, 50000, 100000], value=cur_b)
            if budget != cur_b:
                 database.update_budget(st.session_state.username, budget)
                 cur_b = budget
            
            rem      = budget - spent
            pct      = (spent / budget)*100 if budget > 0 else 0
            burn     = max(0, rem / days_rem)
            
            if pct > 100: 
                pace_st, pace_col = "LIMIT BREACHED 🚨", "#ff4d6d"
            else: 
                pace_st, pace_col = "SAFE ZONE ✅", "#00f5c4"
            
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.03); border:1px solid var(--border); border-radius:12px; padding:16px; margin-top:12px;'>
                <div style='font-size:10px; color:#6b7a99; font-weight:700; letter-spacing:1px; margin-bottom:5px;'>DAILY ALLOWANCE</div>
                <div style='font-family:"Space Mono",monospace; font-size:22px; font-weight:700; color:{pace_col};'>₹{burn:.0f}</div>
                <div style='font-size:11px; color:#6b7a99; margin-top:8px;'>{pace_st}</div>
            </div>
            """, unsafe_allow_html=True)

        with b_col2:
            st.plotly_chart(charts.build_gauge_chart(spent, budget), use_container_width=True, config={'displayModeBar': False})

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        st.markdown("<span style='font-size:13px; color:#6b7a99; font-weight:600;'>📊 CUMULATIVE TRAJECTORY</span>", unsafe_allow_html=True)
        st.plotly_chart(charts.build_burn_chart(df_all, budget), use_container_width=True, config={'displayModeBar': False})


    # ════════════════════════════════
    #  ADD EXPENSE
    # ════════════════════════════════
    elif choice == "Add Expense":
        st.markdown("""
        <div class='page-title'>Add Expense</div>
        <div class='page-sub'>Log a new transaction to your tracker.</div>
        """, unsafe_allow_html=True)
        _, fc, _ = st.columns([1, 2, 1])
        with fc:
            st.markdown("<div class='section-label'>📸 Photo Evidence</div>", unsafe_allow_html=True)
            photo_source = st.radio("Source", ["None", "Capture Photo", "Upload File"], horizontal=True, label_visibility="collapsed", key="add_source")
            
            img_bytes = None
            if photo_source == "Capture Photo":
                photo = st.camera_input("Take Pic", label_visibility="collapsed", key="add_cam")
                if photo: img_bytes = photo.getvalue()
            elif photo_source == "Upload File":
                up_file = st.file_uploader("Pick Image", type=['png','jpg','jpeg'], label_visibility="collapsed", key="add_upl")
                if up_file: img_bytes = up_file.getvalue()
            
            st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

            with st.form("add_expense_form", clear_on_submit=True):
                st.markdown("<div class='section-label'>Transaction Details</div>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    amt = st.number_input("Amount (₹)", min_value=1, step=10)
                with c2:
                    cat = st.selectbox("Category", ["Food","Travel","Shopping","Study","Other"])
                
                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                if st.form_submit_button("Add to Tracker →", use_container_width=True):
                    database.add_expense(st.session_state.username, pd.Timestamp.now().day, cat, amt, img_bytes)
                    st.success("✅ Expense logged successfully!")
                    if img_bytes:
                        st.balloons()

    # ════════════════════════════════
    #  HISTORY
    # ════════════════════════════════
    elif choice == "History":
        st.markdown("""
        <div class='page-title'>Transaction Ledger</div>
        <div class='page-sub'>Advanced historical analysis and record management.</div>
        """, unsafe_allow_html=True)
        
        if df_all.empty:
            st.info("No records found in the ledger.")
            st.stop()

        st.markdown("<div class='section-label'>Ledger Overview</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-label'>Lifetime Records</div>
                <div class='stat-value'>{len(df_all)}</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-label'>Peak Expense</div>
                <div class='stat-value' style='color:#f5a623;'><span class='stat-accent'>₹</span>{df_all['amount'].max():,.0f}</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-label'>Total Velocity</div>
                <div class='stat-value'><span class='stat-accent'>₹</span>{df_all['amount'].sum():,.0f}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<div class='section-label'>Interactive Filters</div>", unsafe_allow_html=True)
        f_col1, f_col2, f_col3 = st.columns([2, 2, 1])
        with f_col1:
            cat_list = ["All Categories"] + sorted(df_all['category'].unique().tolist())
            f_cat = st.selectbox("Category Filter", cat_list)
        with f_col2:
            f_amt = st.slider("Amount Range (₹)", 0, int(df_all['amount'].max()), (0, int(df_all['amount'].max())))
        with f_col3:
            st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
            if st.button("⚙️ Manage Selection", use_container_width=True):
                components.manage_entries_dialog(df_all)

        filtered_df = df.copy()
        if f_cat != "All Categories":
            filtered_df = filtered_df[filtered_df['category'] == f_cat]
        filtered_df = filtered_df[(filtered_df['amount'] >= f_amt[0]) & (filtered_df['amount'] <= f_amt[1])]

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-label'>Historical Grid</div>", unsafe_allow_html=True)
        
        display_df = filtered_df.copy()
        if not display_df.empty:
            display_df['Photo'] = display_df['image'].apply(lambda x: "📸 Yes" if x else "❌ No")
            display_df = display_df.drop(columns=['image'], errors='ignore')
            cols = ['id', 'day', 'created_at', 'category', 'amount', 'Photo']
            cols = [c for c in cols if c in display_df.columns]
            display_df = display_df[cols]

        st.dataframe(
            display_df.style.set_properties(**{
                'background-color': '#0f1420',
                'color': '#e8ecf4',
                'border-color': 'rgba(255,255,255,0.05)'
            }),
            use_container_width=True
        )