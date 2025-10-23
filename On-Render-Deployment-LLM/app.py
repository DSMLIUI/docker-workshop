import streamlit as st
from groq import Groq
import time
import os

if "GROQ_API_KEY" not in os.environ:
    st.error(
        "GROQ_API_KEY environment variable not set! Please set it in your environment or secrets."
    )
    st.info(
        "You can get a free API key from https://console.groq.com/"
    )
    st.stop()


st.set_page_config(
    page_title="Chat Assistant - Groq",
    page_icon="💬",
    layout="wide",
)


@st.cache_resource
def load_client():
    """Initialize and cache the Groq client."""
    try:
        with st.spinner("Connecting to Groq..."):
            client = Groq()
        st.success("✓ Connected to Groq!")
        return client
    except Exception as e:
        st.error(f"Failed to initialize Groq client: {str(e)}")
        return None


def get_chat_response(client, messages, model, temperature=0.7, max_tokens=1024):
    """Generate a chat response using the Groq API."""
    try:
        start_time = time.time()

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=0.95,
            stream=True,
        )

        response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                response += chunk.choices[0].delta.content
                yield chunk.choices[0].delta.content

        response_time = time.time() - start_time
        return response, response_time

    except Exception as e:
        yield f"Sorry, I encountered an error: {str(e)}"


if "messages" not in st.session_state:
    st.session_state.messages = []
if "client_loaded" not in st.session_state:
    st.session_state.client_loaded = False

st.title("💬 Chat Assistant")

# Model information
MODELS = {
    "llama-3.1-8b-instant": {
        "name": "Llama 3.1 8B",
        "speed": "560 T/sec",
        "context": "131K",
        "max_output": 131072
    },
    "llama-3.3-70b-versatile": {
        "name": "Llama 3.3 70B",
        "speed": "280 T/sec",
        "context": "131K",
        "max_output": 32768
    },
    "meta-llama/llama-guard-4-12b": {
        "name": "Llama Guard 4 12B",
        "speed": "1200 T/sec",
        "context": "131K",
        "max_output": 1024
    },
    "openai/gpt-oss-120b": {
        "name": "GPT OSS 120B",
        "speed": "500 T/sec",
        "context": "131K",
        "max_output": 65536
    },
    "openai/gpt-oss-20b": {
        "name": "GPT OSS 20B",
        "speed": "1000 T/sec",
        "context": "131K",
        "max_output": 65536
    }
}

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "llama-3.3-70b-versatile"

current_model = MODELS[st.session_state.selected_model]
st.caption(f"Powered by Groq • {current_model['name']} • {current_model['speed']}")

with st.sidebar:
    st.markdown("### Model Selection")
    
    selected_model = st.selectbox(
        "Choose Model",
        options=list(MODELS.keys()),
        format_func=lambda x: f"{MODELS[x]['name']} ({MODELS[x]['speed']})",
        index=list(MODELS.keys()).index(st.session_state.selected_model),
        help="Select the AI model for chat responses"
    )
    
    # Update model and clear chat if changed
    if selected_model != st.session_state.selected_model:
        st.session_state.selected_model = selected_model
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("### Settings")
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more random, lower values more deterministic"
    )
    
    # Dynamic max tokens based on selected model
    max_output_tokens = MODELS[selected_model]["max_output"]
    default_tokens = min(1024, max_output_tokens)
    
    max_tokens = st.slider(
        "Max Tokens",
        min_value=256,
        max_value=min(8192, max_output_tokens),
        value=default_tokens,
        step=256,
        help=f"Maximum length of the response (model limit: {max_output_tokens:,})"
    )

    with st.expander("ℹ️ Current Model Info"):
        model_info = MODELS[selected_model]
        st.markdown(
            f"""
        **{model_info['name']}**
        - Speed: {model_info['speed']}
        - Context Window: {model_info['context']} tokens
        - Max Output: {model_info['max_output']:,} tokens
        - Provider: Groq (Ultra-low latency)
        """
        )

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if not st.session_state.client_loaded:
    client = load_client()
    if client:
        st.session_state.client = client
        st.session_state.client_loaded = True
    else:
        st.error("Failed to load Groq client. Check API key and refresh.")
        st.stop()
else:
    client = st.session_state.client

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Message Chat Assistant..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Prepare messages for API (only role and content)
        api_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
        
        # Stream the response
        for chunk in get_chat_response(
            client, 
            api_messages, 
            st.session_state.selected_model,
            temperature, 
            max_tokens
        ):
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Welcome message for new users
if len(st.session_state.messages) == 0:
    st.markdown("### Welcome!")
    st.info(
        "👋 I'm your AI assistant powered by Groq. Ask me anything!"
    )

    with st.expander("💡 Example Prompts"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                "• Explain quantum computing\n"
                "• Write a Python function\n"
                "• Summarize recent AI trends"
            )
        with col2:
            st.markdown(
                "• Help me debug code\n"
                "• Create a recipe\n"
                "• Brainstorm ideas"
            )