# TrademarkVista
This project aims to create a **free, publicly accessible** platform to query and explore U.S. Patent and Trademark Office (USPTO) trademark data. It combines **data parsing**, a **relational database**, **GraphQL APIs**, and **large language models (LLMs)** to allow natural language queries and structured responses about trademarks. Test it out [here](Link to be added).

## Table of Contents
- [Project Objectives](#project-objectives)  
- [High-Level Architecture](#high-level-architecture)  
- [Technical Tools & Components](#technical-tools--components)  
- [Implementation Details](#implementation-details)  
  - [Part 1: Data Parsing and PostgreSQL Setup](#part-1-data-parsing-and-postgresql-setup)  
  - [Part 2: Simple QA UI](#part-2-simple-qa-ui)  
  - [Part-3: GraphQL API with Flask and Graphene](#part-3-graphql-api-with-flask-and-graphene)  
  - [Part-4: Natural Language Query Processing with an LLM](#part-4-natural-language-query-processing-with-an-llm)  
  - [Part-5: Conversational Workflow with LangChain](#part-5-conversational-workflow-with-langchain)  
  - [Part-6: Hosting the Project](#part-6-hosting-the-project)  
- [Future Enhancements](#future-enhancements)  

---
## Project Objectives
1. **Automate Data Ingestion**: Parse 1000+ USPTO trademark XML files to extract key information (e.g., mark name, ID, date, owner name, classes).
2. **Create a Queryable Database**: Store the parsed data in a PostgreSQL database to efficiently handle queries.
3. **Natural Language QA**: Provide a simple QA interface where users can ask questions in natural language (e.g., “Is there a trademark with the phrase ‘DreamSpark’ in Class 42?”).
4. **GraphQL API**: Expose the data through a GraphQL API built with Flask and Graphene, enabling structured data retrieval.
5. **Intelligent Query Conversion**: Leverage an LLM to interpret human language questions and convert them into valid GraphQL queries.
6. **Conversational Experience with LangChain**: Handle multi-turn conversations and retrieval pipelines using LangChain.

---

## High-Level Architecture
```
                        +----------------------------+
                        |      User/Client UI       |
                        +-------------+--------------+
                                      |
                                      | Natural Language Questions
                                      v
                         +---------------------------+
                         | LLM (e.g., LLaMA) +       |
                         |   LangChain Pipeline      |
                         +------------+--------------+
                                      | Converted GraphQL Queries
                                      v
                        +----------------------------+
                        | Flask + Graphene GraphQL   |
                        +-------------+--------------+
                                      | 
                                      | DB Queries (SQL)
                                      v
                         +--------------------------+
                         |  PostgreSQL USPTO DB     |
                         +--------------------------+
```

---

## Technical Tools & Components

1. **Data Parsing**
   - **XML Parsing**: Libraries such as `lxml` or `xml.etree.ElementTree`.
   - **Batch Processing**: Methods for iterating over multiple XML files.

2. **Relational Database**
   - **PostgreSQL**: A robust open-source RDBMS to store trademark data.

3. **Backend Framework**
   - **Flask**: A lightweight Python web framework to serve the GraphQL API.

4. **GraphQL**
   - **Graphene**: A Python library to build GraphQL schemas and handle requests.

5. **LLM for Natural Language Processing**
   - **LLaMA** or **SmolLM** for interpreting user questions.

6. **LangChain**
   - Orchestrates the conversation flow, context management, and retrieval of relevant data.
---

## Implementation Details

### Part 1: Data Parsing and PostgreSQL Setup
1. **XML File Collection**: Obtain 10000+ USPTO XML files. Each file contains trademark data such as:
   - Trademark phrase or mark.
   - Trademark ID / Registration Number.
   - Owner name.
   - Filing/registration date.
   - Trademark class(es).
   - Status (live, abandoned, etc.).

2. **Parsing Strategy**:
   - Use Python libraries for XML parsing to read each file.
   - Extract the fields of interest (mark name, ID, class, etc.).

3. **Database Schema Design**:
   - Define tables (e.g., `trademarks`, `owners`, `classes`).
   - Establish relationships (one trademark can have multiple classes, etc.).

4. **Database Ingestion**:
   - Connect to PostgreSQL.
   - Insert parsed records into the tables.
   - Handle duplicates and data validation (e.g., unique constraints on trademark IDs).

### Part 2: Simple QA UI
1. **Objective**:
   - Offers a minimal web-based or command-line interface for end-users.
   - Let users type in questions like:
     - *“Is there a trademark with the phrase ‘DreamSpark’ in Class 42?”*
     - *“Show me all marks from ‘XYZ Corp’ that are currently live and in Class 25.”*

2. **Basic Components**:
   - A text input field where the user can type queries in natural language.
   - A button to submit the query.
   - A display area or console to show the response (structured data such as a table of results).

3. **Interaction Flow**:
   - User inputs a query.
   - The query is sent to the LLM pipeline (Part 4).
   - The UI displays the results fetched by the GraphQL query (Part 3).

### Part-3: GraphQL API with Flask and Graphene
1. **Project Structure**:
   - A **Flask** app that sets up the server.
   - A **Graphene** schema describing the data types (`Trademark`, `Owner`, etc.) and the queries.

2. **Schema Definition**:
   - Example queries might include:
     - `allTrademarks` (return a list of trademarks).
     - `trademarkByOwner(ownerName: String!)`.
     - `trademarksByClass(classNumber: Int!)`.
   - Resolvers map GraphQL queries to database queries.

### Part-4: Natural Language Query Processing with an LLM
1. **Goal**:
   - Convert free-form user questions into structured GraphQL queries.

2. **Model Setup**:
   - Provide the model with a prompt or instructions on how to interpret user queries.
   - The user’s question is fed into the LLM along with context about the GraphQL schema and examples.
   - The LLM outputs a string representing a valid GraphQL query (including filters and fields).
   - Check for correctness. If the query is invalid, handle errors gracefully.

### Part-5: Conversational Workflow with LangChain
1. **Pipeline Orchestration**:
   - Use LangChain to manage the conversation state, memory, and chaining of prompts.
   - For multi-turn interactions, maintain context of previous user questions and partial results.

2. **Retrieval and Tools**:
   - LangChain can integrate with various “tools”:
     - A “database query” tool (backed by the GraphQL endpoint).
     - A “summarization” or “reasoning” tool if needed.

3. **User Experience**:
   - Users can refine or clarify queries (“Actually, show me only the live ones”).
   - LangChain re-prompts the LLM to update or refine the GraphQL query accordingly.

### Part-6: Hosting the Project
1. **Containerization (Optional)**:
   - Containerize the app (Flask + GraphQL + LLM) using Docker.

2. **Hosting Platforms**:
   - **Render**: Similar free-tier approach for hosting web services and Postgres.

---

## Future Enhancements
1. **Advanced Search**:
   - Implement fuzzy search or advanced filtering on the GraphQL layer.
2. **LLM Fine-Tuning**:
   - Enhance the LLM with training data specific to USPTO queries for more accurate GraphQL generation.
3. **Analytics Dashboard**:
   - Visualize trademark trends, popular classes, or top owners in real-time.
