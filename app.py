import streamlit as st
from agent import agent_executor

st.set_page_config(page_title="C++ Tutorial Assistant", page_icon="💻")
st.title("💻 C++ Smart Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about C++ programming..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = agent_executor.invoke(prompt)
            answer = response["output"]
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

with st.sidebar:
    st.header("Agent Thought Process")
    st.caption("Check your terminal for detailed ReAct steps (verbose mode)")
    st.write("To see full reasoning:")
    st.code("Run: streamlit run app.py")
    st.write("Look at the terminal output for Thought → Action → Observation → Answer")
