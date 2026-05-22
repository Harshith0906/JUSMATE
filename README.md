# JUSMATE

AI-powered legal intelligence platform using RAG, embeddings, NLP, and semantic search.

![React](https://img.shields.io/badge/Frontend-React%20%2B%20TypeScript-blue?logo=react)
![Node.js](https://img.shields.io/badge/Backend-Node.js%20%2B%20Express-green?logo=node.js)
![Python](https://img.shields.io/badge/AI%20Engine-Python-yellow?logo=python)
![MySQL](https://img.shields.io/badge/Database-MySQL-orange?logo=mysql)
![RAG](https://img.shields.io/badge/AI-RAG%20%2B%20LLM-purple)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## Overview

JUSMATE is a legal-tech platform designed to help users retrieve and analyze legal information efficiently using Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs).

The system combines semantic search, embeddings, and AI-powered retrieval to provide intelligent legal assistance and clause-level contextual responses.

---

## ✨ Features

- 🤖 **AI Legal Chat Assistant** — Ask legal questions and get clause-level, context-aware answers powered by RAG + LLM
- 🔍 **Semantic Search** — Embedding-based retrieval finds the most relevant legal documents for any query
- 👤 **Citizen Dashboard** — Manage consultations, track case history, and interact with the AI assistant
- 🧑‍⚖️ **Lawyer Dashboard** — Lawyers can manage their profile, view client requests, and handle consultations
- 🔎 **Lawyer Discovery** — Citizens can search and filter lawyers by specialization
- 🔐 **Authentication & Authorization** — Secure login flows for both citizens and lawyers
- 📊 **Evaluation Pipeline** — Built-in response quality evaluation for the RAG system

---

## Application Screenshots

### Home Page

![Home Page](screenshots/homepage.png)

---

### AI Legal Chat Assistant

![Chatbot](screenshots/chatbot.png)

---

### Citizen Dashboard

![Citizen Dashboard](screenshots/citizen-dashboard.png)

---

### Lawyer Dashboard

![Lawyer Dashboard](screenshots/lawyer-dashboard.png)

---

### Lawyer Discovery Module

![Lawyer Discovery](screenshots/lawyer-discovery.png)

---

## System Architecture

![Architecture](screenshots/architecture.png)

### Architecture Explanation

JUSMATE follows a modular full-stack AI architecture designed for intelligent legal assistance and semantic legal information retrieval.

#### Frontend Layer
The frontend is built using React, TypeScript, and Tailwind CSS. It provides:
- User authentication
- Lawyer discovery
- Consultation management
- AI legal chat interface
- Dashboard analytics

#### Backend Layer
The backend is developed using Node.js and Express.js. It handles:
- REST API management
- Authentication and authorization
- User and lawyer management
- Consultation workflows
- Request routing between frontend and AI modules

#### AI / RAG Engine
The `ragNllm` module powers the intelligent legal retrieval system using:
- Retrieval-Augmented Generation (RAG)
- Embedding-based semantic search
- Context-aware legal response generation
- Legal document retrieval and ranking

#### Data Flow
1. User submits a legal query through the frontend.
2. Backend APIs process and validate the request.
3. Query is forwarded to the RAG engine.
4. Relevant legal documents and clauses are retrieved using embeddings.
5. Retrieved context is passed to the LLM.
6. AI-generated legal response is returned to the frontend.

#### Key Advantages
- Context-aware legal assistance
- Faster legal information retrieval
- Modular scalable architecture
- AI-enhanced semantic understanding
- Separation of frontend, backend, and AI services

---

## Tech Stack

### Frontend
- React.js
- TypeScript
- Tailwind CSS
- Vite

### Backend
- Node.js
- Express.js
- MySql

### AI / ML
- Python
- RAG Pipeline
- NLP
- Embeddings
- LLM Integration

---

## Project Structure

```text
backend/   -> Backend APIs and server logic
frontend/  -> Frontend application
ragNllm/   -> RAG pipeline, retrieval, evaluation, embeddings
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Harshith0906/JUSMATE.git
cd JUSMATE
```

### Backend Setup

```bash
cd backend
npm install
npm run dev
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Python Environment

```bash
cd ragNllm
pip install -r requirements.txt
```

---

## Future Improvements

- Legal document summarization
- Multi-language support
- Fine-tuned legal LLM
- Risk analysis engine
- AI legal chatbot

---

## Author

Chakinala Harshith Patel
