import os
import openai
import datetime

class OpenAIAgent:
    """Handles calls to the OpenAI Chat API."""
    def __init__(self, api_key: str = None, model: str = "gpt-4-0613", temperature: float = 0.7):
        key = api_key or os.getenv("OPENAI_API_KEY")
        assert key, "Define OPENAI_API_KEY in environment"
        openai.api_key = key
        self.model = model
        self.temperature = temperature

    def ask(self, prompt: str, system: str = None) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature
        )
        return resp.choices[0].message.content

class EmailAgent:
    """Generic email coordination and logging."""
    def __init__(self, log_list: list):
        self.log_list = log_list

    def send_email(self, to: str, subject: str, body: str) -> None:
        # Integrate SMTP or another email service here
        timestamp = datetime.datetime.now().isoformat()
        self.log_list.append({"to": to, "subject": subject, "time": timestamp})

class InspectorAgent:
    """Requests property inspection analysis from OpenAI."""
    def __init__(self, openai_agent: OpenAIAgent):
        self.openai = openai_agent

    def analyze(self, inspector: dict, property_info: dict) -> str:
        system = "You are a certified property inspector. Provide a fixes list and assign contractor categories."
        prompt = (
            f"You are {inspector['name']} ({inspector['certification']}). "
            f"Assess property at {property_info['formattedAddress']} priced ${property_info['lastSalePrice']} "
            f"with {property_info['bedrooms']} beds, {property_info['bathrooms']} baths, "
            f"{property_info['squareFootage']} sqft."
        )
        return self.openai.ask(prompt, system=system)

class ContractorAgent:
    """Generates emails to contractors based on inspection report."""
    def __init__(self, openai_agent: OpenAIAgent):
        self.openai = openai_agent

    def generate_email(self, category: str, contractor: dict, inspection_report: str) -> dict:
        system = "You are an assistant generating contractor outreach emails."
        subject = f"{category} Services Needed: {contractor.get('formattedAddress', '')}"
        prompt = (
            f"Based on this inspection report: {inspection_report}\n"
            f"Write an email to a {category} contractor named {contractor['name']} specifying the exact {category.lower()} work needed and asking for a quote."
        )
        body = self.openai.ask(prompt, system=system)
        return {"to": contractor['email'], "subject": subject, "body": body}