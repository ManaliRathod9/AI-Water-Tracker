# 💧 AI Water Tracker — Powered by Agentic AI

AI Water Tracker is an intelligent hydration assistant built with Python and Streamlit.

Unlike a traditional tracking dashboard, this system includes an autonomous AI agent that evaluates hydration input, selects a reasoning strategy, and delivers personalized guidance in real time.

The application is designed to function reliably across environments:

• Full LLM-powered reasoning (local development)  
• Autonomous fallback reasoning (cloud deployment)

The agent adapts automatically based on system capabilities.
---

# 🧠 Why This Is an Agent-Based System

Most dashboards collect data and display results.

This project introduces a dedicated reasoning layer — `WaterIntakeAgent`.

The agent is responsible for:

• Receiving hydration input  
• Interpreting intake in context  
• Selecting an appropriate reasoning method  
• Generating tailored advice  
• Adapting to runtime conditions  

The UI does not make decisions.

All evaluation flows through the agent.

---

# ⚙️ What This Application Does

The dashboard allows users to:

• Log daily water intake (in ml)  
• Automatically calculate recommended hydration based on weight and gender  
• Track daily goal completion  
• Monitor hydration streaks  
• View historical trends and a calendar heatmap  
• Download a PDF hydration summary  
• Receive optional email reminders  

Each intake log triggers the AI agent for contextual feedback.

---

# 🔍 How the Agent Works

At the core of this project is:

`WaterIntakeAgent`

An autonomous reasoning module that evaluates hydration input.

## Step-by-Step Flow

1. User logs water intake (e.g., 800 ml)  
2. `WaterIntakeAgent.analyze_intake()` is triggered  
3. Agent checks if Ollama (Llama3) is available  
4. Agent selects reasoning strategy  
5. Personalized hydration advice is returned  

---

# 🔁 Decision Architecture
```
User logs intake (e.g., 800ml)
        |
        v
WaterIntakeAgent.analyze_intake()
        |
        v
Is Ollama (Llama3) available?
        |
        +---------------------------+
        |                           |
       YES                         NO
(Local Development)       (Cloud / No Ollama)
        |                           |
        v                           v
LLM contextual reasoning     Rule-based reasoning
        |                           |
        v                           v
Personalized AI advice        Smart fallback advice
```

The system is environment-aware.

It always returns a response, regardless of deployment constraints.

---

# 🧠 Dual Reasoning Modes

## Local Mode (Full AI Reasoning)

• Uses Ollama  
• Uses Llama3 model  
• Performs contextual language reasoning  
• Generates natural-language personalized advice  

## Cloud Mode (Autonomous Fallback)

Streamlit Cloud does not support Ollama.

Instead of failing, the agent:

• Detects LLM unavailability  
• Switches to deterministic hydration logic  
• Continues functioning without interruption  

This ensures the application never breaks during deployment.

---

# 🏗️ System Architecture

The application is structured into clear layers:
```
System Architecture

        ┌──────────────────────────────┐
        │        dashboard.py          │
        │  UI + Visualization +        │
        │        Interaction           │
        └───────────────┬──────────────┘
                        │
                        ▼
        ┌──────────────────────────────┐
        │         src/agent.py         │
        │     Agent reasoning logic    │
        └───────────────┬──────────────┘
                        │
                        ▼
        ┌──────────────────────────────┐
        │        src/database.py       │
        │     SQLite persistence layer │
        └──────────────────────────────┘
```


The UI and reasoning layers are separated intentionally.

The dashboard never performs reasoning directly.

All hydration logic flows through the agent.

This makes the system modular and extendable.

---

# 📊 Core Features

Hydration Tracking  
Users log intake throughout the day.

Daily Progress Calculation  
Percentage completion toward recommended goal.

Streak System  
Tracks consecutive days meeting hydration target.

Gamification Layer  
Hydration levels based on streak performance.

Calendar Heatmap  
Monthly hydration visualization using Plotly.

PDF Report Export  
Generates a structured hydration summary.

Email Reminder System  
Optional hourly hydration reminders using Gmail SMTP.

Agent-Based Advice  
Every intake log triggers reasoning logic.

---

# 🛠️ Tech Stack

| Technology | Role in System |
|------------|---------------|
| Python 3.10 | Core language |
| Streamlit | Frontend UI layer |
| SQLite | Lightweight persistence |
| Ollama + Llama3 | Local LLM reasoning |
| Plotly | Data visualization |
| ReportLab | PDF generation |
| GitHub | Version control |
| Streamlit Cloud | Deployment |

# 🚀 Running Locally

## 1. Clone the repository

```
git clone https://github.com/ManaliRathod9/AI-Water-Tracker.git
cd AI-Water-Tracker
```

## 2. Create a virtual environment

Mac/Linux:

```
python -m venv venv
source venv/bin/activate
```

Windows:

```
python -m venv venv
venv\Scripts\activate
```

## 3. Install dependencies

```
pip install -r requirements.txt
```

## 4. Run the application

```
streamlit run dashboard.py
```

Open:

```
http://localhost:8501
```

---

# ☁️ Deployment (Streamlit Cloud)

1. Push code to GitHub  
2. Go to streamlit.io/cloud  
3. Connect your repository  
4. Set entry file to:

```
dashboard.py
```

5. Deploy  

The agent will automatically switch to fallback reasoning in cloud mode.

No additional configuration required.

---

# 📁 Project Structure

```
AI-Water-Tracker/
│
├── dashboard.py
├── src/
│   ├── agent.py
│   └── database.py
├── requirements.txt
└── README.md
```

---

# 💡 Agent Capabilities

| Capability | Description |
|------------|------------|
| 🧠 LLM Reasoning | Uses Llama3 to reason about hydration context |
| 🔁 Autonomous Fallback | Switches reasoning mode based on environment |
| 💬 Natural Language Output | Delivers advice in a human-friendly way |
| ⚡ Real-time Response | Agent responds instantly on every log |

---

# 🔮 Future Agent Enhancements

Planned improvements:

• Agent memory across days  
• Trend-based reasoning  
• Proactive low-hydration alerts  
• Multi-agent architecture  
• Adaptive daily goal generation  
• Behavioral pattern detection  

---
# 🌐 Live Demo

👉 **Streamlit App:** [https://your-streamlit-link-here](https://ai-water-tracker-uuytdjw4pkxggaxdqhvryg.streamlit.app/)
# 👩‍💻 Author

Manali Rathod  

