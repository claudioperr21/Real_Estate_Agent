# Real Estate Investor Assistant (Streamlit Multi‑Agent App)

A Streamlit‑based real‑estate investment assistant that integrates multiple “agents” powered by the OpenAI API:

- **OpenAIAgent**: handles all LLM calls  
- **EmailAgent**: logs and (stub‑)sends emails to owners, inspectors, and contractors  
- **InspectorAgent**: generates a property inspection analysis  
- **ContractorAgent**: drafts outreach emails to contractors based on the inspection report  

This project demonstrates how to orchestrate specialized agents in a single interactive dashboard, covering property overview, filtering & mapping, email coordination, and contractor recommendations.

---

## Repository layout

- **agents.py**  
  Contains the four agent classes: `OpenAIAgent`, `EmailAgent`, `InspectorAgent`, `ContractorAgent`.
- **app.py**  
  Streamlit application that wires together the agents into four tabs:
  - **Overview**: property details & financial projections  
  - **Dashboard**: filter properties and view on map + chat insights  
  - **Email**: send inquiries to agents & inspectors and retrieve analyses  
  - **Angi Assistant**: draft and log contractor outreach emails
- **synthetic_properties_j.json**, **synthetic_angi_contractors_j.json**, **synthetic_property_inspectors.json**  
  Sample data for properties, contractors, and inspectors.
- **.env**, **requirements.txt**, **README.md**  
  Root‑level environment setup, dependencies and this guide.

---

## Getting started

Follow these steps to run the app locally.

### 1. Clone the repository

```bash
git clone https://github.com/claudioperr21/realestate-agent.git
cd realestate-agent

Create a .env file in the project root:
OPENAI_API_KEY=your_openai_api_key
5. Run the Streamlit app
streamlit run app.py
Your browser will open at http://localhost:8501 with the four‑tab interface.

Usage overview
Login & Navigate (sidebar)
Click Login to unlock the four tabs:

Overview: View basic property info and financial projections.

Dashboard: Filter by city, price, beds/baths, square footage; view on map; ask free‑form questions about the selection.

Email:

Send a buyer inquiry to the listing agent

Request an inspection from a matched inspector and retrieve an AI‑generated report

Angi Assistant: Using the inspection report, draft contractor emails by trade category, then send and log them.

Data Sources
The app reads the sample JSON files in the root. You can replace them with your own data of the same schema.

Agent Architecture

OpenAIAgent wraps calls to openai.ChatCompletion

EmailAgent stubs real email sending and logs to st.session_state['sent_emails']

InspectorAgent generates a fixes list and contractor categories based on property details

ContractorAgent drafts trade‑specific outreach emails from the inspector’s report
