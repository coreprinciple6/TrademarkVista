# TrademarkVista
This project aims to create a **free, publicly accessible** platform to query and explore U.S. Patent and Trademark Office (USPTO) trademark data. It combines **data parsing**, a **relational database**, **GraphQL APIs**, and **large language models (LLMs)** to allow natural language queries and structured responses about trademarks.
## Table of Contents
- [Project Objectives](#project-objectives)
- [High-Level Architecture](#high-level-architecture)  
- [Technical Tools & Components](#technical-tools--components)  
- [Implementation Details](#implementation-details)  
  - [Part 1: Data Parsing and PostgreSQL Setup](#part-1-data-parsing-and-postgresql-setup) :white_check_mark:
  - [Part 2: Simple QA UI](#part-2-simple-qa-ui) :hourglass_flowing_sand:
  - [Part-3: GraphQL API with Flask and Graphene](#part-3-graphql-api-with-flask-and-graphene) :white_check_mark: 
  - [Part-4: Natural Language Query Processing with an LLM](#part-4-natural-language-query-processing-with-an-llm) :hourglass_flowing_sand: 
  - [Part-5: Conversational Workflow with LangChain](#part-5-conversational-workflow-with-langchain) :white_check_mark: 
  - [Part-6: Hosting the Project](#part-6-hosting-the-project) :white_check_mark:
- [Future Enhancements](#future-enhancements)
- [Local Deployment](#local-deployment)
- [Latest Updates](#latest-updates)


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
   - **Streamlit**: For a simple web interface

4. **GraphQL**
   - **Graphene**: A Python library to build GraphQL schemas and handle requests.

5. **LLM for Natural Language Processing**
   -  **SmolLM 135m** for interpreting user questions.

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
   - Offers a minimal web-based or command-line interface for end-users using streamlit
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
   - advanced resolvers to handle complex queries

### Part-4: Natural Language Query Processing with an LLM
1. **Goal**:
   - Convert free-form user questions into structured GraphQL queries.

2. **Model Setup**:
   - Provide the model with a prompt or instructions on how to interpret user queries.
   - advanced prompt engineering to handle complex queries with filtering
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

1. **Hosting Platforms**:
   - **Render**: Similar free-tier approach for hosting web services and Postgres.
   - Direct GraphQL to final output is done :white_check_mark: and its availabe [here](https://trademarkvista.onrender.com/graphql?query=%7B%0A%20%20searchMarks(keyword:%20%22NTHLIFE%22)%20%7B%0A%20%20%20%20id%0A%20%20%20%20categoryCode%0A%20%20%20%20markIdentification%20%20%0A%20%20%20%20serialNumber%0A%20%20%20%20caseFileOwners%0A%20%20%20%20status%0A%20%20%20%20xmlFilename%0A%20%20%7D%0A%7D)
<img width="618" alt="image" src="https://github.com/user-attachments/assets/f73e5b93-982c-4200-a022-3319225f3d28" />
---

## Future Enhancements
1. **Advanced Search**:
   - Implement fuzzy search or advanced filtering on the GraphQL layer.
2. **LLM Fine-Tuning**:
   - Enhance the LLM with training data specific to USPTO queries for more accurate GraphQL generation.
3. **Analytics Dashboard**:
   - Visualize trademark trends, popular classes, or top owners in real-time.
--- 
## Local Deployment
- Make sure you have the postgres database locally (demo db included in repo)
- Run 'TMV_local/flask_app.py'
- Run 'streamlit run TMV_local/streamlit_app.py'
<img width="698" alt="image" src="https://github.com/user-attachments/assets/ffda2880-87d3-4962-a5d7-b274b5df9677" />

---
## Latest Updates
- Testing with natural language endpoint (without UI) can be done by running the folowing command
  ```
  Link_to_site = ''
  !curl -X POST f'{Link_to_site}/api/query \
     -H "Content-Type: application/json" \
     -d '{"question": "Find trademarks with NTHLIFE in category 40"}'
  ```
  <img width="591" alt="image" src="https://github.com/user-attachments/assets/c7fdf825-cc51-44ec-bb28-5c1fc4eaa730" />

- Testing with a small subset of dataset for storage restrictions
- prompt engineering for handling advanced filtering
- advanced resolvers to handle complex queries

