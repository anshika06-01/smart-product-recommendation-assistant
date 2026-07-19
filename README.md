# 🛍️ Smart Product Recommendation Assistant

> An AI-powered shopping assistant that provides intelligent product recommendations using **Retrieval-Augmented Generation (RAG)** and **Google Gemini**. The system understands natural language queries, retrieves the most relevant products from a product catalogue, and generates personalized recommendations with the help of a Large Language Model.

---

# 📖 Project Overview

The **Smart Product Recommendation Assistant** is designed to simplify online shopping by allowing users to search for products using natural language instead of traditional keyword-based searches.

The application combines **semantic product retrieval** with **Google Gemini** to generate context-aware recommendations. By using Retrieval-Augmented Generation (RAG), the assistant retrieves relevant product information before generating a response, making recommendations more accurate and reliable.

---

# ✨ Key Features

- 🤖 AI-powered shopping assistant
- 🔍 Natural language product search
- 📦 Product recommendations from a product catalogue
- 🧠 Context-aware responses using RAG
- 💬 Conversational chat interface
- 📊 Product filtering by category, brand, price, and rating
- ⚡ FastAPI backend with Streamlit frontend
- 🔄 Session-based conversation history

---

# 🏗️ System Architecture

```
                    User
                      │
                      ▼
             Streamlit Frontend
                      │
                      ▼
               FastAPI Backend
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
 Product Retrieval Engine     Google Gemini
 (CSV + Vector Retrieval)         LLM
          │                       │
          └───────────┬───────────┘
                      ▼
           Intelligent Recommendation
```

---

# 🤖 AI Agent Workflow

The project follows an agent-based workflow:

### 🔹 User Interaction Agent
- Accepts user queries
- Maintains conversation history
- Sends requests to the backend

### 🔹 Retrieval Agent
- Searches the product catalogue
- Retrieves the most relevant products
- Provides context for recommendation generation

### 🔹 Recommendation Agent
- Uses Google Gemini
- Analyzes retrieved products
- Generates personalized recommendations

---

# 🔄 Retrieval-Augmented Generation (RAG)

Instead of asking the Large Language Model to answer directly, the application first retrieves relevant product information from the product catalogue.

The retrieved product information is then supplied as context to Gemini, enabling it to generate accurate and explainable recommendations.

### RAG Workflow

```
User Query
     │
     ▼
Retrieve Relevant Products
     │
     ▼
Provide Context to Gemini
     │
     ▼
Generate Recommendation
     │
     ▼
Display Response
```

---

# 🧠 Large Language Model (LLM)

**Google Gemini**

Gemini is responsible for:
- Understanding user intent
- Generating personalized recommendations
- Producing conversational responses
- Providing context-aware suggestions

---

# 🛠️ Technologies Used

### Frontend
- Streamlit

### Backend
- FastAPI
- Uvicorn

### AI & Machine Learning
- Google Gemini
- LangChain
- Retrieval-Augmented Generation (RAG)
- Sentence Transformers

### Data Processing
- Pandas

### Environment Management
- Python Virtual Environment
- Python Dotenv

### Version Control
- Git
- GitHub

---

# 📁 Project Structure

```text
smart-product-recommendation-assistant/
│
├── backend/
│   ├── main.py
│   ├── rag_pipeline.py
│   ├── recommender.py
│   ├── response_generator.py
│   ├── explanation_generator.py
│   ├── llm_extractor.py
│   ├── metadata_filter.py
│   ├── memory.py
│   ├── prompts.py
│   ├── models.py
│   ├── config.py
│   ├── list_models.py
│   ├── .env.example
│   └── .gitignore
│
├── data/
│   ├── ecommerce_products_killer.csv
│   ├── ingest.py
│   ├── config.py
│   ├── main.py
│   └── pyproject.toml
│
├── frontend/
│   ├── app.py
│   ├── components.py
│   └── styles.py
│
├── requirements.txt
│
└── README.md

---

# 👥 Team Members & Responsibilities

| Team Member        | Role                               |
| ------------------ | ---------------------------------- |
| **Aditi Pandey**   | RAG & Backend Engineer             |
| **Anshika Priya**  | System Integration & QA Lead       |
| **Arshpreet Kaur** | Data Engineer                      |
| **Gauri**          | Frontend & UI/UX Developer         |
| **Gurleen Kaur**   | Agentic Logic & Filtering Engineer |

---

# ✅ Testing

The application was tested for:

- Backend API functionality
- Frontend–backend integration
- AI recommendation generation
- Product retrieval accuracy
- Product filtering
- Cross-platform compatibility (Windows & macOS)

---

# 🚀 Future Scope

- User authentication
- Personalized recommendation history
- Wishlist and shopping cart
- Database integration (MongoDB/PostgreSQL)
- Voice-based shopping assistant
- Deployment on cloud platforms
- Multi-language support

---

# 🎯 Conclusion

The **Smart Product Recommendation Assistant** demonstrates how **Retrieval-Augmented Generation (RAG)** and **Large Language Models (Google Gemini)** can be combined to build an intelligent shopping assistant capable of understanding natural language queries and delivering relevant product recommendations. The project showcases the integration of modern AI technologies with a user-friendly web interface to enhance the online shopping experience.