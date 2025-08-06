import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os

st.set_page_config(page_title="Chat with Groq", page_icon="🤖")

st.title("Chat with Groq")
st.markdown("Learn LangChain basics with Groq's ultra-fast inference!")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("GROQ API Key", type="password", help="GET Free API Key at console.groq.com")
    model_name = st.selectbox(
        "Model",
        ["llama3-8b-8192", "gemma2-9b-it"],
        index=0
    )
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

@st.cache_resource
def get_chain(api_key, model_name):
    if not api_key:
        return None
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name=model_name,
        temperature=0.7,
        streaming=True
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant powered by Groq. Answer questions clearly and concisely."),
        ("user", "{question}")
    ])
    chain = prompt | llm | StrOutputParser()
    return chain

chain = get_chain(api_key, model_name)

if not chain:
    st.warning("Please enter your Groq API key in the sidebar to start chatting!")
    st.markdown("[Get your free API key here](https://console.groq.com)")
else:
    # Display the chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    question = st.chat_input("Ask me anything")
    if question:
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)
        # Generate response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                # Stream response from Groq
                for chunk in chain.stream({"question": question}):
                    full_response += chunk
                    message_placeholder.markdown(full_response)
                # Add to history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown("### Try these examples:")
col1, col2 = st.columns(2)
with col1:
    st.markdown("- What is LangChain?")
    st.markdown("- Explain Groq's LPU technology")
with col2:
    st.markdown("- How do I learn programming?")
    st.markdown("- Write a haiku about AI")

st.markdown("---")
st.markdown("Built with LangChain & Groq")