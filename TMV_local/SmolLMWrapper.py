from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import re

class SmolLMWrapper:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM2-135M-Instruct")
        self.model = AutoModelForCausalLM.from_pretrained("HuggingFaceTB/SmolLM2-135M-Instruct")
        
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=50,     # Short responses only
            temperature=0.1,       # Very focused responses
            do_sample=False        # Deterministic output
        )
        print("Loaded pipeline")
        
        self.llm = HuggingFacePipeline(pipeline=self.pipe)
        print("Loaded LLM")
        
        self.query_templates = {
            "search": (
                "query { \n"
                "    searchMarks(keyword: \"%s\") { \n"
                "        id\n"
                "        markIdentification\n"
                "        serialNumber\n"
                "        categoryCode\n"
                "        status\n"
                "        caseFileOwners\n"
                "    } \n"
                "}"
            ),
            "category": (
                "query { \n"
                "    trademarksByCategory(category_code: \"%s\") { \n"
                "        id\n"
                "        markIdentification\n"
                "        serialNumber\n"
                "        categoryCode\n"
                "        status\n"
                "        caseFileOwners\n"
                "    } \n"
                "}"
            )
        }

    def _extract_trademark_name(self, question: str) -> str:
        """
        Extracts the trademark name from the question.
        First, try regex patterns (for cases like "with NTHLIFE", "mark NTHLIFE", etc.).
        If no match is found, fall back to the LLM extraction.
        Returns the trademark in uppercase.
        """
        # Try several regex patterns to capture a likely trademark term.
        patterns = [
            r'with\s+([A-Z0-9]+)',         # e.g., "with NTHLIFE"
            r'mark(?:ed|)?\s+([A-Z0-9]+)',   # e.g., "mark NTHLIFE" or "marked NTHLIFE"
            r'trademark(?:\s+name)?\s+([A-Z0-9]+)'  # e.g., "trademark NTHLIFE"
        ]
        for pattern in patterns:
            match = re.search(pattern, question, re.IGNORECASE)
            if match:
                trademark = match.group(1).upper()
                # Additional check: if it’s a short word, we might not want it.
                if len(trademark) >= 2:
                    return trademark

        # Fallback: use LLM extraction.
        prompt = (
            f"Extract ONLY the trademark name from this question. "
            f"Return just the name in capital letters.\n"
            f"Question: {question}\nTrademark:"
        )
        response = self.llm(prompt).strip()
        
        # Cleanup the response
        response = re.sub(r'["\']', '', response)  # Remove any quotes
        response = re.sub(r'trademark:\s*', '', response, flags=re.IGNORECASE)
        response = ' '.join(response.split())
        return response.upper()

    def _extract_category(self, question: str) -> str:
        """
        Extracts the category or class number from the question.
        Supports phrases like "category 40" or "class 40".
        """
        match = re.search(r'(?:category|class)\s*(\d+)', question, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    def get_graphql_query(self, user_question: str) -> str:
        """
        Generates a GraphQL query based on the user's natural language question.
        If a category/class number is provided, it includes it in the query.
        Otherwise, it creates a simple trademark search query.
        """
        # Extract trademark name
        trademark = self._extract_trademark_name(user_question)
        print("Extracted trademark:", trademark)
        if not trademark:
            raise ValueError("Could not extract a valid trademark name from the question")
        
        # Extract category (if any)
        category = self._extract_category(user_question)
        print("Extracted category:", category)
        
        if category:
            # Generate query including both trademark and category filtering.
            return (
                "query {\n"
                f"    searchMarks(keyword: \"{trademark}\", category_code: \"{category}\") {{\n"
                "        id\n"
                "        markIdentification\n"
                "        serialNumber\n"
                "        categoryCode\n"
                "        status\n"
                "        caseFileOwners\n"
                "    }\n"
                "}}"
            )
        else:
            # Generate trademark-only search query.
            return self.query_templates["search"] % trademark