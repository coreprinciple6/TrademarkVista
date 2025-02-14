from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import graphene

class TrademarkQA:
    def __init__(self, llm_wrapper, schema):
        self.llm = llm_wrapper
        self.schema = schema
        # self.memory = ConversationBufferMemory(
        #     memory_key="chat_history",
        #     return_messages=True
        # )
    
    def process_query(self, user_question: str):
        try:
            # Generate GraphQL query
            print('process_query-> User question:', user_question)
            graphql_query = self.llm.get_graphql_query(user_question)
            print('Generated GraphQL query:', graphql_query)
            
            # Execute using your existing schema
            result = self.schema.execute(graphql_query)
            
            if result.errors:
                return {"error": str(result.errors[0])}
            
            # # Update conversation memory
            # self.memory.chat_memory.add_user_message(user_question)
            # self.memory.chat_memory.add_ai_message(str(result.data))
            
            return result.data
            
        except Exception as e:
            return {"error": str(e)}

    def get_chat_history(self):
        return self.memory.chat_memory.messages