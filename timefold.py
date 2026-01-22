import streamlit as st
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Optional
from graphviz import Digraph
import json
import time
from PIL import Image
import io
import random

st.set_page_config(page_title="TIMEFOLD: Neural Strategy Engine", page_icon="🔮", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0E1117; color: #C9D1D9; }
    h1 {
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }
    .stButton>button {
        border: 1px solid #00C9FF; border-radius: 6px;
        background-color: rgba(0, 201, 255, 0.05); color: #00C9FF;
        font-family: 'Courier New'; font-weight: bold; transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #00C9FF; color: black; box-shadow: 0 0 15px #00C9FF;
    }
    .agent-card {
        padding: 20px; border-radius: 12px; background-color: #161B22;
        border-left: 5px solid #92FE9D; margin-bottom: 15px; height: 100%;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3); transition: transform 0.2s;
    }
    .agent-card:hover { transform: translateY(-5px); }
    .trace-box {
        background-color: #1F1F1F; border-left: 3px solid #FFA500;
        padding: 10px; font-size: 0.85em; margin-top: 10px; font-family: monospace; color: #d0d0d0;
    }
    .quick-btn { margin: 5px; }
</style>
""", unsafe_allow_html=True)

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = None

if not api_key:
    st.error("SECURITY ALERT: API Key not found. Please set `GOOGLE_API_KEY` in Streamlit secrets")
    st.info("If running locally create a `.streamlit/secrets.toml` file")
    st.stop()

genai.configure(api_key=api_key)

class AgentProfile(BaseModel):
    name: str = Field(description="Name of the expert (No titles like Dr./Prof., use generic or code names)")
    role: str = Field(description="Specific Expertise (e.g., Supply Chain Analyst)")
    stance: str = Field(description="Strategic stance (e.g., Risk-Averse, Disruptive)")
    avatar: str = Field(description="Single emoji representing the persona")

class Council(BaseModel):
    agents: List[AgentProfile]

class ScenarioNode(BaseModel):
    id: str
    title: str = Field(description="Short, punchy title")
    description: str
    probability: int
    time_horizon: str = Field(description="Short Term (0-6m), Mid Term (1-2y), or Long Term (5y+)")
    risk_level: str = Field(description="Low, Medium, High, Critical")
    impact_score: int = Field(description="1-10")
    data_confidence: int = Field(description="Confidence in underlying data (0-100)")
    assumption_stability: int = Field(description="How stable are the assumptions? (0-100)")
    reasoning_trace: str = Field(description="Brief explanation of the logic chain and rejected alternatives.")

class SimulationOutput(BaseModel):
    scenarios: List[ScenarioNode]
    synthesis: str
    black_swan_alert: Optional[str] = Field(description="If a low probability high impact event was detected, describe it here.")

def recruit_agents(context, image_part=None):
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash', 
        generation_config={"response_mime_type": "application/json", "response_schema": Council}
    )
    prompt = f"MISSION: Recruit 3 distinct strategic experts to analyze: {context}. RULES: No honorifics. Diverse perspectives."
    inputs = [prompt]
    if image_part:
        inputs.append(image_part)
        inputs.append("Analyze visual data.")
    
    response = model.generate_content(inputs)
    return json.loads(response.text)

def run_simulation(context, agents, image_part=None, inject_chaos=False):
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        generation_config={"response_mime_type": "application/json", "response_schema": SimulationOutput}
    )
    
    agents_desc = "\n".join([f"- {a['name']} ({a['role']}): {a['stance']}" for a in agents['agents']])
    
    chaos_prompt = ""
    if inject_chaos:
        chaos_prompt = "⚠️ INJECT A BLACK SWAN EVENT: Introduce a low-probability, high-impact disruption into the scenarios."

    prompt = f"""
    You are TIMEFOLD, an Advanced Strategic Foresight Engine.
    ACTIVE COUNCIL: {agents_desc}
    TASK: Simulate a debate, generate 3 divergent future scenarios. Include reasoning traces and confidence metrics.
    {chaos_prompt}
    CURRENT STATE: {context}
    """
    
    inputs = [prompt]
    if image_part: inputs.extend([image_part, "Incorporate visual insights."])

    try:
        response = model.generate_content(inputs)
        return json.loads(response.text)
    except Exception as e:
        st.error(f"Simulation Error: {e}")
        return None

def generate_markdown_report(history):
    report = "# TIMEFOLD STRATEGIC REPORT\n"
    report += f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    for i, step in enumerate(history):
        report += f"## Step {i+1}: {step['title']}\n"
        report += f"_{step['description']}_\n\n"
        if 'reasoning_trace' in step:
            report += f"> **Reasoning:** {step['reasoning_trace']}\n\n"
        if 'risk_level' in step:
            report += f"**Metrics:** Risk: {step['risk_level']} | Prob: {step['probability']}%\n"
        report += "---\n"
    return report

def draw_advanced_tree(history, options):
    dot = Digraph(format='png')
    dot.attr(bgcolor='#0E1117', rankdir='LR')
    dot.attr('node', fontname='Helvetica', fontcolor='white')
    dot.attr('edge', color='#555555', arrowsize='0.7', fontcolor='#AAAAAA')

    for i, step in enumerate(history):
        node_id = f"H_{i}"
        label = f"{step['title']}"
        dot.node(node_id, label=label, shape='box', style='filled', fillcolor='#21262D', penwidth='2.0', color='white')
        if i > 0: dot.edge(f"H_{i-1}", node_id)

    last_id = f"H_{len(history)-1}"
    if options:
        for opt in options.get("scenarios", []):
            opt_id = f"OPT_{opt['id']}"
            risk = opt.get('risk_level', '').lower()
            color = '#8B0000' if 'critical' in risk else '#B22222' if 'high' in risk else '#006400' if 'low' in risk else '#003366'
            
            label = f"""<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0"><TR><TD><B>{opt['title']}</B></TD></TR>
            <TR><TD><FONT POINT-SIZE="10">{opt['time_horizon']}</FONT></TD></TR>
            <TR><TD><FONT POINT-SIZE="10">Prob: {opt['probability']}%</FONT></TD></TR></TABLE>>"""
            
            dot.node(opt_id, label=label, shape='note', style='filled', fillcolor=color)
            dot.edge(last_id, opt_id, label=f"Risk: {opt['risk_level']}")
    return dot

with st.sidebar:
    st.header("⚙️ Configuration")
    show_reasoning = st.toggle("🧠 Show Reasoning Trace", value=True)
    st.markdown("### Vision Input")
    uploaded_file = st.file_uploader("Upload Chart/Map/Photo", type=["jpg", "png", "jpeg"])
    
    image_part = None
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Visual Context Loaded", use_column_width=True)
        image_part = image

    st.divider()
    if st.button("🔄 Reset System", type="primary"):
        st.session_state.clear()
        st.rerun()

if 'stage' not in st.session_state: st.session_state.stage = 'INPUT'
if 'history' not in st.session_state: st.session_state.history = []
if 'agents' not in st.session_state: st.session_state.agents = None
if 'simulation' not in st.session_state: st.session_state.simulation = None

st.title("TIMEFOLD")
st.caption("Multimodal Strategic Foresight Engine | Powered by Gemini")

if st.session_state.stage == 'INPUT':
    st.markdown("### Initialize Simulation")
    
    
    st.markdown("Or choose a preset:")
    c1, c2, c3 = st.columns(3)
    if c1.button("📉 Crypto Crash"):
        st.session_state.history.append({"title": "START", "description": "Bitcoin crashes below $30k, triggering global regulatory crackdown."})
        st.session_state.stage = 'RECRUITING'
        st.rerun()
    if c2.button("🦠 Pandemic 2.0"):
        st.session_state.history.append({"title": "START", "description": "A new respiratory virus with high transmission rate is detected in major transit hubs."})
        st.session_state.stage = 'RECRUITING'
        st.rerun()
    if c3.button("🤖 AI Ban"):
        st.session_state.history.append({"title": "START", "description": "UN passes a resolution banning autonomous AI development above a certain compute threshold."})
        st.session_state.stage = 'RECRUITING'
        st.rerun()

    user_input = st.text_area("Define your own scenario:", placeholder="E.g., A sudden collapse in the global lithium supply chain...", height=100)
    
    if st.button("INITIALIZE SYSTEM", use_container_width=True):
        if user_input or image_part:
            input_text = user_input if user_input else "Analyze the uploaded visual data."
            st.session_state.history.append({"title": "START", "description": input_text})
            st.session_state.stage = 'RECRUITING'
            st.rerun()
        else:
            st.warning("Please enter text or upload an image.")


elif st.session_state.stage == 'RECRUITING':
    last_context = st.session_state.history[-1]['description']
    
    with st.status("📡 Establishing Neural Link...", expanded=True) as status:
        st.write("Processing context and visual data...")
        time.sleep(0.5)
        st.write("Recruiting domain experts...")
        st.session_state.agents = recruit_agents(last_context, image_part)
        status.update(label="✅ Council Assembled", state="complete", expanded=False)
    
    st.subheader("🧠 The Strategic Council")
    cols = st.columns(3)
    for i, agent in enumerate(st.session_state.agents['agents']):
        with cols[i]:
            st.markdown(f"""
            <div class="agent-card">
                <div style="font-size: 2.5em; text-align:center;">{agent['avatar']}</div>
                <div style="font-weight: bold; color: #00C9FF; text-align:center; font-size: 1.1em;">{agent['name']}</div>
                <div style="font-size: 0.9em; opacity: 0.8; text-align:center;">{agent['role']}</div>
                <hr style="border-color: #333;">
                <div style="font-size: 0.85em; font-style: italic;">"{agent['stance']}"</div>
            </div>
            """, unsafe_allow_html=True)
            
    if st.button("START SIMULATION ➡️", use_container_width=True):
        st.session_state.stage = 'SIMULATING'
        st.rerun()

elif st.session_state.stage == 'SIMULATING':
    last_context = st.session_state.history[-1]['description']
    
    
    inject_chaos = False
    if st.button("Inject Chaos (Black Swan Event)", type="secondary"):
        inject_chaos = True
        st.session_state.simulation = None 
    
    if not st.session_state.simulation:
        with st.spinner("Simulating Futures... (Agents debating)"):
            st.session_state.simulation = run_simulation(last_context, st.session_state.agents, image_part, inject_chaos)
    
    
    tab1, tab2 = st.tabs(["🕸️ Interactive Graph", "📋 Executive Summary"])
    
    with tab1:
        st.graphviz_chart(draw_advanced_tree(st.session_state.history, st.session_state.simulation), use_container_width=True)
    
    with tab2:
        st.success("Council Synthesis")
        st.write(st.session_state.simulation['synthesis'])
        if st.session_state.simulation.get('black_swan_alert') or inject_chaos:
             st.error(f"⚠️ BLACK SWAN / CHAOS DETECTED: {st.session_state.simulation.get('black_swan_alert', 'Chaos Injection Active')}")

    st.divider()
    
    st.subheader("📍 Select Future Path")
    scenarios = st.session_state.simulation.get("scenarios", [])
    
    cols = st.columns(len(scenarios))
    for i, sc in enumerate(scenarios):
        with cols[i]:
            with st.container(border=True):
                risk_color = ":red" if "Critical" in sc['risk_level'] else ":orange" if "High" in sc['risk_level'] else ":green"
                st.markdown(f"#### {risk_color}[{sc['title']}]")
                st.caption(f"Time Horizon: {sc['time_horizon']}")
                
                c1, c2 = st.columns(2)
                c1.metric("Prob", f"{sc['probability']}%")
                c2.metric("Impact", f"{sc['impact_score']}/10")
                
                st.write(sc['description'])
                
                if show_reasoning:
                    with st.expander("🔍 Reasoning Trace"):
                        st.markdown(f"""
                        <div class="trace-box">
                        <b>Logic:</b> {sc['reasoning_trace']}<br>
                        <b>Data Conf:</b> {sc['data_confidence']}%<br>
                        <b>Assumption Stability:</b> {sc['assumption_stability']}%
                        </div>
                        """, unsafe_allow_html=True)
                
                if st.button("Explore This Path", key=f"btn_{i}", use_container_width=True):
                    st.session_state.history.append(sc)
                    st.session_state.simulation = None
                    st.session_state.agents = None
                    st.session_state.stage = 'RECRUITING'
                    st.rerun()

    st.divider()
    report_md = generate_markdown_report(st.session_state.history)
    st.download_button(
        label="📄 Download Strategic Report (Markdown)",
        data=report_md,
        file_name="timefold_report.md",
        mime="text/markdown"
    )