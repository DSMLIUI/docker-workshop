import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import time

st.set_page_config(
    page_title="Story Generator - DistilGPT2",
    page_icon="📚",
    layout="wide"
)

@st.cache_resource
def load_model():
    try:
        # Using DistilGPT2 - much smaller (~80MB) and optimized for low-memory environments
        # Perfect for 512MB RAM demonstrations
        model_name = "distilgpt2"
        with st.spinner("Loading model..."):
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            # Add padding token if it doesn't exist
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float32,  # Use float32 for stability
                low_cpu_mem_usage=True
            )
            
            # Set model to evaluation mode to reduce memory
            model.eval()
            
        st.success("✓ Model loaded successfully!")
        return tokenizer, model
    except Exception as e:
        st.error(f"Failed to load model: {str(e)}")
        return None, None

def generate_story(tokenizer, model, prompt, max_length=200):
    try:
        # Format prompt to start with "Once upon a time"
        if not prompt.lower().startswith("once upon a time"):
            formatted_prompt = f"Once upon a time {prompt.lower()}"
        else:
            formatted_prompt = prompt
        
        start_time = time.time()
        
        # Try to generate with the model
        try:
            input_ids = tokenizer(formatted_prompt, return_tensors="pt", padding=True, truncation=True).input_ids
            
            # Move to same device as model
            device = next(model.parameters()).device
            input_ids = input_ids.to(device)
            
            with torch.no_grad():  # Disable gradient computation for inference
                outputs = model.generate(
                    input_ids, 
                    max_length=input_ids.shape[1] + max_length,
                    min_length=input_ids.shape[1] + 50,
                    do_sample=True,
                    temperature=0.8,
                    top_p=0.95,
                    repetition_penalty=1.3,
                    pad_token_id=tokenizer.pad_token_id,
                    eos_token_id=tokenizer.eos_token_id,
                    early_stopping=True,
                    no_repeat_ngram_size=2
                )
            
            response_time = time.time() - start_time
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract the generated story continuation
            if formatted_prompt in response:
                response = response.replace(formatted_prompt, "").strip()
            
            # Clean up the response
            import re
            response = re.sub(r'\s+', ' ', response)
            response = response.strip()
            
            # If the response is too short or empty, use fallback
            if not response or len(response.strip()) < 20:
                raise Exception("Generated response too short")
                
        except Exception as model_error:
            # If model generation fails, use fallback stories
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
if "model_loaded" not in st.session_state:
    st.session_state.model_loaded = False

st.title("📚 Story Generator")
st.caption("Powered by DistilGPT2 • 80MB • 512MB RAM")

with st.sidebar:
    st.markdown("### Settings")
    max_length = st.slider("Story Length", min_value=100, max_value=300, value=200, step=10)
    
    with st.expander("ℹ️ Model Info"):
        st.markdown("""
        **DistilGPT2**
        - Size: 80MB
        - Parameters: 82M
        - Optimized for 512MB RAM
        """)
    
    if st.button("Clear", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if not st.session_state.model_loaded:
    tokenizer, model = load_model()
    if tokenizer and model:
        st.session_state.tokenizer = tokenizer
        st.session_state.model = model
        st.session_state.model_loaded = True
    else:
        st.error("Failed to load model. Please refresh the page.")
        st.stop()
else:
    tokenizer = st.session_state.tokenizer
    model = st.session_state.model

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
            response, response_time = generate_story(tokenizer, model, prompt, max_length)
        
        # Display the full story with "Once upon a time" prefix
        full_story = f"Once upon a time {response}"
        
        words = full_story.split()
        displayed_story = ""
        message_placeholder = st.empty()
        
        for word in words:
            displayed_story += word + " "
            message_placeholder.markdown(displayed_story + "▌")
            time.sleep(0.03)
        
        message_placeholder.markdown(displayed_story)
    
    st.session_state.messages.append({"role": "assistant", "content": full_story})

if len(st.session_state.messages) == 0:
    st.markdown("### Welcome!")
    st.info("Type a story idea and it will create a story starting with 'Once upon a time...'")
    
    with st.expander("💡 Example Ideas"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("• a brave knight\n• a magical forest\n• a friendly robot")
        with col2:
            st.markdown("• a curious cat\n• two best friends\n• a wise wizard")