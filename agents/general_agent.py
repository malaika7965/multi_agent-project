from agents.base_agent import BaseAgent

class GeneralAgent(BaseAgent):
    def handle_chat(self, query: str) -> str:
        system_prompt = (
            "You are a friendly and professional AI Help Desk agent for University of Sahiwal. "
            "Do NOT use repetitive greetings like Assalam-o-Alaikum again and again. "
            "Respond directly, politely, and professionally to the user's input."
        )
        messages = [("system", system_prompt), ("human", query)]
        response = self.llm.invoke(messages)
        return response.content