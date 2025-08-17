import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

# run command : streamlit run langchain-basic/app.py

# Load environment variables
load_dotenv()

st.set_page_config(page_title="LangChain Chatbot with Groq", page_icon="🤖")

st.title("LangChain Chat with Groq")
st.markdown("Learn LangChain basics with Groq's ultra-fast inference!")

# Get API key from environment variable
api_key = os.getenv("GROQ_API_KEY")

# Sidebar: Settings and chat history
with st.sidebar:
    st.header("Settings")
    
    # Show API key status instead of input field
    if api_key:
        st.success("✅ API Key Loaded")
        st.info("API key is securely loaded from environment variables")
    else:
        st.error("❌ API Key Not Found")
        st.markdown("""
        **To use this app, you need to:**
        
        1. Create a `.env` file in the project root
        2. Add: `GROQ_API_KEY=your_actual_api_key_here`
        3. Get your free API key at [console.groq.com](https://console.groq.com)
        
        **Or set as environment variable:**
        ```bash
        export GROQ_API_KEY=your_actual_api_key_here
        ```
        """)
    
    model_name = st.selectbox(
        "Model",
        ["llama3-8b-8192", "gemma2-9b-it"],
        index=0
    )
    
    # Chat management
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear Chat", help="Clear current conversation"):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("Save Chat", help="Save current conversation"):
            if st.session_state.messages:
                # Generate a timestamp for the conversation
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                conversation_name = f"Chat_{timestamp}"
                
                # Save to session state (in a real app, you'd save to a database or file)
                if "saved_conversations" not in st.session_state:
                    st.session_state.saved_conversations = {}
                st.session_state.saved_conversations[conversation_name] = st.session_state.messages.copy()
                st.success(f"Chat saved as '{conversation_name}'")
                st.rerun()
    
    st.markdown("---")
    
    # Enhanced Chat History Section
    st.subheader("📚 Chat History")
    
    # Search functionality
    if "messages" in st.session_state and st.session_state.messages:
        search_term = st.text_input("🔍 Search in chat", placeholder="Search messages...")
        
        # Filter messages based on search
        filtered_messages = st.session_state.messages
        if search_term:
            filtered_messages = [
                msg for msg in st.session_state.messages 
                if search_term.lower() in msg["content"].lower()
            ]
        
        # Display filtered messages with better formatting
        if filtered_messages:
            st.markdown(f"**Found {len(filtered_messages)} messages**")
            
            # Group messages by conversation turns
            for i in range(0, len(filtered_messages), 2):
                if i < len(filtered_messages):
                    # User message
                    user_msg = filtered_messages[i]
                    st.markdown(f"**🧑 User:**")
                    st.markdown(f"<div style='background-color: black; padding: 8px; border-radius: 5px; margin: 5px 0; font-size: 0.9em;'>{user_msg['content'][:100]}{'...' if len(user_msg['content']) > 100 else ''}</div>", unsafe_allow_html=True)
                    
                    # Assistant message (if exists)
                    if i + 1 < len(filtered_messages):
                        assistant_msg = filtered_messages[i + 1]
                        st.markdown(f"**🤖 Assistant:**")
                        st.markdown(f"<div style='background-color:black ; padding: 8px; border-radius: 5px; margin: 5px 0; font-size: 0.9em;'>{assistant_msg['content'][:100]}{'...' if len(assistant_msg['content']) > 100 else ''}</div>", unsafe_allow_html=True)
                    
                    st.markdown("---")
        else:
            st.info("No messages found matching your search.")
    else:
        st.info("No chat history yet.")
    
    # Saved Conversations Section
    if "saved_conversations" in st.session_state and st.session_state.saved_conversations:
        st.markdown("---")
        st.subheader("💾 Saved Conversations")
        
        for conv_name, conv_messages in st.session_state.saved_conversations.items():
            with st.expander(f"📁 {conv_name} ({len(conv_messages)} messages)"):
                st.markdown(f"**Messages:** {len(conv_messages)}")
                st.markdown(f"**Last updated:** {conv_name.split('_')[1] if '_' in conv_name else 'Unknown'}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Load {conv_name[:10]}...", key=f"load_{conv_name}"):
                        st.session_state.messages = conv_messages.copy()
                        st.rerun()
                with col2:
                    if st.button(f"Delete", key=f"delete_{conv_name}"):
                        del st.session_state.saved_conversations[conv_name]
                        st.rerun()
    
    # Statistics
    if "messages" in st.session_state and st.session_state.messages:
        st.markdown("---")
        st.subheader("📊 Statistics")
        total_messages = len(st.session_state.messages)
        user_messages = len([msg for msg in st.session_state.messages if msg["role"] == "user"])
        assistant_messages = len([msg for msg in st.session_state.messages if msg["role"] == "assistant"])
        
        st.metric("Total Messages", total_messages)
        st.metric("User Messages", user_messages)
        st.metric("Assistant Messages", assistant_messages)
        
        # Calculate average response length
        if assistant_messages > 0:
            avg_length = sum(len(msg["content"]) for msg in st.session_state.messages if msg["role"] == "assistant") / assistant_messages
            st.metric("Avg Response Length", f"{avg_length:.0f} chars")

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

if not api_key:
    st.error("❌ API Key Required")
    st.markdown("""
    **Please set up your GROQ API key to start chatting:**
    
    1. **Create a `.env` file** in your project root directory
    2. **Add this line:** `GROQ_API_KEY=your_actual_api_key_here`
    3. **Get your free API key** at [console.groq.com](https://console.groq.com)
    4. **Restart the Streamlit app**
    
    **Alternative:** Set as environment variable before running:
    ```bash
    export GROQ_API_KEY=your_actual_api_key_here
    streamlit run app.py
    ```
    """)
elif not chain:
    st.error("❌ Failed to initialize chat model")
    st.info("Please check your API key and try again")
else:
    # Main area: Only show the latest chat
    if st.session_state.messages:
        last_msg = st.session_state.messages[-1]
        with st.chat_message(last_msg["role"]):
            st.write(last_msg["content"])

    # Chat input
    question = st.chat_input("Ask me anything")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                for chunk in chain.stream({"question": question}):
                    full_response += chunk
                    message_placeholder.markdown(full_response)
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
st.markdown("Built with LangChain & Groq | Experience the speed! 🚀")