from langchain_community.llms import Ollama
from src.tools import query_expenses, query_financial_documents

class FinanceAgent:
    def __init__(self):
        # We use qwen2.5:7b for local processing. 
        # Temperature = 0 enforces strict logical accuracy over creativity.
        self.llm = Ollama(model="qwen2.5:7b", temperature=0)
        
    def ask(self, user_prompt: str) -> str:
        data_context = ""
        prompt_lower = user_prompt.lower()
        
        # --- INTELLIGENT ROUTER ---
        
        # 1. Route to CSV if keywords indicate spreadsheet analysis
        needs_csv = any(word in prompt_lower for word in ["spend", "transaction", "cost", "csv", "amount", "buy", "purchase", "ledger", "total"])
        if needs_csv:
            data_context += query_expenses(user_prompt) + "\n\n"
            
        # 2. Route to PDF RAG if keywords indicate document lookup
        needs_pdf = any(word in prompt_lower for word in ["pdf", "lease", "contract", "statement", "agreement", "policy", "rule", "terms", "document", "tax", "w2"])
        if needs_pdf:
            data_context += query_financial_documents(user_prompt) + "\n\n"
            
        # 3. If it's a general greeting or non-data question, let them know what tools are armed
        if not needs_csv and not needs_pdf:
            data_context = "No local database search was triggered. Provide general assistance based on default memory."

        # --- SYSTEM PROMPT ---
        system_prompt = (
            "You are a private, local AI Personal Finance Assistant.\n"
            "You have secure local access to the user's transaction spreadsheet (CSV) and financial contracts (PDFs).\n\n"
            "=== LOCAL DATA CONTEXT ENVIRONMENT ===\n"
            f"{data_context}\n"
            "=======================================\n\n"
            "Strict Operating Rules:\n"
            "1. Answer the user's query using ONLY the verified facts from the 'Local Data Context Environment' above.\n"
            "2. If the user asks about calculations (total spending, count of items, averages), calculate it accurately yourself using the numbers provided in the context.\n"
            "3. If a file is missing or a warning is shown in the context, guide the user on how to add/upload their files.\n"
            "4. NEVER hallucinate, make up numbers, or guess details not mentioned in the context.\n"
            "5. Maintain a professional, constructive, and helpful tone.\n"
        )
        
        # Combine system guidelines and execute
        prompt = f"{system_prompt}\nUser Question: {user_prompt}\nAssistant Answer:"
        return self.llm.invoke(prompt)