from duckduckgo_search import DDGS

def web_search_tool(query: str) -> str:
    """Yeh tool internet se live university ka data search karke lata hai."""
    try:
        with DDGS() as ddgs:
            # University of Sahiwal ke sath query ko merge karke top 3 results nikalna
            search_query = f"University of Sahiwal {query}"
            results = ddgs.text(search_query, max_results=3)
            
            if not results:
                return "No recent web search results found."
                
            # Saare results ko ek paragraph mein jorh dena
            context_list = []
            for r in results:
                context_list.append(f"Title: {r['title']}\nSnippet: {r['body']}\n")
            
            return "\n---\n".join(context_list)
    except Exception as e:
        return f"Web search failed due to: {str(e)}"