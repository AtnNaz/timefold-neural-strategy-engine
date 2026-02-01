# ⏳ TIMEFOLD: Neural Strategy Engine
**The Future is Not Predicted. It is Simulated.**

---

## 📖 Introduction

**TIMEFOLD** is an advanced **Multimodal Strategic Foresight Engine** powered by **Google's Gemini** models.

Unlike traditional chatbots that generate linear text, TIMEFOLD functions as a **recursive simulation environment**. It creates a **Council of Agents** — dynamic AI personas representing domain experts — to debate, analyze, and forecast divergent future scenarios.

TIMEFOLD bridges the gap between **Generative AI** and **Decision Theory**, allowing leaders, analysts, and curious minds to explore the **Tree of Possibilities** with mathematical confidence scores, transparent reasoning traces, and visual graph structures.

---

## 🚀 Key Features

### 🧠 1. Dynamic Agent Orchestration

TIMEFOLD doesn’t just *guess*. It recruits a team.

- **Context-Aware Recruitment**  
  Based on your input (e.g. *Crypto Crash* vs *Pandemic*), the system autonomously recruits **three unique domain experts** such as:
  - Macro-Economist  
  - Virologist  
  - Cyber-Security Analyst  

- **Adversarial Debate**  
  Agents simulate structured debates to uncover blind spots before generating future scenarios.

---

### 👁️ 2. Multimodal "Vision" Input

Don’t just tell — **show**.

- **Visual Grounding**  
  Upload stock charts, geopolitical maps, or supply chain diagrams.

- **Image-to-Simulation**  
  Gemini 3  analyzes visual inputs and injects them directly into the causal simulation logic.

---

### 🌳 3. Recursive Tree of Thought

Go down the rabbit hole.

- **Branching Narratives**  
  Each simulated future becomes a new starting point for further exploration.

- **Graph Visualization**  
  Interactive decision trees rendered via **Graphviz**, mapping causal relationships between events.

---

### 📊 4. Quantified Metrics & Transparency

No black boxes.

- **Reasoning Trace**  
  View logic chains, rejected alternatives, and assumptions.

- **Confidence Scores**  
  Every scenario includes:
  - Probability  
  - Impact Score  
  - Data Confidence  
  - Assumption Stability  

- **Risk Heatmap**  
  Visual color-coding (Green → Red) for instant risk assessment.

---

### 🦢 5. Chaos Mode (Black Swan Injection)

Test resilience against the unknown.

- **Chaos Injection**  
  Inject low-probability, high-impact **Black Swan events** to observe how timelines fracture.

---

## 🛠️ Technical Architecture

TIMEFOLD is built on a **modular reasoning pipeline**:

### 🔹 Input Layer
- Text prompts
- Image uploads (processed via **Pillow**)

### 🔹 Orchestration Layer
- Gemini 3 analyzes context
- Generates JSON-based **Agent Profiles**

### 🔹 Simulation Layer
- Injects agent personas into structured prompts
- Enforces strict **Pydantic schemas**
- Calculates probabilities and risk metrics

### 🔹 Visualization Layer
- Converts structured output into **DOT language**
- Renders causal graphs via **Graphviz**

---

## 🧰 Tech Stack

- **LLM:** Google Gemini 3 (`google-generativeai`)
- **Frontend / Backend:** Streamlit
- **Data Validation:** Pydantic
- **Graph Rendering:** Graphviz
- **Image Processing:** Pillow (PIL)

---

## 📸 Screenshots

<img width="1919" height="938" alt="image" src="https://github.com/user-attachments/assets/ddd04b1e-e450-456a-b736-20bc84b21cd3" />
<img width="1919" height="938" alt="image" src="https://github.com/user-attachments/assets/d76ff811-9ae1-405f-98e0-b26d543a6f24" />
<img width="1919" height="938" alt="image" src="https://github.com/user-attachments/assets/5f9664be-e914-418e-a2f8-7b409e771189" />
<img width="1919" height="938" alt="image" src="https://github.com/user-attachments/assets/efac236d-acba-4999-a86a-3e6a2395410b" />
<img width="1919" height="685" alt="image" src="https://github.com/user-attachments/assets/9b14fb0b-7594-43ae-99a4-1ad7675b932f" />


## ⚡ Quick Start Guide

Run TIMEFOLD locally in **3 simple steps**.

### ✅ Prerequisites
- Python **3.10+**
- Google AI Studio API Key

---

### 📦 Installation

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/burakdevelopment/timefold-neural-strategy-engine
cd timefold-neural-strategy-engine
```

#### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3️⃣ Configure API Key

Create a Streamlit secrets file:

* Windows: .streamlit\secrets.toml
* Mac/Linux: .streamlit/secrets.toml

- Add your API key:
```bash
GOOGLE_API_KEY = "YOURAPIKEY"
```

#### 4️⃣ Run the Engine
```bash
streamlit run timefold.py
```

## 🌍 Use Cases

* Crisis Management
- Simulate ripple effects of natural disasters on supply chains.

* Policy Making
- Analyze long-term societal impact of regulations (e.g. AI laws).

* Investment Strategy
- Stress-test portfolios against Black Swan market events.

* Education
- Teach systems thinking and causality.

## 🏆 Hackathon Context

* Built for the Google DeepMind Gemini Hackathon, leveraging the reasoning and multimodal capabilities of the Gemini model family to tackle complex strategic foresight problems.

## 📄 License
MIT License

* Developed with by [Burak / TIMEFOLD Team]
* Developed with by [Ali Toprak / TIMEFOLD Team]
