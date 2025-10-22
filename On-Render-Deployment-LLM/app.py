import streamlit as st
from groq import Groq
import time
import os
import re

if "GROQ_API_KEY" not in os.environ:
    st.error(
        "GROQ_API_KEY environment variable not set! Please set it in your environment or secrets."
    )
    st.info(
        "You can get a free API key from https://console.groq.com/"
    )
    st.stop()


st.set_page_config(
    page_title="Story Generator - Groq",
    page_icon="📚",
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


def generate_story(client, prompt, max_length=200):
    """Generate a story using the Groq API."""
    try:
        if not prompt.lower().startswith("once upon a time"):
            formatted_prompt = f"Once upon a time {prompt.lower()}"
        else:
            formatted_prompt = prompt

        start_time = time.time()

        # System prompt to guide the model
        system_message = (
            "You are a creative storyteller. "
            "Continue the story based on the user's prompt. "
            "Do not repeat the user's prompt; only write the continuation. "
            "The story should be engaging and at least 50 words long."
        )

        try:
            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b",  # Fast and capable model on Groq
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": formatted_prompt},
                ],
                max_tokens=max_length,
                temperature=0.8,
                top_p=0.95,
                stream=False,  # We'll get the full response and stream it manually
            )

            response_time = time.time() - start_time
            response = completion.choices[0].message.content

            response = re.sub(r"\s+", " ", response)
            response = response.strip()

        except Exception as model_error:
            st.warning(
                f"Model generation failed ({model_error}), using fallback story."
            )
            response_time = time.time() - start_time
            response = get_fallback_story(prompt)

        return response, response_time

    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}", 0


def get_fallback_story(prompt):
    """Generate fallback stories based on prompt content"""
    prompt_lower = prompt.lower()

    if "robot" in prompt_lower:
        return "there was a friendly robot named Rob who lived in a small village. Rob loved to help people and make their lives easier. One day, Rob discovered that the village's water pump was broken, so it used its mechanical skills to fix it. The villagers were so grateful that they threw a celebration in Rob's honor."
    elif "magical" in prompt_lower or "forest" in prompt_lower:
        return "there was an enchanted forest where the trees whispered secrets and the flowers glowed with magical light. A young explorer named Luna discovered that the forest was home to talking animals and mystical creatures. Together, they embarked on a quest to save the forest from an evil spell that was making the magic fade away."
    elif "friendship" in prompt_lower or "friend" in prompt_lower:
        return "there were two best friends, Maya and Alex, who lived in neighboring villages. When a terrible storm separated their villages, Maya and Alex worked together to build a bridge that would reunite their communities. Through their friendship, they taught everyone that cooperation and kindness can overcome any obstacle."
    elif "knight" in prompt_lower:
        return "there was a brave knight who protected the kingdom from dragons and dark magic. One day, the knight discovered that the real treasure was not gold or jewels, but the happiness and safety of the people they protected."
    elif "cat" in prompt_lower:
        return "there was a curious cat named Whiskers who loved to explore. One day, Whiskers found a secret garden behind the old library where magical creatures lived. The cat became the guardian of this hidden world, protecting it from those who would harm its beauty."
    elif "wizard" in prompt_lower:
        return "there was a wise old wizard who lived in a tower filled with books and potions. The wizard spent their days teaching young apprentices about magic, but their greatest lesson was that true magic comes from kindness and helping others."
    elif "dragon" in prompt_lower:
        return "there was a gentle dragon who lived in the mountains and collected shiny stones instead of gold. The dragon became friends with a brave child who showed everyone that dragons could be kind and helpful, not scary monsters."
    else:
        return "there was a brave adventurer who set out on a journey to discover new lands. Along the way, they met interesting characters, faced exciting challenges, and learned valuable lessons about courage, friendship, and the importance of following one's dreams."


if "messages" not in st.session_state:
    st.session_state.messages = []
if "client_loaded" not in st.session_state:
    st.session_state.client_loaded = False

st.title("📚 Story Generator")
st.caption("Powered by Groq • mixtral-8x7b-32768")

with st.sidebar:
    st.markdown("### Settings")
    max_length = st.slider(
        "Story Length", min_value=100, max_value=300, value=200, step=10
    )

    with st.expander("ℹ️ Model Info"):
        st.markdown(
            """
        **Groq API**
        - Provider: Groq
        - Model: openai/gpt-oss-20b
        - Ultra-low latency API
        """
        )

    if st.button("Clear", use_container_width=True):
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

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

chat_input = st.chat_input("Start your story idea...")
if chat_input:
    prompt = chat_input
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(f"**Your idea:** {prompt}")

    with st.chat_message("assistant"):
        with st.spinner("Writing story..."):
            response, response_time = generate_story(
                client, prompt, max_length
            )

        full_story = f"Once upon a time {response}"

        words = full_story.split()
        displayed_story = ""
        message_placeholder = st.empty()

        for word in words:
            displayed_story += word + " "
            message_placeholder.markdown(displayed_story + "▌")
            time.sleep(0.03)

        message_placeholder.markdown(displayed_story)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_story}
    )

if len(st.session_state.messages) == 0:
    st.markdown("### Welcome!")
    st.info(
        "Type a story idea and it will create a story starting with 'Once upon a time...'"
    )

    with st.expander("💡 Example Ideas"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                "• a brave knight\n• a magical forest\n• a friendly robot"
            )
        with col2:
            st.markdown(
                "• a curious cat\n• two best friends\n• a wise wizard"
            )