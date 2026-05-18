from agents.base_agent import BaseAgent

class RouterAgent(BaseAgent):
    def classify(self, query: str) -> str:
        query_lower = query.lower()
        # Direct strict keywords route
        if any(keyword in query_lower for keyword in ["vc", "vice chancellor", "chancellor", "location", "admission", "course", "fee", "sahiwal", "subject", "automata", "hostel", "female"]):
            return "university_info"

        system_prompt = (
            "Classify the user query into one of these two categories:\n"
            "1. 'university_info' (If asking about university, VC, admissions, courses, subjects, automata, or hostel)\n"
            "2. 'general_chat' (If saying hi, hello, how are you, or general talk)\n"
            "Respond with ONLY one word: either 'university_info' or 'general_chat'."
        )
        messages = [("system", system_prompt), ("human", query)]
        try:
            response = self.llm.invoke(messages)
            if "university_info" in response.content.strip().lower():
                return "university_info"
        except:
            pass
        return "general_chat"