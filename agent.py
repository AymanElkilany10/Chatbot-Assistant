# agent.py

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage
from tools import search_cpp_tutorial


load_dotenv()

# LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)

# System prompt
system_prompt = """
You are a smart assistant specialized in C++ programming concepts.
- Always respond in clear, polite English.
- For general greetings (hello, hi, how are you), reply directly without using any tools.
- For questions about C++ programming (variables, data types, loops, conditionals, functions, arrays, structs, basic syntax, etc.), use the search tool to retrieve information first.
- Base your answer only on the retrieved information from the C++ tutorial PDF.
- If no relevant information is found, say: "I couldn't find specific information about that in the C++ tutorial."
- Never make up information.
"""


# إنشاء الـ ReAct Agent
app = create_react_agent(llm, tools=[search_cpp_tutorial])

# دالة لتشغيل الـ agent مع الـ system prompt والذاكرة يدوياً
class CppTutorialAgent:
    def __init__(self):
        self.history = []

    def invoke(self, user_input):
        # إضافة الـ system prompt في البداية (مرة واحدة)
        messages = [SystemMessage(content=system_prompt)]
        
        # إضافة التاريخ
        messages += self.history
        
        # إضافة الرسالة الجديدة
        messages += [HumanMessage(content=user_input)]
        
        # استدعاء الـ agent
        response = app.invoke({"messages": messages})
        
        # استخراج الرد النهائي
        answer = response["messages"][-1].content
        
        # تحديث التاريخ
        self.history += [HumanMessage(content=user_input), response["messages"][-1]]
        
        # الحفاظ على الحجم معقولاً (آخر 20 رسالة فقط)
        if len(self.history) > 20:
            self.history = self.history[-20:]
        
        return {"output": answer}

# إنشاء الـ agent الجاهز للاستخدام في app.py
agent_executor = CppTutorialAgent()
