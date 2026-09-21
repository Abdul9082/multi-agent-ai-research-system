# 🧠 Multi-Agent AI Research System

An AI-powered multi-agent research system that automatically **searches the web, scrapes relevant information, generates a structured research report, and evaluates the report using a critic chain**.

The system uses **LangChain agents, Groq LLMs, Tavily web search, BeautifulSoup, and Streamlit** to create an end-to-end automated research workflow.

---

## 🚀 Overview

Researching a topic manually often requires searching through multiple websites, extracting useful information, organizing the findings, and reviewing the final result.

This project automates that workflow using specialized AI components.

A user enters a research topic through the Streamlit interface, and the system performs the following steps:

```text
User enters a topic
        ↓
   Search Agent
        ↓
   Scrape Agent
        ↓
   Writer Chain
        ↓
   Critic Chain
        ↓
Research Report + Feedback
```

Each component has a specific responsibility, making the overall system modular and easier to extend.

---

## ✨ Features

* 🔍 **AI Web Search Agent**

  * Searches for recent and reliable information using Tavily.
  * Selects relevant search results.

* 📚 **Web Scraping Agent**

  * Selects relevant URLs from the search results.
  * Extracts useful webpage content using BeautifulSoup.

* ✍️ **Research Writer**

  * Processes the collected research.
  * Generates a structured research report containing:

    * Introduction
    * Key Findings
    * Conclusion
    * Sources

* 🧐 **Critic Chain**

  * Reviews the generated report.
  * Evaluates accuracy, relevance, depth, clarity, completeness, organization, and source quality.
  * Provides scores, strengths, weaknesses, missing information, and areas for improvement.

* 🖥️ **Streamlit UI**

  * User-friendly research interface.
  * Suggested research topics.
  * Pipeline status tracking.
  * Research history during the current session.
  * Separate tabs for report, critic feedback, search results, scraped content, and logs.
  * Download generated reports as Markdown or JSON.

---

## 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │    Streamlit UI     │
                         │       app.py        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Research Pipeline │
                         │     pipeline.py     │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
          ┌─────────────────┐             ┌─────────────────┐
          │   Search Agent  │             │   Scrape Agent  │
          │                 │             │                 │
          │  Tavily Search  │             │ BeautifulSoup   │
          └────────┬────────┘             └────────┬────────┘
                   │                               │
                   └───────────────┬───────────────┘
                                   │
                                   ▼
                         ┌─────────────────────┐
                         │    Writer Chain     │
                         │   Research Report   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Critic Chain     │
                         │  Report Evaluation  │
                         └─────────────────────┘
```

---

## 🔄 How It Works

### 1. User Input

The user enters a research topic through the Streamlit application.

Example:

```text
Latest advances in solid-state batteries
```

The topic is passed to the research pipeline.

---

### 2. Search Agent

The Search Agent uses the `web_search` tool to search the web through Tavily.

The search tool returns information such as:

```text
Title
URL
Short snippet
```

The agent is instructed to return only the most relevant results and keep the response concise.

---

### 3. Scrape Agent

The Scrape Agent receives the search results and selects the most relevant URLs.

It then uses the `web_scrape` tool to extract webpage content.

BeautifulSoup removes unnecessary elements such as:

```text
script
style
nav
footer
```

The extracted text is then passed to the next stage.

---

### 4. Writer Chain

The Writer Chain combines:

```text
Search Results
+
Scraped Content
```

and passes the information to the research writer.

The writer generates a structured report containing:

```text
1. Introduction
2. Key Findings
3. Conclusion
4. Sources
```

The writer is instructed to use only the provided research and avoid inventing information.

---

### 5. Critic Chain

The generated report is passed to the Critic Chain.

The critic evaluates the report based on:

* Accuracy
* Relevance
* Depth
* Clarity
* Completeness
* Organization
* Source quality

It produces:

```text
Overall Score
Category Scores
Strengths
Weaknesses
Missing Information
Areas for Improvement
Critical Issues
Final Assessment
```

---

## 🛠️ Tech Stack

| Technology    | Purpose                           |
| ------------- | --------------------------------- |
| Python        | Core programming language         |
| LangChain     | Agent and LLM orchestration       |
| Groq          | LLM inference                     |
| GPT-OSS-120B  | Language model used by the agents |
| Tavily        | Web search                        |
| BeautifulSoup | Web scraping                      |
| Requests      | HTTP requests                     |
| Streamlit     | Web interface                     |
| python-dotenv | Environment variable management   |

---

## 📁 Project Structure

```text
Multi-Agent AI Research System/
│
├── app.py
├── agents.py
├── pipeline.py
├── tools.py
├── requirements.txt
├── .gitignore
│
├── .env
├── .venv/
└── __pycache__/
```

### File Descriptions

#### `app.py`

Contains the Streamlit user interface.

It handles:

* User topic input
* Suggested topics
* Pipeline execution
* Research history
* Results display
* Critic feedback display
* Search and scraped content display
* Downloading reports
* Console logs

---

#### `agents.py`

Contains the AI components used by the system.

It defines:

* Search Agent
* Scrape Agent
* Writer Chain
* Critic Chain

The project uses Groq's LLM through `ChatGroq`.

---

#### `tools.py`

Contains the external tools used by the agents.

### `web_search`

Uses Tavily to search the web.

### `web_scrape`

Uses Requests and BeautifulSoup to extract webpage text.

---

#### `pipeline.py`

Orchestrates the complete research workflow.

It connects:

```text
Search Agent
      ↓
Scrape Agent
      ↓
Writer Chain
      ↓
Critic Chain
```

The pipeline returns the collected results, generated report, and critic feedback as a state dictionary.

---

#### `requirements.txt`

Contains the Python dependencies required to run the project.

---

#### `.env`

Stores API credentials locally.

Example:

```env
TAVILY_API_KEY=your_tavily_api_key
GROQ_API_KEY=your_groq_api_key
```

**Never commit your `.env` file to GitHub.**

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=your_tavily_api_key
GROQ_API_KEY=your_groq_api_key
```

The application loads these variables using `python-dotenv`.

Make sure `.env` is included in `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/multi-agent-ai-research-system.git
```

Move into the project directory:

```bash
cd multi-agent-ai-research-system
```

Create and activate a virtual environment.

If using `uv`:

```bash
uv venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install the dependencies:

```bash
uv pip install -r requirements.txt
```

Create your `.env` file and add the required API keys.

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 💡 Example Workflow

Enter a topic such as:

```text
Latest advances in humanoid robotics
```

The system will:

```text
🔍 Search the web
       ↓
📚 Scrape relevant pages
       ↓
✍️ Generate research report
       ↓
🧐 Critique the report
       ↓
📄 Display final results
```

The Streamlit interface allows you to view each stage separately.

---

## 📊 Streamlit Interface

The application provides separate sections for:

### 📄 Report

Displays the generated research report and allows it to be downloaded as a Markdown file.

### 🧐 Critic Feedback

Displays the evaluation generated by the Critic Chain.

### 🔍 Search Results

Displays the information returned by the Search Agent.

### 📚 Scraped Content

Displays the content collected from selected webpages.

### 🖥️ Logs

Displays pipeline execution logs for debugging and monitoring.

---

## 🔒 Security

API keys are loaded through environment variables rather than being hardcoded into the source code.

The `.env` file should remain local and must not be committed to the repository.

Recommended `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
```

---

## 🎯 Learning Objectives

This project demonstrates practical implementation of:

* LLM application development
* LangChain agents
* Tool calling
* Multi-agent workflows
* Prompt engineering
* LCEL chains
* Web search integration
* Web scraping
* LLM-based report generation
* LLM-based evaluation
* Streamlit application development
* Environment variable management
* Modular Python project architecture

---

## 🔮 Future Improvements

Possible future extensions include:

* Persistent research history
* More specialized research agents
* Source credibility verification
* Parallel agent execution
* Improved citation handling
* PDF report generation
* Database integration
* Authentication
* Deployment with Streamlit Community Cloud

---

## 👨‍💻 Author

**Abdul Ahad Shaikh**

---

## 📄 License

This project is intended for educational and portfolio purposes.
