import streamlit as st
import pandas as pd
from datetime import date, timedelta

# ---------- Page Config ----------
st.set_page_config(page_title="Aviva Business Portal - Mock Demo", layout="wide")

# ---------- Style Loader ----------
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('style.css')

# ---------- Session State ----------
def init_state():
    defaults = {
        "current_step": 1,
        "quote_reference": "",
        "client_last": "",
        "client_first": "",
        "client_addr": "1386 Castlemore Ave, Markham ON",
        "company": "Aviva Insurance Company of Canada",
        "branch": "A-10 Ontario",
        "broker_id": "",
        "user_id": "123068",
        "effective": date.today() + timedelta(days=10),
        "process_date": date.today(),
        "client_number": "8093847",
        "policy_number": "P97455511HAB",
        "product_type": "Property",
        "province": "Ontario",
        "rating_subtotal": 2183.00,
        "coverage_rows": [
            {"Coverage": "Dwelling Building", "Limit": 702450, "Deductible": 500, "Txn Premium": "Incl", "Full Term": 2183.00},
            {"Coverage": "Personal Property", "Limit": 140490, "Deductible": 500, "Txn Premium": "Incl", "Full Term": 0.00},
            {"Coverage": "Legal Liability", "Limit": 1000000, "Deductible": 0, "Txn Premium": "Incl", "Full Term": 0.00},
            {"Coverage": "Sewer Backup", "Limit": 25000, "Deductible": 2500, "Txn Premium": "75.00", "Full Term": 75.00},
            {"Coverage": "Overland Water", "Limit": 25000, "Deductible": 2500, "Txn Premium": "120.00", "Full Term": 120.00},
            {"Coverage": "By-Law Coverage", "Limit": 70000, "Deductible": 500, "Txn Premium": "Incl", "Full Term": 0.00},
        ],
        "uw_rules": [
            {"Message #": "M865", "Description": "Full payment required. Credit info not available.", "Type": "UW Rule", "Selected": True},
            {"Message #": "M866", "Description": "No hit on personal info — check and re-enter details.", "Type": "UW Rule", "Selected": True},
            {"Message #": "M663", "Description": "Insurer may order HITS report to verify claims.", "Type": "UW Rule", "Selected": True},
        ],
        "client_created": False,
        "associate_client": "No",
        "consent_recorded": False,
        "search_message": ""
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ---------- UI Components ----------
def app_header():
    # Enhanced Demo Banner
    st.markdown(
        '''
        <div class="demo-banner">
            <div style="display: flex; align-items: center; justify-content: center; gap: 12px;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                    <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                    <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                </svg>
                <span>Demo Purpose Only - Aviva Business Portal TSR Upload Agentic Workflow</span>
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Navigation removed as requested


def toolbar(title, subtitle=None):
    st.markdown(f"""
    <div class="toolbar-container" style="
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0 24px 0;
        box-shadow: 0 2px 4px var(--shadow-color);
    ">
        <h2 style="
            color: var(--text-primary);
            margin: 0 0 8px 0;
            font-size: 24px;
            font-weight: 600;
            letter-spacing: -0.025em;
        ">{title}</h2>
        {f'<p style="color: var(--text-secondary); margin: 0; font-size: 16px; font-weight: 400;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def two_cols(a, b):
    c1, c2 = st.columns(2)
    with c1: a()
    with c2: b()

# ---------- Step Renderers ----------
def step1_quote_inquiry():
    st.header("QUOTE SEARCH")
    st.caption(f"GQL001 ver 7.0 | {date.today().strftime('%a %b %d %H:%M:%S %Y')}")

    # Row 1: Company and Branch
    c1, c2 = st.columns(2)
    with c1:
        st.selectbox("Company", ["All Companies"], label_visibility="collapsed")
    with c2:
        st.selectbox("Branch", ["All Branches"], label_visibility="collapsed")

    # Row 2: Broker # and User ID
    c1, c2, c3 = st.columns([2, 1, 2])
    with c1:
        st.text_input("Broker #")
    with c2:
        st.markdown('<p style="text-align: center; margin-top: 30px;">or</p>', unsafe_allow_html=True)
    with c3:
        st.text_input("User ID")


    st.subheader("Locate By")
    st.radio("Locate By",
             options=["Last Name / Company Name", "Product", "Reference Number"],
             index=2, # Default to Reference Number
             key="locate_by",
             label_visibility="collapsed")

    if st.session_state.locate_by == "Last Name / Company Name":
        c1, c2, c3 = st.columns(3)
        with c1:
            st.text_input("Last Name / Company Name")
        with c2:
            st.text_input("First Name")
        with c3:
            st.text_input("Postal Code")
    elif st.session_state.locate_by == "Product":
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Product", ["All", "Property", "Auto"], index=0)
        with c2:
            st.selectbox("Status", ["All", "In Progress", "Bound"], index=0)
    elif st.session_state.locate_by == "Reference Number":
        st.text_input("Reference Number", key="reference_number_input", value=st.session_state.quote_reference, on_change=handle_reference_search)
        if st.session_state.search_message:
            st.warning(st.session_state.search_message)

    # Date fields from the original screenshot
    c1, c2, c3 = st.columns(3)
    with c1:
        st.selectbox("Type of Date", ["Process Date", "Effective Date"])
    with c2:
        st.date_input("From", value=None)
    with c3:
        st.date_input("To", value=None)

    # Bottom buttons
    c1, c2 = st.columns([5, 1]) # Push confirm to the right
    with c2:
        if st.button("Confirm"):
            if st.session_state.locate_by == "Reference Number":
                handle_reference_search()
                # After handling the search, we need to rerun to see the changes
                st.rerun()
            else:
                st.warning("This search type is not yet implemented.")

def handle_reference_search():
    ref_num = st.session_state.reference_number_input
    if ref_num == "P11162731HAB0003":
        st.session_state.quote_reference = ref_num
        st.session_state.current_step = 2
        st.session_state.search_message = ""
    elif ref_num:
        st.session_state.search_message = "No result found"
    else:
        st.session_state.search_message = ""

def step2_results():
    toolbar("Quote Search Results", "Shows the matching quote(s) based on criteria.")
    st.info(f"Search Criteria — Company: All | Branches: All | Reference: {st.session_state.quote_reference}")
    # Add client's first and last name from session state to the dataframe
    st.session_state.client_first = "Vincent"
    st.session_state.client_last = "Yeung"
    
    # Create a custom table with clickable reference number
    st.markdown("### Quote Results")
    
    # Create a properly aligned table using HTML for header and styled columns for data
    st.markdown("""
    <div class="quote-table-container" style="
        width: 100%; 
        border: 1px solid var(--border-color); 
        border-collapse: collapse; 
        font-family: Arial, sans-serif;
        background: var(--bg-primary);
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px var(--shadow-color);
    ">
        <div style="
            display: flex; 
            background: var(--bg-secondary); 
            border-bottom: 1px solid var(--border-color);
            color: var(--text-primary);
        ">
            <div style="width: 15%; padding: 12px 8px; border-right: 1px solid var(--border-color); font-weight: bold; color: var(--text-primary);">Reference Number</div>
            <div style="width: 30%; padding: 12px 8px; border-right: 1px solid var(--border-color); font-weight: bold; color: var(--text-primary);">Prospect</div>
            <div style="width: 10%; padding: 12px 8px; border-right: 1px solid var(--border-color); font-weight: bold; color: var(--text-primary);">Status</div>
            <div style="width: 12%; padding: 12px 8px; border-right: 1px solid var(--border-color); font-weight: bold; color: var(--text-primary);">Process Date</div>
            <div style="width: 12%; padding: 12px 8px; border-right: 1px solid var(--border-color); font-weight: bold; color: var(--text-primary);">Effective Date</div>
            <div style="width: 8%; padding: 12px 8px; border-right: 1px solid var(--border-color); font-weight: bold; color: var(--text-primary);">User ID</div>
            <div style="width: 23%; padding: 12px 8px; font-weight: bold; color: var(--text-primary);">Company / Branch</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create data row using columns with exact same proportions
    col1, col2, col3, col4, col5, col6, col7 = st.columns([15, 30, 10, 12, 12, 8, 23])
    
    with col1:
        # Create a clickable link-styled button for the reference number
        if st.button(st.session_state["quote_reference"], key="ref_number_click", 
                    help="Click to view quote details"):
            st.session_state["current_step"] = 3
            st.rerun()
    
    with col2:
        st.markdown(f'<div class="table-cell" style="padding: 12px 8px; min-height: 40px; display: flex; align-items: center; border: 1px solid var(--border-color); border-top: none; background-color: var(--bg-primary); color: var(--text-primary);">{st.session_state["client_first"]} {st.session_state["client_last"]}, {st.session_state["client_addr"]}</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="table-cell" style="padding: 12px 8px; min-height: 40px; display: flex; align-items: center; border: 1px solid var(--border-color); border-top: none; border-left: none; background-color: var(--bg-primary); color: var(--text-primary);">In progress</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'<div class="table-cell" style="padding: 12px 8px; min-height: 40px; display: flex; align-items: center; border: 1px solid var(--border-color); border-top: none; border-left: none; background-color: var(--bg-primary); color: var(--text-primary);">{st.session_state["process_date"].strftime("%b %d, %Y")}</div>', unsafe_allow_html=True)
    
    with col5:
        st.markdown(f'<div class="table-cell" style="padding: 12px 8px; min-height: 40px; display: flex; align-items: center; border: 1px solid var(--border-color); border-top: none; border-left: none; background-color: var(--bg-primary); color: var(--text-primary);">{st.session_state["effective"].strftime("%b %d, %Y")}</div>', unsafe_allow_html=True)
    
    with col6:
        st.markdown(f'<div class="table-cell" style="padding: 12px 8px; min-height: 40px; display: flex; align-items: center; border: 1px solid var(--border-color); border-top: none; border-left: none; background-color: var(--bg-primary); color: var(--text-primary);">{st.session_state["user_id"]}</div>', unsafe_allow_html=True)
    
    with col7:
        st.markdown(f'<div class="table-cell" style="padding: 12px 8px; min-height: 40px; display: flex; align-items: center; border: 1px solid var(--border-color); border-top: none; border-left: none; background-color: var(--bg-primary); color: var(--text-primary);">{st.session_state["company"]} — {st.session_state["branch"]}</div>', unsafe_allow_html=True)
    
    # Add a divider line
    st.markdown("---")

def step3_messages():
    toolbar("Step 3: Messages / Underwriting Rules", "System-generated rules tied to the quote.")
    st.write(f"**Reference Number:** {st.session_state['quote_reference']}")
    for i, row in enumerate(st.session_state["uw_rules"]):
        st.checkbox(f"{row['Message #']} — {row['Description']} ({row['Type']})",
                    value=row["Selected"], key=f"uw_{i}")
    c1, c2, c3, c4 = st.columns(4)
    c1.button("Create Request")
    c2.button("View Requests")
    c3.button("Save Incomplete")
    if c4.button("Continue ➜"):
        st.session_state["current_step"] = 4
        st.rerun()

def step4_rating():
    toolbar("Step 4: Rating Summary", "Premium calculation and coverage breakdown.")

    df = pd.DataFrame(st.session_state["coverage_rows"])

    # Calculate total premium from the "Full Term" column
    rating_subtotal = df["Full Term"].sum()

    st.write(f"**Reference:** {st.session_state['quote_reference']}  |  **Company/Branch:** {st.session_state['company']} — {st.session_state['branch']}  |  **Commission Variance:** 0.000")
    st.subheader("Premium Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Risk", st.session_state["client_addr"])
    c2.metric("Territory", "4/OZ02")
    c3.metric("Sub Total", f"${rating_subtotal:,.2f}")
    c4.metric("Risk Total", f"${rating_subtotal:,.2f}")

    st.subheader("Coverages")
    st.dataframe(df.style.hide(axis="index"), width='stretch')

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.button("Cancel Transaction")
    c2.button("Create Request")
    c3.button("View Requests")
    c4.button("Notes")
    c5.button("Save Incomplete")
    if c6.button("Next ➜"):
        st.session_state["current_step"] = 5
        st.rerun()

def step5_confirmation():
    toolbar("Step 5: Confirmation Options", "Save, re-quote, or convert to new business.")
    choice = st.radio("Options",
                      options=["Return to Client / Policy Search",
                               "Save Quote and Re-Quote",
                               "Save Quote and Convert to New Business"],
                      index=2)
    c1, c2 = st.columns(2)
    c1.button("Cancel Transaction")
    if c2.button("Submit Quote"):
        if choice == "Save Quote and Convert to New Business":
            st.success("Quote converted to New Business.")
            st.session_state["current_step"] = 6
            st.rerun()
        elif choice == "Save Quote and Re-Quote":
            st.info("Quote saved. You can re-run underwriting/pricing.")
        else:
            st.session_state["current_step"] = 1
            st.rerun()

def step6_client_search():
    # Header with version and timestamp
    st.markdown("### CLIENT / POLICY SEARCH RESULTS")
    st.markdown(f'<div style="float: right; color: #666; font-size: 14px;">GCL002A ver 7.0</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="float: right; clear: both; color: #666; font-size: 14px;">{date.today().strftime("Wed %d %b %y %H:%M:%S %p")}</div>', unsafe_allow_html=True)
    st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)
    
    # Search Criteria Section
    st.markdown("""
    <div style="background-color: #003366; color: white; padding: 8px; margin: 10px 0; font-weight: bold;">
        SEARCH CRITERIA
    </div>
    """, unsafe_allow_html=True)
    
    # Create search criteria display in a structured format
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Company**")
        st.markdown("1 - Aviva Insurance Company of Canada")
        st.markdown("**Last Name / Company Name**")
        st.markdown("YEUNG")
    
    with col2:
        st.markdown("**Branch**")
        st.markdown("A - 10 - Ontario")
        st.markdown("**First Initial**")
        st.markdown("")
        st.markdown("**Postal Code**")
        st.markdown("")
    
    # Search Results Section
    st.markdown("""
    <div style="background-color: #003366; color: white; padding: 8px; margin: 20px 0 10px 0; font-weight: bold;">
        SEARCH RESULTS
    </div>
    """, unsafe_allow_html=True)
    
    # Instructions
    st.markdown("""
    <div style="margin: 10px 0; font-size: 14px;">
        To view a particular Client's list of policies, please select the Policy Number(s) link to the right of that Client's name.<br>
        To view information at a Client's detail level, please select the Client Number link to the left of that Client's name.
    </div>
    """, unsafe_allow_html=True)
    
    # Results table header
    st.markdown("""
    <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
        <thead>
            <tr style="background-color: #f0f0f0; border: 1px solid #ccc;">
                <th style="padding: 8px; border: 1px solid #ccc; text-align: left; width: 15%;">Client Number</th>
                <th style="padding: 8px; border: 1px solid #ccc; text-align: left; width: 25%;">Client Name</th>
                <th style="padding: 8px; border: 1px solid #ccc; text-align: left; width: 15%;">Policy List</th>
                <th style="padding: 8px; border: 1px solid #ccc; text-align: left; width: 45%;">Address</th>
            </tr>
        </thead>
    </table>
    """, unsafe_allow_html=True)
    
    # No results message
    st.markdown("""
    <div style="text-align: center; padding: 20px; font-weight: bold; color: #666;">
        No items matching your search criteria were found.
    </div>
    """, unsafe_allow_html=True)
    
    # Bottom navigation buttons
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("Create New Client ➜"):
        st.session_state["current_step"] = 7
        st.rerun()
    if c2.button("New Search"):
        st.rerun()

def step7_client_entry():
    # Header with version and timestamp
    st.markdown("### CLIENT ENTRY")
    st.markdown(f'<div style="float: right; color: #666; font-size: 14px;">NCL005 ver 7.0</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="float: right; clear: both; color: #666; font-size: 14px;">{date.today().strftime("Wed %d %b %y %H:%M:%S %p")}</div>', unsafe_allow_html=True)
    st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)
    
    with st.form("client_entry"):
        # Company and Branch Section
        st.markdown("""
        <div style="background-color: #003366; color: white; padding: 8px; margin: 10px 0; font-weight: bold;">
            COMPANY AND BRANCH
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            st.markdown("**Company**")
            st.text_input("Company", value="1 - Aviva Insurance Company of Canada", disabled=True, label_visibility="collapsed")
        with c2:
            st.markdown("**Branch**")
            st.text_input("Branch", value="A - 10 - Ontario", disabled=True, label_visibility="collapsed")
        with c3:
            st.markdown("**Broker #**")
            st.text_input("Broker #", value=st.session_state["broker_id"], label_visibility="collapsed")

        # Client Type Section
        st.markdown("""
        <div style="background-color: #003366; color: white; padding: 8px; margin: 20px 0 10px 0; font-weight: bold;">
            CLIENT TYPE
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Client Type**")
            st.selectbox("Client Type", ["Insured"], index=0, label_visibility="collapsed")
            st.markdown("**VIP**")
            col1, col2 = st.columns([1, 4])
            with col1:
                st.radio("VIP", ["Yes", "No"], index=1, label_visibility="collapsed", horizontal=True)
        with c2:
            st.markdown("**Date of Birth**")
            st.date_input("Date of Birth", value=date(1980,1,1), label_visibility="collapsed")
            st.markdown("**Member #**")
            st.text_input("Member #", label_visibility="collapsed")
        with c3:
            st.markdown("**Language**")
            st.selectbox("Language", ["English", "French"], index=0, label_visibility="collapsed")
            st.markdown("**Broker Client ID**")
            st.text_input("Broker Client ID", label_visibility="collapsed")

        # Client Name Section
        st.markdown("""
        <div style="background-color: #003366; color: white; padding: 8px; margin: 20px 0 10px 0; font-weight: bold;">
            CLIENT NAME
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**First Named Insured**")
        c1, c2, c3 = st.columns([1, 2, 2])
        with c1:
            st.markdown("**Title**")
            st.text_input("Title", label_visibility="collapsed")
        with c2:
            st.markdown("**Last Name**")
            st.text_input("Last Name", value="YEUNG", label_visibility="collapsed")
        with c3:
            st.markdown("**First Name**")
            st.text_input("First Name", value="VINCENT", label_visibility="collapsed")
        
        st.markdown("**Or**")
        st.markdown("**Company Name**")
        st.text_input("Company Name", label_visibility="collapsed")

        # Additional Named Insured Section
        st.markdown("**Additional Named Insured**")
        c1, c2, c3, c4 = st.columns([1, 1, 2, 2])
        with c1:
            st.markdown("**Name Link**")
            st.selectbox("Name Link", [""], label_visibility="collapsed")
        with c2:
            st.markdown("**Title**")
            st.text_input("Additional Title", label_visibility="collapsed")
        with c3:
            st.markdown("**Last Name**")
            st.text_input("Additional Last Name", label_visibility="collapsed")
        with c4:
            st.markdown("**First Name**")
            st.text_input("Additional First Name", label_visibility="collapsed")
        
        st.markdown("**Or**")
        st.markdown("**Company Name**")
        st.text_input("Additional Company Name", label_visibility="collapsed")

        # Legal Address Section
        st.markdown("""
        <div style="background-color: #003366; color: white; padding: 8px; margin: 20px 0 10px 0; font-weight: bold;">
            LEGAL ADDRESS
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Address**")
        st.text_input("Address", value="1386 CASTLEMORE AVE", label_visibility="collapsed")
        
        # Additional address fields
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("City", value="Markham", label_visibility="collapsed")
        with c2:
            st.text_input("Additional Address Line", label_visibility="collapsed")
        
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Additional Address Line 2", label_visibility="collapsed")
        with c2:
            st.text_input("Additional Address Line 3", label_visibility="collapsed")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Province**")
            st.selectbox("Province", ["Ontario"], index=0, label_visibility="collapsed")
        with c2:
            st.markdown("**Postal Code**")
            col1, col2 = st.columns([2, 1])
            with col1:
                st.text_input("Postal Code", value="L6E0H1", label_visibility="collapsed")
            with col2:
                validate = st.form_submit_button("Validate", type="secondary")

        # Telephone Section
        st.markdown("""
        <div style="background-color: #003366; color: white; padding: 8px; margin: 20px 0 10px 0; font-weight: bold;">
            TELEPHONE
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Residence**")
            st.text_input("Residence", value="437-986-7928", label_visibility="collapsed")
        with c2:
            st.markdown("**Business**")
            st.text_input("Business", value="nnn-nnn-nnnn", label_visibility="collapsed")
        with c3:
            st.markdown("**Ext**")
            st.text_input("Ext", label_visibility="collapsed")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Cell Phone**")
            st.text_input("Cell Phone", value="nnn-nnn-nnnn", label_visibility="collapsed")
        with c2:
            st.markdown("**Contact**")
            st.text_input("Contact", label_visibility="collapsed")

        # Additional Information / Paperless Policy Delivery Preference Section
        st.markdown("""
        <div style="background-color: #003366; color: white; padding: 8px; margin: 20px 0 10px 0; font-weight: bold;">
            ADDITIONAL INFORMATION / PAPERLESS POLICY DELIVERY PREFERENCE
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Mailing Address**")
        st.text_input("Mailing Address", value="The most recent address", label_visibility="collapsed")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Occupation**")
            st.selectbox("Occupation", ["All other"], index=0, label_visibility="collapsed")
        with c2:
            st.markdown("**Cross Reference Date**")
            st.text_input("Cross Reference Date", value="dd/mm/yyyy", label_visibility="collapsed")
        with c3:
            st.markdown("**Tax Exempt**")
            col1, col2 = st.columns(2)
            with col1:
                st.radio("Tax Exempt", ["Yes", "No"], index=1, label_visibility="collapsed", horizontal=True)
            with col2:
                st.markdown("**Certificate #**")
                st.text_input("Certificate #", label_visibility="collapsed")

        # Policy Document Mailing Preference Section
        st.markdown("""
        <div style="background-color: #003366; color: white; padding: 8px; margin: 20px 0 10px 0; font-weight: bold;">
            POLICY DOCUMENT MAILING PREFERENCE
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Policy Documents Mailing Preference**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.checkbox("BMS", value=True)
            with col2:
                st.checkbox("Email")
            with col3:
                st.checkbox("Print")
        with c2:
            st.markdown("**Reason**")
            st.selectbox("Reason", ["Select reason..."], index=0, label_visibility="collapsed")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Liability Slip Mailing Preference**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.checkbox("Print", key="liability_print")
            with col2:
                st.checkbox("Email", key="liability_email")
            with col3:
                st.checkbox("Text", key="liability_text")
        with c2:
            st.markdown("**E-Mail Address**")
            st.text_input("E-Mail Address", value="VINCENTYEUNG2002@GMAIL.CO", label_visibility="collapsed")

        # Bottom buttons row
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3, c4, c5 = st.columns(5)
        
        with c1:
            cancel = st.form_submit_button("Cancel Transaction", type="secondary")
        with c2:
            additional1 = st.form_submit_button("Additional Names", type="secondary", key="additional_1")
        with c3:
            additional2 = st.form_submit_button("Additional Address", type="secondary", key="additional_2")
        with c4:
            bank = st.form_submit_button("Bank Details", type="secondary")
        with c5:
            confirm = st.form_submit_button("Confirm", type="primary")
        
        if validate:
            st.success("Postal code validated successfully.")
        
        if confirm:
            st.session_state["client_created"] = True
            st.success("Client created successfully.")
            st.session_state["current_step"] = 8
            st.rerun()

def step8_client_confirmation():
    toolbar("Step 8: Client Creation Confirmation", "Client successfully created; choose association.")
    st.success("The New Client Process is Complete. The Client has been submitted successfully.")
    st.metric("Client Number", st.session_state["client_number"])
    st.radio("Do you want to Associate this Client with Another Client?",
             options=["No", "Yes"], key="associate_client")
    if st.button("Confirm ➜"):
        st.session_state["current_step"] = 9
        st.rerun()

def step9_policy_selection():
    # Header with version and timestamp
    st.markdown("### POLICY SELECTION")
    st.markdown(f'<div style="float: right; color: #666; font-size: 14px;">NP 5001 ver 7.0</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="float: right; clear: both; color: #666; font-size: 14px;">{date.today().strftime("Wed %d %b %y %H:%M:%S %p")}</div>', unsafe_allow_html=True)
    st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)
    
    # Client Name section
    st.markdown("**Client Name**")
    st.markdown(f"VINCENT CHEUK FUN YEUNG")
    
    # Client Number section
    st.markdown("**Client Number**")
    st.markdown(f"{st.session_state['client_number']}")
    
    # Two column layout for Company/Branch and Province sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Company and Branch**")
        st.markdown("**Company**")
        st.markdown("1 - Aviva Insurance Company of Canada")
        st.markdown("**Branch**")
        st.markdown("A - 10 - Ontario")
    
    with col2:
        st.markdown("**Province**")
        st.markdown("**Query Province**")
        st.markdown("Ontario")
    
    # Product section
    st.markdown("**Product**")
    st.markdown("**Product Type**")
    st.markdown("Property")
    
    # Broker section
    st.markdown("**Broker**")
    st.markdown("**Broker #**")
    st.markdown("27267")
    
    # Policy Term section
    st.markdown("**Policy Term**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Effective Date**")
        st.markdown(f"{st.session_state['effective'].strftime('Sep %d, %Y')}")
    with col2:
        st.markdown("**Term**")
        st.markdown("12 Months")
    
    # Bottom buttons
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.button("Cancel Transaction")
    if c2.button("Confirm ➜"):
        st.session_state["current_step"] = 10
        st.rerun()

def step10_customer_consent():
    # Header with version and timestamp
    st.markdown("### CUSTOMER CONSENT")
    st.markdown(f'<div style="float: right; color: #666; font-size: 14px;">CCP001 ver 1.0</div>', unsafe_allow_html=True)
    st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)
    
    # Policy Number
    st.markdown("**Policy Number**")
    st.markdown(f"{st.session_state['policy_number']}")
    
    # Declaration of Applicant section
    st.markdown("""
    <div style="background-color: #003366; color: white; padding: 8px; margin: 20px 0 10px 0; font-weight: bold;">
        Declaration of Applicant
    </div>
    """, unsafe_allow_html=True)
    
    # Consent question
    st.markdown("**Does the Applicant agree to the following statements?**")
    consent_choice = st.radio(
        "Does the Applicant agree to the following statements?",
        options=["Yes", "No"],
        index=0,
        key="consent_agreement",
        label_visibility="collapsed",
        horizontal=True
    )
    
    # Consent text sections
    st.markdown("""
    **By Clicking "Yes" to the above question, you agree to provide Aviva with consent on behalf of yourself and other individuals 
    listed to collect and use your credit information**
    
    **By Clicking "No" to the above question, you disagree to provide Aviva with consent on behalf of yourself and other individuals 
    listed to collect and use your credit information**
    
    **Consent to Use of Personal and Credit Information**
    
    To provide you with the best possible price for your insurance policy, Aviva is asking for your consent to obtain your credit 
    information, which may include your credit score and other information in your credit file in addition to using your credit 
    information for the purpose of writing your insurance policy. We may also ask TransUnion, Equifax and other sources to verify 
    your information in connection with your insurance policy. This information will be collected and used in accordance with our Privacy 
    Policy. This credit inquiry may appear on your credit file and may be accessed during your policy renewal and at any time while 
    you have a policy with Aviva. When accessed, Aviva Insurance Company and its affiliates will be listed as an inquiry to report an 
    existing account in good standing, and will not be treated as an application for new credit or service. This consent is not a 
    consent to collection and use of your credit information is optional, and you may withdraw your consent at any time by contacting 
    your broker; however, this may impact your price.
    
    The personal information you provide in this webform will be used by Aviva Canada Inc. and our member companies ("Aviva") to 
    process your quote, issue your insurance contract, if applicable, and support the administration of your policy. The personal 
    information may be validated and reviewed, including your claims and policy history, and used in statistical models to calculate 
    your insurance risk and premium.
    
    The personal information you provide may also be pooled with information from other sources and subject to analysis for the 
    limited purpose of preventing, detecting or suppressing fraud. For this purpose, and to validate the information provided in this 
    application, Aviva may report to and obtain information from various databases.
    """)
    
    # Additional consent information
    st.markdown("""
    If the information returned from these sources differs from what you have disclosed, the price and coverages offered to you may 
    change, or your policy may be cancelled.
    
    Aviva may also collect, use or disclose your personal information for other purposes. These purposes and our privacy practices 
    and procedures are outlined in our respective privacy policies, as well as information about your privacy rights. Aviva's privacy 
    policy can be obtained at www.avivacanada.com
    
    By clicking the "Submit" button below, you consent to Aviva collecting, using and disclosing the personal information you provide 
    in connection with this webform and declare that you have obtained consent from the individuals listed in this webform for the 
    collection, use and disclosure of their personal information, all as described above.
    """)
    
    # Personal Information Form Section
    st.markdown("""
    <div style="background-color: #e6e6e6; padding: 10px; margin: 20px 0; border-radius: 5px;">
        <strong>Personal Information Form</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # Form fields in a structured layout
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        st.text_input("Last Name", value="YEUNG", key="consent_last_name")
    
    with col2:
        st.text_input("First Name", value="VINCENT CHEUK FUN", key="consent_first_name")
    
    with col3:
        st.text_input("Middle Name", key="consent_middle_name")
    
    # Street Address row
    st.text_input("Street Address", value="1386 CASTLEMORE AVE", key="consent_street_address")
    
    # City, Province, Postal Code row
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.text_input("City", value="MARKHAM", key="consent_city")
    
    with col2:
        st.selectbox("Province", ["Ontario"], index=0, key="consent_province")
    
    with col3:
        st.text_input("Postal Code", value="L6E0H1", key="consent_postal_code")
    
    # Date of Birth and Home Phone row
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Date Of Birth", value="01/01/1980", key="consent_dob")
    
    with col2:
        st.text_input("Home Phone", value="437-986-7928", key="consent_home_phone")
    
    # Submit and Exit buttons
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col2:
        submit_clicked = st.button("Submit", type="primary")
    
    with col3:
        exit_clicked = st.button("Exit", type="secondary")
    
    # Handle button actions
    if submit_clicked:
        if consent_choice == "Yes":
            st.session_state["consent_recorded"] = True
            st.success("Consent submitted successfully!")
            st.session_state["current_step"] = 11
            st.rerun()
        else:
            st.warning("You must agree to the consent statements to proceed.")
    
    if exit_clicked:
        st.session_state["current_step"] = 9  # Go back to policy selection
        st.rerun()

def step11_general_info():
    # Header with version and timestamp
    st.markdown("### GENERAL INFORMATION")
    st.markdown(f'<div style="float: right; color: #666; font-size: 14px;">Wed 10 Sep 25 3:34:39 pm</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="float: right; clear: both; color: #666; font-size: 14px;">NPP001 ver 7.0</div>', unsafe_allow_html=True)
    st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)
    
    # Top row - Policy info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Policy Number**")
        st.markdown(f"{st.session_state['policy_number']}")
        st.markdown("**Processing Date**")
        st.markdown("Sep 10, 2025")
        st.markdown("**Status**")
        st.markdown("In progress")
    
    with col2:
        st.markdown("**Product**")
        st.markdown("Property")
        st.markdown("**Company**")
        st.markdown("1 - Aviva Insurance Company of Canada")
        st.markdown("**Branch**")
        st.markdown("A - 10 - Ontario")
    
    with col3:
        st.markdown("**Client Number**")
        st.markdown(f"{st.session_state['client_number']}")
        st.markdown("**Branch**")
        st.markdown("Aviva")
        st.markdown("**Client Association**")
        st.markdown("No")
        st.markdown("**Combined Policy Discount**")
        st.checkbox("Combined Policy Discount", value=True, key="combined_discount", label_visibility="collapsed")
    
    # Policy Holder Information Section
    st.markdown("""
    <div style="background-color: #003366; color: white; padding: 8px; margin: 20px 0 10px 0; font-weight: bold;">
        POLICY HOLDER INFORMATION
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("**Insured Type**")
        st.selectbox("Insured Type", ["Individual"], index=0, key="insured_type", label_visibility="collapsed")
        st.markdown("**Insured Name**")
        st.selectbox("Insured Name", ["VINCENT CHEUK FUN YEUNG"], index=0, key="insured_name", label_visibility="collapsed")
    
    with col2:
        st.markdown("**Insured Address**")
        st.text_input("Insured Address", value="1386 CASTLEMORE AVE MARKHAM ON L6E0H1", key="insured_address", label_visibility="collapsed")
        st.markdown("**Mailing Address**")
        st.text_input("Mailing Address", value="1386 CASTLEMORE AVE MARKHAM ON L6E0H1", key="mailing_address", label_visibility="collapsed")
    
    # Broker Information Section
    st.markdown("""
    <div style="background-color: #003366; color: white; padding: 8px; margin: 20px 0 10px 0; font-weight: bold;">
        BROKER INFORMATION
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Master Broker Name**")
        st.text_input("Master Broker Name", value="Element Insurance - 27267", key="master_broker", label_visibility="collapsed")
        st.markdown("**Address**")
        st.text_input("Broker Address", value="303-3660 VICTORIA PARK AVE NORTH YORK ON M2H2P7", key="broker_address", label_visibility="collapsed")
        st.markdown("**Telephone #**")
        st.text_input("Telephone", value="(416) 613-7867", key="broker_phone", label_visibility="collapsed")
        st.markdown("**Fax #**")
        st.text_input("Fax", value="(416) 613-7868", key="broker_fax", label_visibility="collapsed")
    
    with col2:
        st.markdown("**Group Name**")
        st.text_input("Group Name", key="group_name", label_visibility="collapsed")
        st.markdown("**Broker #**")
        st.text_input("Broker Number", value="27267", key="broker_number", label_visibility="collapsed")
    
    # Policy Term Section
    st.markdown("""
    <div style="background-color: #003366; color: white; padding: 8px; margin: 20px 0 10px 0; font-weight: bold;">
        POLICY TERM
    </div>
    """, unsafe_allow_html=True)
    
    # First row of policy term fields
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**Effective Date**")
        st.date_input("Effective Date", value=st.session_state['effective'], key="policy_effective_date", label_visibility="collapsed")
        st.markdown("**Expiry Date**")
        st.date_input("Expiry Date", value=st.session_state['effective'] + timedelta(days=365), key="policy_expiry_date", label_visibility="collapsed")
    
    with col2:
        st.markdown("**Time**")
        st.text_input("Time", value="12:01 AM", key="effective_time", label_visibility="collapsed")
        st.markdown("**Time**")
        st.text_input("Time", value="12:01 AM", key="expiry_time", label_visibility="collapsed")
    
    with col3:
        st.markdown("**Policy Inception Date**")
        st.date_input("Policy Inception Date", value=st.session_state['effective'], key="policy_inception_date", label_visibility="collapsed")
        st.markdown("**Client Loyalty Date**")
        st.date_input("Client Loyalty Date", value=st.session_state['effective'], key="client_loyalty_date", label_visibility="collapsed")
    
    with col4:
        st.markdown("**Term (in months)**")
        st.text_input("Term", value="12", key="policy_term_months", label_visibility="collapsed")
        st.markdown("**Renewal Term**")
        st.selectbox("Renewal Term", ["12 Months"], index=0, key="renewal_term", label_visibility="collapsed")
        st.markdown("**Replace Policy Number**")
        st.text_input("Replace Policy Number", key="replace_policy_number", label_visibility="collapsed")
    
    # Second row of policy term fields
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**Transferred From**")
        st.text_input("Transferred From", key="transferred_from", label_visibility="collapsed")
        st.markdown("**Service Next Renewal**")
        col_yes, col_no = st.columns(2)
        with col_yes:
            st.checkbox("Yes", key="service_renewal_yes")
        with col_no:
            st.checkbox("No", value=True, key="service_renewal_no")
    
    with col2:
        st.markdown("**Lapse Next Renewal**")
        col_yes, col_no = st.columns(2)
        with col_yes:
            st.checkbox("Yes", key="lapse_renewal_yes")
        with col_no:
            st.checkbox("No", value=True, key="lapse_renewal_no")
    
    # Bottom section spacing
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Action buttons
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.button("Cancel Transaction")
    c2.button("Customer Consent")
    c3.button("Notes")
    c4.button("Policy General Page")
    c5.button("Save Incomplete")
    if c6.button("Next"):
        st.success("General Information completed. Continue to Risks → Coverages → Billing → Finalize.")
        # Could add navigation to next step here if needed

# ---------- Main App Logic ----------
app_header()

step_map = {
    1: step1_quote_inquiry,
    2: step2_results,
    3: step3_messages,
    4: step4_rating,
    5: step5_confirmation,
    6: step6_client_search,
    7: step7_client_entry,
    8: step8_client_confirmation,
    9: step9_policy_selection,
    10: step10_customer_consent,
    11: step11_general_info,
}

# This check is to prevent re-rendering issues with on_change
if "current_step" not in st.session_state:
    st.session_state.current_step = 1

step_map[st.session_state["current_step"]]()
