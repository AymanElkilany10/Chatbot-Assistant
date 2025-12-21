from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage
from tools import search_cpp_tutorial


load_dotenv()


llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)

system_prompt = """
You are a smart assistant specialized in C++ programming concepts.
- Always respond in clear, polite English.
- For general greetings (hello, hi, how are you), reply directly without using any tools.
- For questions about C++ programming (variables, data types, loops, conditionals, functions, arrays, structs, basic syntax, etc.), use the search tool to retrieve information first.
- Base your answer only on the retrieved information from the C++ tutorial PDF.
- If no relevant information is found, say: "I couldn't find specific information about that in the C++ tutorial."
- Never make up information.
"""



app = create_react_agent(llm, tools=[search_cpp_tutorial])

class CppTutorialAgent:
    def __init__(self):
        self.history = []

    def invoke(self, user_input):
        messages = [SystemMessage(content=system_prompt)]
        

        messages += self.history
        
        messages += [HumanMessage(content=user_input)]
        
        response = app.invoke({"messages": messages})
        
        answer = response["messages"][-1].content
        
        self.history += [HumanMessage(content=user_input), response["messages"][-1]]
        
        if len(self.history) > 20:
            self.history = self.history[-20:]
        
        return {"output": answer}

agent_executor = CppTutorialAgent()
