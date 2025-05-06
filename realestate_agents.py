# realestate_agents.py
import os
from dotenv import load_dotenv
import openai

# Load .env before using OPENAI_API_KEY
load_dotenv()

from typing import Any, Dict, List, Union, Optional
from pydantic import BaseModel

# Import the framework from the installed `agents` package
from agents import Agent, Runner, handoff, function_tool, InputGuardrail, GuardrailFunctionOutput, input_guardrail
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

# --- Core OpenAI Wrapper ---
class OpenAIAgent:
    """Handles calls to the OpenAI Chat API using v1.0+ Python SDK interface."""
    def __init__(self, api_key: str = None, model: str = "gpt-4-0613", temperature: float = 0.7):
        key = api_key or os.getenv("OPENAI_API_KEY")
        assert key, "Define OPENAI_API_KEY in environment"
        openai.api_key = key
        self.model = model
        self.temperature = temperature

    def ask(self, prompt_or_messages: Union[str, List[Dict[str, str]]], system: Optional[str] = None) -> str:
        # Normalize to messages list
        if isinstance(prompt_or_messages, str):
            messages: List[Dict[str, str]] = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt_or_messages})
        else:
            messages = prompt_or_messages
        # Use new v1 interface
        resp = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature
        )
        return resp.choices[0].message.content

# Shared OpenAI wrapper instance
openai_agent = OpenAIAgent()

# --- Function Tools ---
@function_tool
def inspect_property(inspector: Dict[str, Any], property_info: Dict[str, Any]) -> str:
    """Run property inspection via OpenAI."""
    system = "You are a certified property inspector. Provide a fixes list and assign contractor categories."
    prompt = (
        f"You are {inspector['name']} ({inspector['certification']}). "
        f"Assess property at {property_info['formattedAddress']} priced ${property_info['lastSalePrice']} "
        f"with {property_info['bedrooms']} beds, {property_info['bathrooms']} baths, "
        f"{property_info['squareFootage']} sqft."
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}
    ]
    return openai_agent.ask(messages)

@function_tool
def create_contractor_email(category: str, contractor: Dict[str, Any], inspection_report: str) -> Dict[str, str]:
    """Generate contractor outreach email via OpenAI."""
    system = "You are an assistant generating contractor outreach emails."
    subject = f"{category} Services Needed: {contractor.get('formattedAddress', '')}"
    prompt = (
        f"Based on this inspection report: {inspection_report}\n"
        f"Write an email to a {category} contractor named {contractor['name']} specifying the exact {category.lower()} work needed and asking for a quote."
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}
    ]
    body = openai_agent.ask(messages)
    return {"to": contractor['email'], "subject": subject, "body": body}

# --- Guardrail: Ensure inspection before outreach ---
class InspectionCheck(BaseModel):
    has_inspection: bool
    reasoning: str

async def require_inspection(ctx, agent, inputs):
    has = 'inspection_report' in inputs
    return GuardrailFunctionOutput(output_info=has, tripwire_triggered=not has)

# --- Agent Definitions with explicit descriptions ---
inspector_agent = Agent(
    name="PropertyInspector",
    instructions="Use inspect_property(inspector, property_info) to analyze the property.",
    tools=[handoff(inspect_property, tool_description_override="Run property inspection")]  # description override
)

contractor_agent = Agent(
    name="ContractorOutreach",
    instructions="Use create_contractor_email(category, contractor, inspection_report) after inspection.",
    tools=[handoff(create_contractor_email, tool_description_override="Generate contractor emails")],
    input_guardrails=[InputGuardrail(guardrail_function=require_inspection)]
)

triage_agent = Agent(
    name="RealEstateTriage",
    instructions=prompt_with_handoff_instructions(
        """
        You have two tools:
         - inspect_property
         - create_contractor_email
        Invoke exactly one based on inputs.
        """
    ),
    handoffs=[
        handoff(inspect_property, tool_description_override="Run property inspection"),
        handoff(create_contractor_email, tool_description_override="Generate contractor emails")
    ]
)

# --- Orchestration Helper ---
async def run_real_estate_workflow(
    inspector: Dict[str, Any],
    property_info: Dict[str, Any],
    contractors: Optional[List[Dict[str, Any]]] = None
) -> Any:
    """
    Executes the triage -> inspection -> outreach pipeline.
    """
    items: List[Dict[str, Any]] = [{"role": "system", "content": "Manage property inspection and contractor outreach."}]
    items.append({"role": "user", "content": f"inspector: {inspector}"})
    items.append({"role": "user", "content": f"property_info: {property_info}"})
    if contractors:
        items.append({"role": "user", "content": f"contractors: {contractors}"})
    run = await Runner.run(triage_agent, items)
    return run.final_output

# --- Backwards-Compatible Wrappers for app.py ---
import datetime

class EmailAgent:
    def __init__(self, log_list: List[Dict[str, Any]]):
        self.log = log_list

    def send_email(self, to: str, subject: str, body: str):
        ts = datetime.datetime.now().isoformat()
        self.log.append({"to": to, "subject": subject, "time": ts})

class InspectorAgent:
    def __init__(self, openai_agent: OpenAIAgent):
        self.openai = openai_agent

    def analyze(self, inspector: Dict[str, Any], property_info: Dict[str, Any]) -> str:
        # Inline inspector logic instead of calling the FunctionTool directly
        system = "You are a certified property inspector. Provide a fixes list and assign contractor categories."
        prompt = (
            f"You are {inspector['name']} ({inspector['certification']}). "
            f"Assess property at {property_info['formattedAddress']} priced ${property_info['lastSalePrice']} "
            f"with {property_info['bedrooms']} beds, {property_info['bathrooms']} baths, "
            f"{property_info['squareFootage']} sqft."
        )
        return self.openai.ask(prompt, system=system)

class ContractorAgent:
    def __init__(self, openai_agent: OpenAIAgent):
        self.openai = openai_agent

    def generate_email(self, category: str, contractor: Dict[str, Any], inspection_report: str) -> Dict[str, Any]:
        # Inline email generation logic
        system = "You are an assistant generating contractor outreach emails."
        subject = f"{category} Services Needed: {contractor.get('formattedAddress', '')}"
        prompt = (
            f"Based on this inspection report: {inspection_report}\n"
            f"Write an email to a {category} contractor named {contractor['name']} specifying the exact {category.lower()} work needed and asking for a quote."
        )
        body = self.openai.ask(prompt, system=system)
        return {"to": contractor['email'], "subject": subject, "body": body}
