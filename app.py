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
    if selected_tab == "Quote Inquiry" and st.session_state.current_step != 1:
        st.session_state.current_step = 1
        st.rerun()


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
    df = pd.DataFrame([{
        "Reference Number": st.session_state["quote_reference"],
        "Prospect": f"{st.session_state['client_first']} {st.session_state['client_last']}, {st.session_state['client_addr']}",
        "Status": "In progress",
        "Process Date": st.session_state["process_date"].strftime("%b %d, %Y"),
        "Effective Date": st.session_state["effective"].strftime("%b %d, %Y"),
        "User ID": st.session_state["user_id"],
        "Company / Branch": f"{st.session_state['company']} — {st.session_state['branch']}",
    }])
    st.dataframe(df.style.hide(axis="index"), use_container_width=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.button("Prev", on_click=lambda: st.session_state.update(current_step=1))
    c2.button("More", disabled=True)
    c3.button("Create New")
    if c4.button("Open Quote"):
        st.session_state["current_step"] = 3

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
        elif choice == "Save Quote and Re-Quote":
            st.info("Quote saved. You can re-run underwriting/pricing.")
        else:
            st.session_state["current_step"] = 1

def step6_client_search():
    toolbar("Step 6: Client / Policy Search Results", "Validate if client already exists.")
    st.info("Search Criteria — Company: Aviva Insurance Company of Canada | Branch: A-10 Ontario | Client Name: Yeung")
    st.warning("No items matching your search criteria were found.")
    c1, c2 = st.columns(2)
    if c1.button("Create New Client ➜"):
        st.session_state["current_step"] = 7
    if c2.button("New Search"):
        st.rerun()

def step7_client_entry():
    toolbar("Step 7: Client Entry", "Capture necessary client details to create the insured.")
    with st.form("client_entry"):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.text_input("Company", st.session_state["company"])
        with c2:
            st.text_input("Branch", st.session_state["branch"])
        with c3:
            st.text_input("Broker #", st.session_state["broker_id"])

        st.subheader("Client Type")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.selectbox("Client Type", ["Insured"], index=0)
        with c2:
            st.date_input("Date of Birth", value=date(1980,1,1))
        with c3:
            st.selectbox("Language", ["English", "French"], index=0)
        with c4:
            st.checkbox("VIP")

        st.subheader("Client Name")
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Last Name", st.session_state["client_last"])
        with c2:
            st.text_input("First Name", st.session_state["client_first"])

        st.subheader("Legal Address")
        st.text_input("Address", st.session_state["client_addr"])
        st.text_input("City", "Markham")
        st.text_input("Province", st.session_state["province"])
        st.text_input("Postal Code", "")

        st.markdown("**Next Steps**")
        c1, c2, c3, c4 = st.columns(4)
        c1.button("Additional Names")
        c2.button("Additional Address")
        c3.button("Bank Details")
        submitted = c4.form_submit_button("Confirm")
        if submitted:
            st.session_state["client_created"] = True
            st.success("Client created successfully.")
            st.session_state["current_step"] = 8

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
