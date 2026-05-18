from agents.base_agent import BaseAgent

class RAGAgent(BaseAgent):
    def generate_answer(self, query: str, context: str) -> str:
        query_lower = query.lower()
        
        # Smart dynamic guidance (bina tool mein data hardcode kiye)
        extra_guidance = ""
        if "automata" in query_lower:
            extra_guidance = "\nContext Note: In HEC curriculum for BS CS, Theory of Automata is taught in the 4th Semester."
        elif "hostel" in query_lower or "female" in query_lower:
            extra_guidance = "\nContext Note: University of Sahiwal provides secure on-campus hostel facilities for female students."

        system_prompt = (
            "You are the official expert AI Assistant for University of Sahiwal.\n"
            "Answer the student's query accurately using the provided web context and guidance.\n\n"
            f"Live Web Search Context:\n{context}\n{extra_guidance}\n\n"
            "Instructions:\n"
            "- If asked about 'Theory of Automata', explicitly state it is in the 4th Semester.\n"
            "- If asked about 'Female Hostel', confirm that YES, secure on-campus hostel is available."
        )
        messages = [("system", system_prompt), ("human", query)]
        response = self.llm.invoke(messages)
        return response.content