import streamlit as st
import requests
import json
from typing import List, Dict, Any

st.set_page_config(
    page_title="TrademarkVista",
    page_icon="🔍",
    layout="wide"
)

# Constants
API_ENDPOINT = "http://127.0.0.1:5000/api/query" #for local hosting only

def query_trademark_api(question: str) -> Dict[str, Any]:
    """Send a natural language query to the TrademarkQA system"""
    try:
        response = requests.post(
            API_ENDPOINT,
            json={"question": question},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return {"error": str(e)}

def format_results(data: Dict[str, Any]) -> str:
    """Format the GraphQL results into readable text"""
    if "error" in data:
        return f"❌ Error: {data['error']}"
    
    # Handle search results
    if "searchMarks" in data:
        marks = data["searchMarks"]
        if not marks:
            return "No matching trademarks found."
        
        results = []
        for mark in marks:
            owners = mark.get("caseFileOwners", "Unknown Owner")
            status = mark.get("status", "Unknown Status")
            results.append(
                f"**{mark['markIdentification']}**\n"
                f"Serial #: {mark.get('serialNumber', 'N/A')}\n"
                f"Category: {mark.get('categoryCode', 'N/A')}\n"
                f"Owner: {owners}\n"
                f"Status: {status}"
            )
        return "\n\n".join(results)
    
    # Other query types can be added here
    return json.dumps(data, indent=2)

def main():
    st.title("🔍 TrademarkVista")
    st.subheader("Search USPTO Trademark Database using Natural Language")
    
    # Sidebar
    #st.sidebar.image("https://via.placeholder.com/150x150?text=TM", width=150)
    
    # Clear chat button
    if st.sidebar.button("🗑️ New Search", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.sidebar.markdown("### About")
    st.sidebar.markdown(
        "TrademarkVista allows you to query USPTO trademark data "
        "using natural language. Ask questions about trademarks, "
        "owners, categories, and more."
    )
    
    st.sidebar.markdown("### Example Questions")
    example_questions = [
        "Are there any trademarks with NTHLIFE?",
        "What trademarks are in class 40?",
    ]
    
    for question in example_questions:
        if st.sidebar.button(f"Try: {question[:30]}...", key=question):
            # Clear previous conversation when using examples
            st.session_state.messages = []
            st.session_state.messages.append({"role": "user", "content": question})
            query_and_display(question)
    
    #Chat input
    if prompt := st.chat_input("Ask about a trademark..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        query_and_display(prompt)

def query_and_display(question: str):
    """Query the API and display results in the chat interface"""
    with st.chat_message("assistant"):
        with st.spinner("Searching trademark database..."):
            response = query_trademark_api(question)
            formatted_response = format_results(response)
            st.markdown(formatted_response)
            
            # Add a "GraphQL Query" expander to show the underlying query
            if "searchMarks" in response and len(response["searchMarks"]) > 0:
                with st.expander("View Results as JSON"):
                    st.json(response)

if __name__ == "__main__":
    main()