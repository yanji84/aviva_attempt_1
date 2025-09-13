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
    locate_by = st.radio("Locate By",
                         options=["Last Name / Company Name", "Product", "Reference Number"],
                         index=2, # Default to Reference Number
                         label_visibility="collapsed")

    if locate_by == "Last Name / Company Name":
        c1, c2, c3 = st.columns(3)
        with c1:
            st.text_input("Last Name / Company Name")
        with c2:
            st.text_input("First Name")
        with c3:
            st.text_input("Postal Code")
    elif locate_by == "Product":
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Product", ["All", "Property", "Auto"], index=0)
        with c2:
            st.selectbox("Status", ["All", "In Progress", "Bound"], index=0)
    elif locate_by == "Reference Number":
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
            # This button will now primarily be for non-reference number searches
            pass

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

def unhandled_step():
    toolbar(f"Step {st.session_state.current_step}", "This step is not implemented in the demo.")
    if st.button("Back to Home"):
        st.session_state.current_step = 1
        st.rerun()

# ---------- Main App Logic ----------
app_header()

step_map = {
    1: step1_quote_inquiry,
    2: step2_results,
    3: unhandled_step,
    4: unhandled_step,
    5: unhandled_step,
    6: unhandled_step,
    7: unhandled_step,
    8: unhandled_step,
    9: unhandled_step,
    10: unhandled_step,
}

# This check is to prevent re-rendering issues with on_change
if "current_step" not in st.session_state:
    st.session_state.current_step = 1

step_map[st.session_state["current_step"]]()
