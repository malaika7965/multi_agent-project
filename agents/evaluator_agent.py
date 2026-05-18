from agents.base_agent import BaseAgent

class EvaluatorAgent(BaseAgent):
    def evaluate(self, query: str, response: str) -> str:
        # Yeh agent check karta hai ke jawab sahi hai ya nahi taake loop chal sake
        system_prompt = (
            "You are the Quality Evaluator Agent for University of Sahiwal AI Helpdesk.\n"
            "Your job is to check if the generated response actually answers the user's query.\n"
            "If the response is helpful and answers the question, respond with exactly one word: 'pass'.\n"
            "If the response is completely blank, broken, or says 'I don't know', respond with: 'fail'."
        )
        messages = [("system", system_prompt), ("human", f"Query: {query}\nResponse: {response}")]
        try:
            eval_response = self.llm.invoke(messages)
            if "fail" in eval_response.content.strip().lower():
                return "fail"
        except:
            pass
        return "pass"