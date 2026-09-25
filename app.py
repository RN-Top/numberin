# TAB 1: MILESTONE TIMELINE LENS & READINGS
with tab_milestones:
    st.header("Chronos & Cosmos: Milestone Timeline")
    st.caption("Cross-reference historical dates against celestial events, eclipses, and personal resonance.")

    timeline_mode = st.radio(
        "Timeline Selection Mode:",
        ["Choose Pre-Set Turning Point", "Enter Any Custom Date"],
        horizontal=True
    )

    if timeline_mode == "Choose Pre-Set Turning Point":
        selected_milestone = st.selectbox(
            "Select Historical or Cosmic Turning Point:",
            list(MILESTONES.keys()),
            index=0  # Defaults to the first item (Crucifixion Blood Moon) instead of sticking
        )
        m_info = MILESTONES[selected_milestone]
        target_year = m_info["year"]
        target_month = m_info["month"]
        target_day = m_info["day"]
        date_display = m_info["date_str"]
        category_display = m_info["category"]
        astro_display = m_info["astronomy"]
        details_display = m_info["details"]
    else:
        custom_input_date = st.date_input("Pick or Type Any Milestone Date:", value=datetime.date.today())
        target_year = custom_input_date.year
        target_month = custom_input_date.month
        target_day = custom_input_date.day
        date_display = custom_input_date.strftime("%Y-%m-%d")
        category_display = "Custom Inquired Timeline"
        astro_display = "Dynamic calculated astronomical phase for selected date."
        details_display = f"Custom timeline probe for {date_display}."

    # Calculations update automatically based on whatever date is active
    m_lunar = get_lunar_phase_details(target_year, target_month, target_day)
    m_root = calculate_vibrational_root(date_display)
    m_compat = evaluate_compatibility(user_lp, m_root)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Date", date_display)
    c2.metric("Lunar Phase", m_lunar["phase"])
    c3.metric("Illumination", f"{m_lunar['illumination']}%")
    c4.metric("Milestone Root", f"Root {m_root}")

    st.markdown("---")
    col_hist, col_read = st.columns([1.2, 1])

    with col_hist:
        st.subheader("📜 Historical & Celestial Chronicle")
        st.markdown(f"**Category:** *{category_display}*")
        st.info(f"**Astronomical Occurrence:**\n\n{astro_display}")
        st.write(details_display)

    with col_read:
        st.subheader("⚡ Synchronicity Reading")
        display_label = user_name if user_name else "Observer"
        st.markdown(f"**{display_label}** | Life Path `{user_lp}`  ↔  Milestone `{m_root}`")
        st.metric("Resonance Index", f"{m_compat['score']}%")
        st.success(m_compat['description'])
        st.markdown(f"""
        * **Lunar Dynamics:** Observer phase: **{user_moon['phase']}** ({user_moon['illumination']}%), Milestone phase: **{m_lunar['phase']}** ({m_lunar['illumination']}%).
        * **Solar Anchor:** {user_sun_sign} alignment across historic coordinates.
        """)
