You will create a Aviva Business Portal mock-up UI for me.

“Aviva Business Portal” (also seen as MyAviva Business) is an online service offered by Aviva (UK) that gives business customers digital access to their business insurance / workplace policies.

You will create a mock up ui of the “Aviva Business Portal” for me according to the screenshots I share with you.

The mock up UI should be able to demonstrate the following workflow

Step 1: Quote Inquiry



Purpose

It lets brokers, agents, or internal staff search for insurance quotes in the Aviva system. This is a back-office tool rather than the customer-facing MyAviva Business portal.

Main Functions

Search Scope

Company / Branch dropdowns: filter by which Aviva company or branch issued the quote.

Broker # / User ID: look up quotes tied to a specific broker or user.

Locate By (search criteria)

Name fields: search by client’s last name, first name, or company name.

Postal code: refine searches by geography.

Product / Status: search by type of insurance product (e.g., auto, property, liability) and the quote’s status (active, pending, etc.).

Reference Number: direct lookup by quote ID.

Date range: narrow results to quotes created/updated within a specific timeframe.

Navigation / Workflow

Tabs across the top (Client, Quote Inquiry, Policy, Work in Progress, Requests, Lists) let users move between different parts of the portal.

Buttons like Cancel Transaction and Confirm finalize or exit searches.

Typical Use Case

A broker or Aviva employee would:

Enter a client name, product, or reference number.
Select a branch or broker ID if needed.
Apply a date filter.
Retrieve the matching quotes to view details, continue underwriting, or convert into a policy

In short: this UI is an insurance quote lookup/search interface within Aviva’s business system, designed for brokers and staff to track, filter, and manage quotes.
Step 2: Quote Search Results



Purpose

It displays the matching insurance quote(s) found based on the search criteria entered (in this case, by reference number).

Key Sections
Search Criteria (top box)
Shows the parameters you searched with (e.g., All Companies, All Branches, Reference Number: 17575232903866).
Acts as a quick recap so you know what filters were applied.

Search Results (main table)
Each row corresponds to a quote record. The columns displayed:
Reference Number: the unique ID of the quote (e.g., P11162731HAB0003 – clickable link).
Prospect Name & Address: the client or business the quote is for (e.g., Yeung Vincent, 1386 Castlemore Ave, Markham ON).
Status: current stage of the quote (e.g., In progress).
Process Date: the date the quote was generated or last updated (Sep 10, 2025).
Effective Date: the date coverage would begin (Sep 23, 2025).
User ID: the identifier for the broker/agent handling the quote (123068).
Company Name & Branch Number: which Aviva entity/branch issued it (Aviva A-10 Ontario).
Navigation Controls (bottom)
Prev / More: move through multiple pages of search results (if more than one quote matched).
Create New / New (green/purple buttons): shortcuts to create a brand-new quote record.

Typical Workflow After This Screen

The broker or staff member would click on the reference number link to open the detailed quote file.

From there, they can review underwriting details, adjust coverages, finalize premiums, or move it forward to policy issuance.

If no results are found, they would refine the search and rerun it.

Step 3: Messages / Underwriting Rules



Purpose

To show system-generated underwriting messages and rules tied to the selected quote. These are conditions, warnings, or required actions before the quote can move further (e.g., toward final approval or binding a policy).

Key Elements

Reference Number
The quote you are working on is clearly identified at the top (e.g., P11162731HAB0003).

Messages Table
Each row lists an underwriting message with:
Message # (e.g., M865, M866, M663) → system rule identifiers.
Description → the actual rule/advice text. For example:
M865: Full payment required. Credit info not available.
M866: No hit on personal info → check and re-enter details
M663: Insurer may order HITS report to verify claims.
Type → all marked as UW Rule (underwriting rules).
Select checkboxes → allows user to mark rules/messages as reviewed or applicable.

Action Buttons (bottom right)
Create Request: raise a follow-up or exception request.
View Requests: check existing requests tied to this quote.
Save Incomplete: save progress without finalizing.
Continue: move forward in the workflow (likely toward approval, confirmation, or policy issue).

Typical Workflow Step

At this stage, the underwriter or broker:

Reviews the rules/messages to understand what must be done before approval.
May update customer information, request missing reports, or confirm payment requirements.

Decides whether to:
Raise a request (if something needs escalation/clarification).
Save and come back later.
Or hit Continue to proceed (usually toward final quote confirmation).

Step 4: Rating Summary


Purpose
This screen consolidates the premium calculation and coverage breakdown for the insurance quote. It shows what the customer would pay, along with itemized coverages and limits.

Key Elements
Header Information


Reference Number: P11162731HAB0003 (the active quote).


Company / Branch: Aviva Insurance Company of Canada – Ontario branch.


Commission Variance: 0.000 (likely commission percentage difference from standard).


Premium Calculation Table (Top Summary)


Risk: property address (1386 Castlemore Ave, Markham).


Territory: risk rating zone (4/OZ02).


Sub Total: $2,183.00 — the calculated base premium.


Taxes: 0.00 (not yet added or handled in billing stage).


Finance Charge: 0.00 (no financing applied yet).


Risk Total: $2,183.00 — total premium for this risk.


Detailed Coverages Breakdown (Bottom Section)
 Each coverage line shows:


Coverage Type (e.g., Dwelling Building, Personal Property, Legal Liability, Sewer Backup, Overland Water, By-Law Coverage, etc.).


Amount of Insurance (limits, e.g., Dwelling = $702,450).


Deductible (e.g., $500 for dwelling, $2,500 for sewer backup/water damage).


Transaction Premium (incremental cost for that coverage).


Full Term Premium (cost for the policy term).


Some are included in the base premium (Incl), while others add specific amounts (e.g., Sewer Backup = $75, Overland Water = $120).


Navigation & Actions (Bottom Buttons)


Cancel Transaction / Return: back out without saving.


Create Request / View Requests: handle special underwriting or broker requests.


Notes: add internal comments.


Save Incomplete: save progress without finalizing.


Next: proceed to the Billing Summary stage.



Typical Workflow Step
At this stage, the broker/underwriter:
Reviews the premium total and all included coverages with limits and deductibles.


Ensures the premium matches underwriting expectations and client needs.


If changes are needed, they can go back to adjust coverages.


If correct, they click Next → this moves to Billing Summary, where payment methods, taxes, financing, and billing schedules are applied.


Step 5: Confirmation Stage


Purpose
To decide what to do with the completed quote:
Leave it as a saved quote, re-run pricing, or


Convert it into a live new business policy.



Key Elements
Reference Number


The active quote is clearly identified again: P11162731HAB0003.


Options (Radio Buttons)


Return to Client / Policy Search → go back without saving changes, returning to the search screen.


Save Quote and Re-Quote → save the current version, but allow rerunning underwriting/pricing (e.g., if new info is available).


Save Quote and Convert to New Business → this is the critical step. Selecting this option issues the policy, turning the quote into an active insurance contract.


Navigation Buttons


Cancel Transaction (bottom left): exit the process without saving.


Submit Quote (bottom right): confirms whichever option you selected above.



Typical Workflow Step
At this point, the broker/underwriter:
Verifies that the quote is accurate and ready.


Decides whether to just save (for later edits or client review) or convert to new business (bind the policy).


Clicks Submit Quote to finalize the action.


If Convert to New Business is selected (as it is in your screenshot), the system will:
Create a new active insurance policy in Aviva’s system.


Assign a policy number (different from the quote reference).


Trigger downstream steps (billing setup, issuance of policy documents, etc.).



⚡ In short: this is the final decision point — either save the quote for later or bind it into an official new insurance policy.
Step 6: Client / Policy Search Results


Purpose
After you’ve completed or attempted to convert the quote into new business, the system checks whether the client already exists in Aviva’s database. This ensures policies are linked to the right customer record.

Key Elements
Search Criteria (top box)


Company: Aviva Insurance Company of Canada


Branch: A-10 Ontario


Client Name: Yeung


Other filters: (First Initial, Postal Code not filled in).


Search Results (table)


Columns: Client Number, Client Name, Policy List, Address.


Message: “No items matching your search criteria were found.”


Meaning: the system did not find an existing client record under “Yeung” at this branch.


Next Step Options (bottom right buttons)


Create New Client → start a new client record (likely the correct next step since no match was found).


New Search → refine or retry search (e.g., different spelling, add postal code).



Typical Workflow Step
At this stage, the broker/underwriter must decide:
If the client already exists but wasn’t found → try New Search with more precise details (postal code, full name, etc.).


If the client truly doesn’t exist in Aviva’s system → click Create New Client to establish a new customer profile.


Once created, the system will link the quote to this new client record.


This is necessary before the policy can be issued.



⚡ In short: this is the client validation step. Since no record was found, the next step is usually “Create New Client” so the quote can be tied to a proper customer record and proceed to policy issuance.
Step 7: Client Entry screen



Purpose
To capture all the necessary client details (personal, address, broker references) that uniquely identify the insured in the system. Without this step, the quote can’t become a policy.

Key Elements
Company and Branch


Pre-filled with Aviva Insurance Company of Canada and Branch A-10 Ontario.


Broker # field available to link the client to a specific broker.


Client Type Section


Client Type: Insured (the policyholder).


Date of Birth: required for personal identification (example shows 01/01/1980).


Language: defaulted to English.


VIP flag, Member #, Broker Client ID fields available for special tagging or internal tracking.


Client Name Section


First Named Insured: Last Name (Yeung), First Name (Vincent).


Option for Company Name if the insured is a business entity instead of an individual.


Additional Named Insured: section for spouses, co-owners, or other parties to be added.


Legal Address


Address field: 1386 Castlemore Ave (pulled from quote earlier).


More address details can be added (postal code, city, province).


Navigation / Next Steps (bottom right buttons)


Additional Names: add co-insureds.


Additional Address: enter mailing or secondary addresses.


Bank Details: set up for billing/payment.


Confirm: finalize the client entry and save the record.



Typical Workflow Step
At this stage, the broker/underwriter:
Completes all mandatory client details (DOB, name, address, broker ID).


Adds any additional insureds or secondary addresses if needed.


Confirms and saves the client record.


Once confirmed:
The system creates a unique client profile tied to this individual.


The quote (P11162731HAB0003) can now be linked to this client.


The workflow then continues toward policy issuance (billing setup → final confirmation → policy number assignment).



⚡ In short: this is the client creation step, where you officially register the insured in Aviva’s system. The next action is usually to Confirm so the system can link the quote to the client record and move forward to billing and policy issuance.
Step 8: Confirmation page


Purpose
To confirm successful client creation and give the user the option to associate this new client with another existing client record (useful for households, businesses with multiple policies, or linked accounts).

Key Elements
Success Message


“The New Client Process is Complete. The Client has been submitted successfully.”


The system assigns a Client Number (8093847 in this case). This is the unique identifier for the insured in Aviva’s database.


Association Option


Question: “Do you want to Associate this Client with Another Client?”


Options: Yes / No (default is No).


Choosing Yes would allow linking this client to another client’s record (e.g., family members, joint ownership, related business entities).


Navigation


Confirm button (bottom right): proceed with the selected option.



Typical Workflow Step
At this point, the broker/underwriter should:
Decide if this client needs to be linked with another existing client.


Example: a husband/wife co-insured, or a business owner tied to multiple companies.


If not, leave it as No and click Confirm.


After confirming:
The new client record is finalized.


The workflow will return to the quote or policy issuance process, allowing you to link the quote (P11162731HAB0003) to this newly created client.


From here, the system moves toward converting the quote into a bound policy (policy number assignment, billing, and issuance).



⚡ In short: this is the finalization step of client creation. The next step after hitting Confirm is to link the quote to this client record, then continue to issue the policy.
Step 9: Policy Selection


Purpose
To review and confirm the key policy details (client, product, branch, broker, term) before the system formally issues the policy.

Key Elements
Client Details


Client Name: Vincent Cheuk Fun Yeung


Client Number: 8093847 (newly created in the last step).


Company and Branch


Company: Aviva Insurance Company of Canada


Branch: A-10 Ontario


Policy Information


Province: Ontario (risk location/province).


Product Type: Property (lines of business being issued).


Broker #: 27257 (the broker handling this policy).


Policy Term: Effective date = Sep 23, 2025; Term = 12 Months.


Navigation


Cancel Transaction (bottom left): abort the process.


Confirm (bottom right): finalize this policy setup and proceed.



Typical Workflow Step
At this point, the broker/underwriter:
Verifies that all policy details match what was quoted (client, product, coverage type, effective date).


Confirms that the correct broker and branch are associated.


If everything is correct, clicks Confirm to:


Convert the quote into a bound insurance policy.


Trigger policy number assignment (different from the quote number and client number).


Enable downstream steps: billing setup, premium payment scheduling, and generation of official policy documents.



⚡ In short: this is the policy issuance confirmation step. The next click (Confirm) finalizes the transition from “quote” to a live policy tied to the client record you just created.
Step 10: General Information screen


Purpose
To confirm the policy setup details (insured, broker, term, underwriting info) and ensure everything is accurate before proceeding through the rest of the new business issuance workflow.

Key Elements
Policy Identification


Policy Number: P97455511HAB (newly assigned; this is now a live policy, distinct from the quote reference).


Processing Date: Sep 10, 2025.


Status: In Progress (not yet finalized, still editable).


Company / Branch: Aviva Insurance Company of Canada – Ontario.


Client Number: 8093847 (from the client record you created).


Combined Policy Discount: Checked, meaning multi-policy discount may apply.


Policyholder Information


Insured Type: Individual.


Insured Name: Vincent Cheuk Fun Yeung.


Insured & Mailing Address: 1386 Castlemore Ave, Markham, ON.


Broker Information


Master Broker Name: Element Insurance – Broker #27257.


Address and phone number for the broker listed.


Policy Term


Effective Date: Sep 23, 2025.


Expiry Date: Sep 23, 2026.


Term: 12 months.


Policy Inception Date / Client Loyalty Date: Sep 23, 2025.


Options for renewal handling, lapse, replacement policy, etc.


Underwriting Information


Language: English.


Policy Province: Ontario.


Other underwriting fields can be completed here.


Navigation Buttons (bottom)


Cancel Transaction: abort.


Customer Consent: confirm client consent (usually required to bind policy).


Notes: internal remarks.


Policy General Page: navigate to broader policy details.


Save Incomplete: save progress without binding.


Next: proceed to the next tab (likely Risks or Coverages).



Typical Workflow Step
At this point, the broker/underwriter:
Reviews the policy number and confirms details match the quote and client record.


Completes any missing underwriting fields.


Records customer consent if required.


Clicks Next to proceed through the remaining new business workflow tabs:


Risks


Coverages


Billing Details


Rating Summary


Billing Summary


Confirmation


Each step will finalize the details until the policy is fully bound and ready for issuance.

⚡ In short: this screen is the policy creation confirmation screen — the system has generated the official policy number, and the next step is to move forward with coverages and billing setup before issuing the finalized policy documents.

