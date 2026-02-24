# 🛒 Commerce Sentiment Engine (Digikala Analyzer)
**Full-Stack Data Engineering & LLM-Powered Analytics Dashboard**

![image-20260224234623252](C:\Users\Shahab\AppData\Roaming\Typora\typora-user-images\image-20260224234623252.png)

This project is an educational and high-performance data engineering tool designed to demonstrate the seamless integration of web APIs, Large Language Models (LLMs), and data science metrics. It acts as an automated pipeline that crawls e-commerce product reviews, analyzes customer sentiment to extract structured JSON metadata, and dynamically generates statistical reports including the Net Promoter Score (NPS) via an interactive web dashboard.

---

## 🏗️ System Architecture & Enhancements
Built with modern software engineering principles, the architecture focuses on modularity, data persistence, and interactive data visualization.

### 1. Core Foundations
* **Modular Component Design:** Decouples the system into independent operational modules (`crawler`, `analyzer`, `db_manager`, `analytics`) to ensure clean code and scalability.
* **Smart API Crawler & Unbiased Sampling:** Directly interfaces with Digikala's public API to fetch real-time reviews, bypassing fragile HTML scraping. It implements a rigorous random sampling algorithm (e.g., extracting exactly 100 random reviews if the total exceeds 200, or 50% otherwise) to prevent statistical bias.
* **Zero-Config Local Database:** Utilizes `SQLite` (`reviews.db`) for robust, local data persistence, allowing the application to store and query historical AI extractions without requiring complex external database server setups.
* **Deterministic LLM Extraction:** Utilizes advanced prompt engineering with `gpt-4o` to enforce strict `json_object` response formatting, transforming raw Farsi comments into actionable metadata (satisfaction boolean, core reason, and an estimated 1-10 score).

---

## 🛠️ Main Features & Services

### 🧠 Semantic Intent Recognition & Scoring
* **Contextual Sentiment Analysis:** Analyzes user comments and synthesizes the core reason for customer satisfaction or dissatisfaction into a concise, 3-5 word summary.
* **AI-Estimated Scoring:** Evaluates the tone and vocabulary of the text to automatically estimate a numerical rating (1 to 10), even if the user didn't explicitly provide a star rating.

### 📊 Automated Analytics & Reporting
* **NPS Calculation:** Mathematically derives the Net Promoter Score (NPS) by categorizing the AI-estimated scores into Promoters (9-10), Passives (7-8), and Detractors (1-6).
* **Dynamic Visualizations:** Leverages `pandas` and `matplotlib` to generate and save high-resolution, analytical charts (Score Distribution Histograms and Satisfaction Pie Charts) directly to the local disk.

---

## 💎 Execution & Data Features

### 🖥️ Professional Interactive UI
* **Streamlit Dashboard:** Features a beautifully crafted, two-column interactive web interface with modern typography (Inter font), custom CSS, and direct chart download capabilities.
* **Live Terminal:** Includes a custom-styled, auto-scrolling execution log built into the UI that provides real-time transparency into the crawler's fetching and the LLM's processing loops.

### 🔒 Security & Standards
* **Environment Management:** Uses `python-dotenv` to keep API keys completely secure and out of the version control system.
* **Type Hinting:** Fully annotated with Python typing (`Dict`, `List`, `Any`, `str`) for enterprise-grade readability, developer experience, and maintainability.

---

## 🚀 How to Run

1. **Clone the Repo**
2.  **Setup Virtual Environment & Install Requirements:**
    ```bash
    python -m venv venv
    # Windows: .\venv\Scripts\activate
    pip install -r requirements.txt
    ```
3.  **Setup Environment:**
    Create a `.env` file in the root directory and add your credentials:
    
    ```env
    AVALAI_API_KEY=your_api_key
    ```
4.  **Launch the Web Application:**
    ```bash
    streamlit run app.py
    ```

---

## 🛠️ Tech Stack
* **Language:** Python 3.12+
* **Frontend/UI:** Streamlit (`streamlit`)
* **AI Providers:** OpenAI API Interface (`gpt-4o` via Avalai)
* **Data Science:** Pandas (`pandas`), Matplotlib (`matplotlib`)
* **Data Engineering:** SQLite3, Requests (`requests`), Regex
* **Environment & Security:** `python-dotenv`
* **Architecture Style:** Full-Stack Data App, Object-Oriented Programming (OOP)
