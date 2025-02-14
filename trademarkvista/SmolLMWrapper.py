from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

class SmolLMWrapper:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM2-135M-Instruct")
        self.model = AutoModelForCausalLM.from_pretrained("HuggingFaceTB/SmolLM2-135M-Instruct")
        print("Loaded model and tokenizer")
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=512,
            temperature=0.7
        )
        print("Loaded pipeline")
        self.llm = HuggingFacePipeline(pipeline=self.pipe)
        print("Loaded LLM")
        self.query_templates = {
            "search": """
            query {
                searchMarks(keyword: "%s") {
                    mark_identification
                    serial_number
                    category_code
                    status
                    case_file_owners
                }
            }""",
            "category": """
            query {
                trademarksByCategory(category_code: "%s") {
                    mark_identification
                    serial_number
                    status
                    case_file_owners
                }
            }""",
            "serial": """
            query {
                trademarkBySerial(serial_number: "%s") {
                    mark_identification
                    category_code
                    status
                    case_file_owners
                }
            }"""
        }

    def get_graphql_query(self, user_question: str) -> str:
        # First, determine query type using LLM
        type_prompt = f"""What type of trademark search is this question asking for? Reply with only one word:
        'search' for keyword search
        'category' for category search
        'serial' for serial number search
        
        Question: {user_question}"""
        print('get_graphql_query-> User question:', user_question)
        query_type = self.llm(type_prompt).strip().lower()
        print("Query type:", query_type)

        print('~'*50)
        # Then extract the search parameter
        param_prompt = f"""Extract only the search parameter from this question:
        Question: {user_question}"""
        
        search_param = self.llm(param_prompt).strip()
        print("Search parameter:", search_param)
        # Format the appropriate template
        if query_type in self.query_templates:
            return self.query_templates[query_type] % search_param
        else:
            # Fallback to search
            return self.query_templates["search"] % search_param