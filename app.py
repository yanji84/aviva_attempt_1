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
        "broker_id": "27257",
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
            {"Coverage": "Sewer Backup", "Limit": 25000, "Deductible": 2500, "Txn Premium": 75.00, "Full Term": 75.00},
            {"Coverage": "Overland Water", "Limit": 25000, "Deductible": 2500, "Txn Premium": 120.00, "Full Term": 120.00},
            {"Coverage": "By-Law Coverage", "Limit": 70000, "Deductible": 500, "Txn Premium": "Incl", "Full Term": 0.00},
        ],
        "uw_rules": [
            {"Message #": "M865", "Description": "Full payment required. Credit info not available.", "Type": "UW Rule", "Selected": False},
            {"Message #": "M866", "Description": "No hit on personal info — check and re-enter details.", "Type": "UW Rule", "Selected": False},
            {"Message #": "M663", "Description": "Insurer may order HITS report to verify claims.", "Type": "UW Rule", "Selected": False},
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
    # Demo Banner
    st.markdown(
        '<div class="demo-banner">This is a demo app for Aviva Business Portal. The purpose is to demonstrate TSR Upload Agentic Workflow.</div>',
        unsafe_allow_html=True
    )

    # Header with Logo and Title
    st.markdown(
        """
        <div style="background-color: #00005A; padding: 10px; border-radius: 5px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/9/9f/Aviva_Logo.svg" alt="Aviva Logo" style="height: 50px; float: left; margin-right: 20px;">
            <h1 style="color: white; margin-top: 10px; float: left;">QUOTE</h1>
            <div style="float: right; margin-top: 10px;">
                <a href="#" style="color: white; margin-left: 15px;">HELP</a>
                <a href="#" style="color: white; margin-left: 15px;">LEGAL</a>
                <a href="#" style="color: white; margin-left: 15px;">SIGN OUT</a>
            </div>
            <div style="clear: both;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Navigation Tabs
    tab_names = ["Client", "Quote Inquiry", "Policy", "Work in Progress", "Requests", "Lists"]
    selected_tab = st.selectbox("Navigation", tab_names, index=1, label_visibility="collapsed")

    # This is a simple way to handle navigation for this demo.
    # A more complex app might need a more robust router.
    #if selected_tab == "Quote Inquiry" and st.session_state.current_step != 1:
    #    st.session_state.current_step = 1
    #    st.rerun()


def toolbar(title, subtitle=None):
    st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)
    st.markdown("---")

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
    
    # Create table header
    st.markdown("""
    <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
        <thead>
            <tr style="background-color: #f0f0f0;">
                <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Reference Number</th>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Prospect</th>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Status</th>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Process Date</th>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Effective Date</th>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">User ID</th>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Company / Branch</th>
            </tr>
        </thead>
    </table>
    """, unsafe_allow_html=True)
    
    # Create clickable reference number row
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1.2, 2.5, 1, 1, 1, 0.8, 2])
    
    with col1:
        if st.button(st.session_state["quote_reference"], key="ref_number_click"):
            st.session_state["current_step"] = 3
            st.rerun()
    
    with col2:
        st.write(f"{st.session_state['client_first']} {st.session_state['client_last']}, {st.session_state['client_addr']}")
    
    with col3:
        st.write("In progress")
    
    with col4:
        st.write(st.session_state["process_date"].strftime("%b %d, %Y"))
    
    with col5:
        st.write(st.session_state["effective"].strftime("%b %d, %Y"))
    
    with col6:
        st.write(st.session_state["user_id"])
    
    with col7:
        st.write(f"{st.session_state['company']} — {st.session_state['branch']}")
    
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
    st.dataframe(df.style.hide(axis="index"), use_container_width=True)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.button("Cancel Transaction")
    c2.button("Create Request")
    c3.button("View Requests")
    c4.button("Notes")
    c5.button("Save Incomplete")
    if c6.button("Next ➜"):
        st.session_state["current_step"] = 5

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

def step9_policy_selection():
    toolbar("Step 9: Policy Selection", "Verify key policy details before issuance.")
    two_cols(
        lambda: st.write(f'''**Client:** {st.session_state['client_first']} Cheuk Fun {st.session_state['client_last']}
**Client Number:** {st.session_state['client_number']}'''),
        lambda: st.write(f"**Company/Branch:** {st.session_state['company']} — {st.session_state['branch']}")
    )
    two_cols(
        lambda: st.write(f'''**Province:** {st.session_state['province']}
**Product Type:** {st.session_state['product_type']}'''),
        lambda: st.write(f'''**Broker #:** {st.session_state['broker_id']}
**Policy Term:** {st.session_state['effective'].strftime('%b %d, %Y')} · 12 months''')
    )
    c1, c2 = st.columns(2)
    c1.button("Cancel Transaction")
    if c2.button("Confirm ➜"):
        st.session_state["current_step"] = 10

def step10_general_info():
    toolbar("Step 10: General Information", "Policy setup details and next workflow tabs.")
    two_cols(
        lambda: st.write(f'''**Policy Number:** {st.session_state['policy_number']}
**Processing Date:** {st.session_state['process_date'].strftime('%b %d, %Y')}
**Status:** In Progress'''),
        lambda: st.write(f'''**Company/Branch:** {st.session_state['company']} — {st.session_state['branch']}
**Client Number:** {st.session_state['client_number']}
**Combined Policy Discount:** ✅''')
    )
    two_cols(
        lambda: st.write(f'''**Insured Type:** Individual
**Insured Name:** {st.session_state['client_first']} Cheuk Fun {st.session_state['client_last']}
**Insured & Mailing Address:** {st.session_state['client_addr']}'''),
        lambda: st.write(f'''**Master Broker:** Element Insurance — #{st.session_state['broker_id']}
**Term:** {st.session_state['effective'].strftime('%b %d, %Y')} → {(st.session_state['effective'] + timedelta(days=365)).strftime('%b %d, %Y')}
**Policy Province:** {st.session_state['province']}''')
    )
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.button("Cancel Transaction")
    consent = c2.button("Customer Consent")
    if consent:
        st.session_state["consent_recorded"] = True
    c3.button("Notes")
    c4.button("Policy General Page")
    c5.button("Save Incomplete")
    c6.button("Next")
    if st.session_state["consent_recorded"]:
        st.success("Customer consent recorded. Continue to Risks → Coverages → Billing → Finalize.")

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
    10: step10_general_info,
}

# This check is to prevent re-rendering issues with on_change
if "current_step" not in st.session_state:
    st.session_state.current_step = 1

step_map[st.session_state["current_step"]]()
