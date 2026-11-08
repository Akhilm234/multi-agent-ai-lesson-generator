# 🤖 Multi-Agent AI Lesson Generator

An AI-powered multi-agent system built using **Python and Google's Gemini API** that automatically generates, evaluates, and improves educational lessons through intelligent agent collaboration.

The project demonstrates how multiple AI agents can work together to complete a task, evaluate results, and iteratively improve the output with minimal human intervention.

## 🚀 Project Overview

The Multi-Agent AI Lesson Generator consists of three main components:

- **Generator Agent:** Generates structured educational lessons based on a given topic using Gemini.
- **Evaluator Agent:** Reviews generated lessons and evaluates their quality against defined criteria.
- **Orchestrator:** Coordinates the agents and manages the complete generate-evaluate-regenerate workflow.

If the generated lesson does not meet the evaluation criteria, the orchestrator sends feedback to the Generator Agent to improve the lesson. This process continues for a maximum of two retries.

## 🏗️ System Architecture

```text
             User Input (Topic)
                     |
                     v
             Orchestrator
                     |
                     v
             Generator Agent
                     |
                     v
              Generated Lesson
                     |
                     v
             Evaluator Agent
                     |
                     v
              Quality Evaluation
                     |
                     v
              Orchestrator
                     |
              +------+------+
              |             |
             PASS          FAIL
              |             |
              v             v
          Final Output   Regenerate
                            |
                            v
                      Generator Agent
                       (Max 2 Retries)
```

## ✨ Key Features

- Multi-agent architecture using specialized AI agents.
- Gemini API integration for AI-powered content generation.
- Automated lesson quality evaluation.
- Feedback-driven lesson regeneration.
- Orchestration of multiple agents.
- Maximum retry limit to prevent infinite execution.
- Structured evaluation results in JSON format.
- Generated educational content in Markdown format.

## 🛠️ Technology Stack

| Technology        | Purpose                              |
| ----------------- | ------------------------------------ |
| Python            | Core development                     |
| Google Gemini API | AI-powered generation and evaluation |
| Google GenAI SDK  | Gemini API integration               |
| Python-dotenv     | Environment variable management      |
| JSON              | Evaluation results                   |
| Markdown          | Generated lesson output              |
| Git & GitHub      | Version control                      |

## 📂 Project Structure

```text
self-evaluating-lesson-generator/
│
├── agents/
│   ├── generator.py
│   └── evaluator.py
│
├── outputs/
│   ├── lesson.md
│   └── evaluation.json
│
├── orchestrator.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/Akhilm234/multi-agent-ai-lesson-generator.git
```

### 2. Navigate to the project directory

```bash
cd multi-agent-ai-lesson-generator
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

**Important:** Never commit your `.env` file or expose your API key publicly.

### 6. Run the application

```bash
python main.py
```

## 📄 Output Files

The system generates two important output files:

**1. lesson.md**

Contains the generated educational lesson in Markdown format.

**2. evaluation.json**

Contains the evaluator's assessment of the generated lesson, including evaluation results and feedback.

## 🔄 Agent Workflow

1. The user provides a topic.
2. The Orchestrator invokes the Generator Agent.
3. The Generator Agent creates a lesson using Gemini.
4. The Evaluator Agent assesses the generated lesson.
5. The Orchestrator checks the evaluation result.
6. If the lesson passes, the final output is accepted.
7. If it fails, evaluation feedback is sent back to the Generator Agent.
8. The system regenerates the lesson, with a maximum of two retries.

## 🎯 Learning Outcomes

Through this project, I explored:

- Building multi-agent AI applications.
- Integrating Large Language Models using APIs.
- Designing agent-specific responsibilities.
- Implementing automated evaluation mechanisms.
- Creating feedback-driven AI workflows.
- Managing agent execution using an orchestrator.
- Handling structured outputs and regeneration logic.

## 🔮 Future Enhancements

Potential improvements include:

- FastAPI integration for exposing the system through REST APIs.
- Web-based interface for interactive lesson generation.
- Advanced evaluation metrics and scoring.
- Support for multiple LLM providers.
- Persistent storage for generated lessons and evaluation history.

## 👨‍💻 Author

**Akhil M**

GitHub: [@Akhilm234](https://github.com/Akhilm234)

---

⭐ If you find this project interesting, feel free to explore the repository!
