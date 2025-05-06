import os
import json
import pandas as pd
import pydeck as pdk
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

from agents import OpenAIAgent, EmailAgent, InspectorAgent, ContractorAgent

# 1) Load .env
load_dotenv()
# 2) Confirm API key
assert os.getenv("OPENAI_API_KEY"), "Missing OPENAI_API_KEY in environment"

# Instantiate agents
openai_agent     = OpenAIAgent(api_key=os.getenv("OPENAI_API_KEY"))
email_agent      = EmailAgent(st.session_state.get('sent_emails', []))
inspector_agent  = InspectorAgent(openai_agent)
contractor_agent = ContractorAgent(openai_agent)

# Paths
BASE  = Path(__file__).parent
PROPS = BASE / "synthetic_properties_j.json"
CONTS = BASE / "synthetic_angi_contractors_j.json"
INSPS = BASE / "synthetic_property_inspectors.json"

@st.cache_data
def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"File not found: {path}")
        return []

properties     = load_json(PROPS)
contractors_df = pd.DataFrame(load_json(CONTS))
inspectors_df  = pd.DataFrame(load_json(INSPS))

# Session defaults
for key, val in {
    'sent_emails':      [],
    'inspector_analysis': "",
    'filtered_records': []
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Sidebar & Login
st.sidebar.title("Login & Navigate")
if not st.session_state.get('logged_in'):
    if st.sidebar.button("Login"):
        st.session_state['logged_in'] = True
    else:
        st.sidebar.warning("Please log in.")
        st.stop()

page = st.sidebar.radio("Page:", ['Overview','Dashboard','Email','Angi Assistant'])

# --- Overview Tab ---
if page == 'Overview':
    st.title("Property Overview & Financials")
    addresses = [p['formattedAddress'] for p in properties]
    sel = st.selectbox('Select Property', addresses)
    prop = next(p for p in properties if p['formattedAddress'] == sel)

    st.subheader('Basic Information')
    st.write(f"**Address:** {prop['formattedAddress']}")
    st.write(f"**Price:** ${prop['lastSalePrice']:,}")
    st.write(f"**Beds/Baths/Sqft:** {prop['bedrooms']} / {prop['bathrooms']} / {prop['squareFootage']} sqft")

    # Financial projections
    purchase     = prop['lastSalePrice']
    agency_fee   = round(purchase * 0.06)
    taxes        = prop.get('propertyTaxes', {})
    last_year    = max(taxes.keys()) if taxes else None
    property_tax = taxes[last_year]['total'] if last_year else 0

    # Ask OpenAI for renovation cost if available
    ren_cost = 0
    if st.session_state['inspector_analysis']:
        prompt = (
            f"From this inspection report, provide a single total renovation cost: "
            f"{st.session_state['inspector_analysis']}"
        )
        ren_str = openai_agent.ask(prompt)
        try:
            ren_cost = int(''.join(filter(str.isdigit, ren_str.split()[0])))
        except:
            ren_cost = 0

    rent_est   = round(purchase * 0.008)
    total_cost = purchase + agency_fee + property_tax + ren_cost
    resale     = purchase + ren_cost * 1.2
    profit     = resale - total_cost

    st.subheader('Financial Projections')
    st.write(f"- **Agency Fee (6%):** ${agency_fee:,}")
    st.write(f"- **Property Tax:** ${property_tax:,}")
    st.write(f"- **Renovation Estimate:** ${ren_cost:,}")
    st.write(f"- **Total Cost:** ${total_cost:,}")
    st.write(f"- **Projected Resale:** ${resale:,.0f}")
    st.write(f"- **Profit:** ${profit:,}")
    st.write(f"- **Est. Monthly Rent:** ${rent_est:,}")

    st.subheader('Communication Log')
    if st.session_state['sent_emails']:
        st.table(pd.DataFrame(st.session_state['sent_emails']))
    else:
        st.write("No emails sent yet.")

# --- Dashboard Tab ---
elif page == 'Dashboard':
    st.title("Real Estate Investor Assistant")
    st.subheader("Filter & Map")

    # Filters
    city = st.selectbox("City", sorted({p['city'] for p in properties}))
    c1, c2 = st.columns(2)
    with c1:
        min_price = st.number_input(
            "Min Price", min_value=0, max_value=10_000_000, value=100_000, step=1_000
        )
        min_bed = st.number_input(
            "Min Beds", min_value=0, max_value=10, value=1, step=1
        )
    with c2:
        max_price = st.number_input(
            "Max Price", min_value=0, max_value=10_000_000, value=500_000, step=1_000
        )
        max_bed = st.number_input(
            "Max Beds", min_value=0, max_value=10, value=5, step=1
        )

    min_bath = st.number_input("Min Baths", min_value=0, max_value=10, value=1, step=1)
    max_bath = st.number_input("Max Baths", min_value=0, max_value=10, value=4, step=1)
    min_sqft = st.number_input("Min Sqft", min_value=0, max_value=20_000, value=600, step=100)
    max_sqft = st.number_input("Max Sqft", min_value=0, max_value=20_000, value=3_000, step=100)

    # Apply filters
    filtered = [
        p for p in properties
        if (
            p['city'] == city
            and min_price <= p['lastSalePrice'] <= max_price
            and min_bed <= p['bedrooms'] <= max_bed
            and min_bath <= p['bathrooms'] <= max_bath
            and min_sqft <= p['squareFootage'] <= max_sqft
        )
    ]
    st.session_state['filtered_records'] = filtered
    st.write(f"Found {len(filtered)} properties.")

    # Map
    if filtered:
        df = pd.DataFrame([
            {
                'lat': p['latitude'],
                'lon': p['longitude'],
                'formattedAddress': p['formattedAddress'],
                'lastSalePrice': p['lastSalePrice']
            } for p in filtered
        ])
        layer = pdk.Layer(
            'ScatterplotLayer',
            df,
            pickable=True,
            get_position='[lon, lat]',
            get_radius=100,
            get_fill_color=[255, 0, 0]
        )
        view = pdk.ViewState(
            latitude=df.lat.mean(),
            longitude=df.lon.mean(),
            zoom=10
        )
        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view))

    # Chat Insights
    st.markdown('---')
    st.subheader('Chat Insights')
    question = st.text_area('Ask about filtered properties')
    if st.button('Get Insights') and question:
        context = json.dumps([
            {k: p[k] for k in ['formattedAddress','lastSalePrice','bedrooms','bathrooms','squareFootage']}
            for p in filtered
        ])
        resp = openai_agent.ask(f"Properties: {context}\nQuestion: {question}")
        st.session_state['chat_history'] = (
            st.session_state.get('chat_history', []) + [(question, resp)]
        )
    for q, a in st.session_state.get('chat_history', []):
        st.markdown(f"**Q:** {q}\n**A:** {a}\n")

# --- Email Tab ---
elif page == 'Email':
    st.title('Email Coordination')
    props = st.session_state['filtered_records']
    if not props:
        st.warning('No properties selected in Dashboard.')
    else:
        sel = st.selectbox('Property', [p['formattedAddress'] for p in props])
        prop = next(p for p in props if p['formattedAddress'] == sel)

        # To Agent
        st.subheader('To Agent')
        to_a   = st.text_input('To', prop['realEstateAgent']['email'])
        subj_a = st.text_input('Subject', f"Inquiry: {prop['formattedAddress']}")
        body_a = st.text_area('Body', f"Hello,\nI am interested in {prop['formattedAddress']}.\nThanks.")
        if st.button('Send to Agent'):
            email_agent.send_email(to_a, subj_a, body_a)
            st.success(f"Sent to {to_a}")

        st.markdown('---')

        # To Inspector & Analysis
        st.subheader('To Inspector & Analysis')
        insp = inspectors_df[inspectors_df['zip_code'] == prop['zipCode']].iloc[0]
        to_i   = st.text_input('To', insp['email'])
        subj_i = st.text_input('Subject', f"Inspect: {prop['formattedAddress']}")
        body_i = st.text_area(
            'Body',
            f"Hello {insp['name']},\nPlease inspect {prop['formattedAddress']}.\nThanks."
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Send to Inspector'):
                email_agent.send_email(to_i, subj_i, body_i)
                st.success(f"Sent to {to_i}")
        with col2:
            if st.button('Get Analysis'):
                report = inspector_agent.analyze(insp.to_dict(), prop)
                st.session_state['inspector_analysis'] = report

        if st.session_state['inspector_analysis']:
            st.markdown('**Inspection Report:**')
            st.write(st.session_state['inspector_analysis'])

# --- Angi Assistant Tab ---
elif page == 'Angi Assistant':
    st.title('Contractor Recommendations')
    props = st.session_state['filtered_records']
    if not props or not st.session_state['inspector_analysis']:
        st.warning('Run analysis in Email tab first.')
    else:
        sel2  = st.selectbox('Property', [p['formattedAddress'] for p in props])
        prop2 = next(p for p in props if p['formattedAddress'] == sel2)

        st.subheader('Inspection Report')
        st.write(st.session_state['inspector_analysis'])

        st.markdown('---')
        st.subheader('Generate Contractor Emails')
        dfc = contractors_df[contractors_df['zip_code'] == prop2['zipCode']]
        for cat in dfc['service_category'].unique():
            contractor = dfc[dfc['service_category'] == cat].nlargest(1, 'rating').iloc[0]
            email_data = contractor_agent.generate_email(cat, contractor.to_dict(), st.session_state['inspector_analysis'])

            st.text_input('To', email_data['to'], key=f"to_{cat}")
            st.text_input('Subject', email_data['subject'], key=f"subj_{cat}")
            st.text_area('Body', email_data['body'], key=f"body_{cat}")

            if st.button(f"Send to {contractor['name']}", key=f"send_{cat}"):
                email_agent.send_email(email_data['to'], email_data['subject'], email_data['body'])
                st.success(f"Sent to {contractor['name']}")