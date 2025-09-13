
import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title="Aviva Business Portal - Mock Demo", layout="wide")

# ---------- Session State ----------
def init_state():
    defaults = {
        "current_step": 1,
        "quote_reference": "P11162731HAB0003",
        "client_last": "Yeung",
        "client_first": "Vincent",
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
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ---------- Helpers ----------
def stepper():
    with st.sidebar:
        st.title("Aviva Business Portal")
        st.caption("Mock UI demo of broker workflow")
        step = st.radio(
            "Navigate steps",
            options=list(range(1, 11)),
            format_func=lambda i: {
                1: "1) Quote Inquiry",
                2: "2) Quote Search Results",
                3: "3) Messages / Underwriting Rules",
                4: "4) Rating Summary",
                5: "5) Confirmation Options",
                6: "6) Client / Policy Search Results",
                7: "7) Client Entry",
                8: "8) Client Creation Confirmation",
                9: "9) Policy Selection",
                10: "10) General Information",
            }[i],
            index=st.session_state["current_step"] - 1
        )
        if step != st.session_state["current_step"]:
            st.session_state["current_step"] = step
        st.markdown("---")
        col1, col2 = st.columns(2)
        if col1.button("◀ Prev", use_container_width=True, disabled=st.session_state["current_step"] == 1):
            st.session_state["current_step"] -= 1
            st.rerun()
        if col2.button("Next ▶", use_container_width=True, disabled=st.session_state["current_step"] == 10):
            st.session_state["current_step"] += 1
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
    toolbar("Step 1: Quote Inquiry", "Search scope, locate-by filters, and workflow tabs.")
    with st.form("quote_inquiry"):
        st.subheader("Search Scope")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.text_input("Company", value=st.session_state["company"])
        with c2:
            st.text_input("Branch", value=st.session_state["branch"])
        with c3:
            st.text_input("Broker # / User ID", value=st.session_state["user_id"])

        st.subheader("Locate By")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.text_input("Last Name", value=st.session_state["client_last"])
        with c2:
            st.text_input("First Name", value=st.session_state["client_first"])
        with c3:
            st.text_input("Company Name")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.text_input("Postal Code")
        with c2:
            st.selectbox("Product", ["Property", "Auto", "Liability"], index=0)
        with c3:
            st.selectbox("Status", ["In progress", "Pending", "Active"], index=0)

        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Reference Number", value=st.session_state["quote_reference"])
        with c2:
            st.date_input("Date range start", value=st.session_state["process_date"] - timedelta(days=30))

        c1, c2 = st.columns(2)
        with c1:
            st.date_input("Date range end", value=st.session_state["process_date"])
        with c2:
            pass

        submitted = st.form_submit_button("Confirm")
        if submitted:
            st.success("Search executed. 1 result found by reference number.")
            st.session_state["current_step"] = 2

    st.button("Cancel Transaction", key="cancel1")

def step2_results():
    toolbar("Step 2: Quote Search Results", "Shows the matching quote(s) based on criteria.")
    st.info(f"Search Criteria — Company: All | Branches: All | Reference: 17575232903866")
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
    c1.button("Prev", disabled=True)
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
    st.write(f"**Reference:** {st.session_state['quote_reference']}  |  **Company/Branch:** {st.session_state['company']} — {st.session_state['branch']}  |  **Commission Variance:** 0.000")
    st.subheader("Premium Summary")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Risk", st.session_state["client_addr"])
    c2.metric("Territory", "4/OZ02")
    c3.metric("Sub Total", f"${st.session_state['rating_subtotal']:,.2f}")
    c4.metric("Risk Total", f"${st.session_state['rating_subtotal']:,.2f}")

    st.subheader("Coverages")
    df = pd.DataFrame(st.session_state["coverage_rows"])
    df["Txn Premium"] = df["Txn Premium"].astype(str)
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
        lambda: st.write(f"**Client:** {st.session_state['client_first']} Cheuk Fun {st.session_state['client_last']}  
**Client Number:** {st.session_state['client_number']}"),
        lambda: st.write(f"**Company/Branch:** {st.session_state['company']} — {st.session_state['branch']}")
    )
    two_cols(
        lambda: st.write(f"**Province:** {st.session_state['province']}  
**Product Type:** {st.session_state['product_type']}"),
        lambda: st.write(f"**Broker #:** {st.session_state['broker_id']}  
**Policy Term:** {st.session_state['effective'].strftime('%b %d, %Y')} · 12 months")
    )
    c1, c2 = st.columns(2)
    c1.button("Cancel Transaction")
    if c2.button("Confirm ➜"):
        st.session_state["current_step"] = 10

def step10_general_info():
    toolbar("Step 10: General Information", "Policy setup details and next workflow tabs.")
    two_cols(
        lambda: st.write(f"**Policy Number:** {st.session_state['policy_number']}  
**Processing Date:** {st.session_state['process_date'].strftime('%b %d, %Y')}  
**Status:** In Progress"),
        lambda: st.write(f"**Company/Branch:** {st.session_state['company']} — {st.session_state['branch']}  
**Client Number:** {st.session_state['client_number']}  
**Combined Policy Discount:** ✅")
    )
    two_cols(
        lambda: st.write(f"**Insured Type:** Individual  
**Insured Name:** {st.session_state['client_first']} Cheuk Fun {st.session_state['client_last']}  
**Insured & Mailing Address:** {st.session_state['client_addr']}"),
        lambda: st.write(f"**Master Broker:** Element Insurance — #{st.session_state['broker_id']}  
**Term:** {st.session_state['effective'].strftime('%b %d, %Y')} → {(st.session_state['effective'] + timedelta(days=365)).strftime('%b %d, %Y')}  
**Policy Province:** {st.session_state['province']}")
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

# ---------- Main ----------
stepper()
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
step_map[st.session_state["current_step"]]()
