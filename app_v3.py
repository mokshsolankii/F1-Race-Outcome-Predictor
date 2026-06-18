with row1_cols[1]:
    # CSS to inject clean block integration and hover effects without breaking variables
    st.markdown("""
    <style>
    /* 1. Shell container to enforce identical look and height to Box 1 */
    .gp-container-card {
        background: #181820;
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 10px;
        padding: 12px 16px;
        height: 95px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        margin-bottom: 0px !important;
    }

    /* Red glow sync configuration */
    div[data-testid="stColumn"]:nth-of-type(2):hover .gp-container-card {
        border-color: #FF1801 !important;
        box-shadow: 0 0 20px rgba(255, 24, 1, 0.3) !important;
        background: #1c1c26 !important;
    }

    /* 2. Target and completely kill the ghost spacing label from Streamlit */
    div[data-testid="stColumn"]:nth-of-type(2) label[data-testid="stWidgetLabel"] {
        display: none !important;
        height: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
    }

    /* Force the native selectbox to tightly integrate inside our card framework */
    div[data-testid="stColumn"]:nth-of-type(2) div[data-testid="stSelectbox"] {
        margin-top: 4px !important;
    }

    div[data-testid="stColumn"]:nth-of-type(2) div[role="combobox"] {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 6px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Render the pure semantic title header card layout first
    st.markdown("""
    <div class="gp-container-card">
        <div style="color: #888888; font-size: 0.72em; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; line-height: 1.2; margin-bottom: 2px;">SELECT GRAND PRIX</div>
    """, unsafe_allow_html=True)

    # CRITICAL FIX: Assigning to 'race_name' directly so downstream formulas don't throw NameError
    race_name = st.selectbox(
        "Select Grand Prix", # Hidden by CSS, but keeps accessibility intact
        options=gps_list if 'gps_list' in locals() else ["Round 10: Austria", "Round 11: Great Britain"],
        key="dashboard_gp_selector_v4"
    )

    # Safely close the visual shell structure container
    st.markdown("</div>", unsafe_allow_html=True)
