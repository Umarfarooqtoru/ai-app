import streamlit as st
import streamlit.components.v1 as components
import base64
from generator import HTMLGenerator

# Configure page
st.set_page_config(
    page_title="AI HTML Generator",
    page_icon="🎨",
    layout="wide"
)

# Initialize the HTML generator
@st.cache_resource
def load_generator():
    return HTMLGenerator()

generator = load_generator()

# Display model status
if hasattr(generator, 'model_name'):
    if generator.model_name == "deepseek-coder":
        st.success("🚀 Using DeepSeek Coder 6.7B for high-quality code generation")
    elif generator.model_name == "dialogpt":
        st.info("🤖 Using Microsoft DialoGPT for AI generation")
    elif generator.model_name == "distilgpt2":
        st.info("⚡ Using DistilGPT2 model for lightweight AI generation")
    elif generator.model_name == "gpt2":
        st.info("🔄 Using GPT2 model for AI generation")
    elif generator.use_openai:
        st.success("🤖 OpenAI API available for generation")
    else:
        st.info("📋 Using smart template-based generation")
        st.info("💡 Tip: AI models may be rate-limited. Templates provide reliable, high-quality results!")

# Main app interface
st.title("🎨 AI HTML Generator")
st.markdown("Generate beautiful HTML web apps from simple English descriptions using AI")

# Show rate limit information if using templates
if hasattr(generator, 'model_name') and generator.model_name == "template":
    with st.expander("ℹ️ About Template-Based Generation", expanded=False):
        st.markdown("""
        **Smart Template Generation Active**
        
        - 🎯 **Intelligent matching**: Analyzes your description to select the best template
        - 🎨 **Professional designs**: Calculator, Todo List, Contact Form, and more
        - ⚡ **Instant results**: No waiting for model downloads or API calls
        - 🔄 **Always reliable**: Works even when AI models are rate-limited
        
        *AI models may return later when rate limits reset!*
        """)

st.markdown("---")

# Create two columns for layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Describe Your App")
    
    # Text area for user prompt
    user_prompt = st.text_area(
        "Enter your app description:",
        placeholder="e.g., Create a simple calculator app with buttons for basic operations",
        height=150,
        help="Describe what kind of web app you want to create. Be as specific as possible!"
    )
    
    # Generate button
    generate_btn = st.button("🚀 Generate App", type="primary", use_container_width=True)
    
    # Example prompts
    st.markdown("### 💡 Example Prompts:")
    examples = [
        "Create a simple to-do list app with add and delete functionality",
        "Build a color picker tool with RGB and hex values",
        "Make a basic calculator with arithmetic operations",
        "Design a contact form with name, email, and message fields",
        "Create a photo gallery with grid layout"
    ]
    
    for example in examples:
        if st.button(f"💭 {example}", key=example):
            st.session_state.user_prompt = example
            st.rerun()

with col2:
    st.header("🖥️ Generated Code & Preview")
    
    # Check if we have a stored prompt to use
    if 'user_prompt' in st.session_state:
        user_prompt = st.session_state.user_prompt

    if generate_btn and user_prompt:
        with st.spinner("🤖 Generating your HTML app..."):
            try:
                # Generate HTML code
                html_code = generator.generate_html(user_prompt)
                
                # Store in session state
                st.session_state.generated_html = html_code
                st.session_state.current_prompt = user_prompt
                
            except Exception as e:
                st.error(f"Error generating code: {str(e)}")
                html_code = None
    
    # Display generated code and preview
    if 'generated_html' in st.session_state:
        html_code = st.session_state.generated_html
        
        # Tabs for code and preview
        tab1, tab2 = st.tabs(["📄 Generated Code", "👁️ Live Preview"])
        
        with tab1:
            st.code(html_code, language='html')
            
            # Download button
            b64_html = base64.b64encode(html_code.encode()).decode()
            href = f'<a href="data:text/html;base64,{b64_html}" download="generated_app.html">📥 Download HTML File</a>'
            st.markdown(href, unsafe_allow_html=True)
        
        with tab2:
            # Live HTML preview
            try:
                components.html(html_code, height=600, scrolling=True)
            except Exception as e:
                st.error(f"Preview error: {str(e)}")
                st.text("Preview not available for this generated code")

# Footer
st.markdown("---")
st.markdown(
    "Built with ❤️ using Streamlit and Hugging Face Transformers | "
    "Deploy on [Streamlit Cloud](https://streamlit.io/cloud)"
)
