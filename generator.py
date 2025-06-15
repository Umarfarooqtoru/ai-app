import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import re

class HTMLGenerator:
    def __init__(self):
        self.model_name = "replit/replit-code-v1-3b"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.load_model()
    
    @st.cache_resource
    def load_model(_self):
        """Load the code generation model"""
        try:
            # Load tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained(_self.model_name, trust_remote_code=True)
            model = AutoModelForCausalLM.from_pretrained(
                _self.model_name,
                trust_remote_code=True,
                torch_dtype=torch.float16 if _self.device == "cuda" else torch.float32,
                device_map="auto" if _self.device == "cuda" else None
            )
            
            # Create pipeline
            _self.generator = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                device=0 if _self.device == "cuda" else -1,
                torch_dtype=torch.float16 if _self.device == "cuda" else torch.float32
            )
            
            return True
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            _self.generator = None
            return False
    
    def create_prompt(self, user_description):
        """Create a structured prompt for HTML generation"""
        prompt = f"""Generate a complete HTML web application based on this description: "{user_description}"

Requirements:
- Complete HTML document with DOCTYPE, head, and body
- Include CSS styling in <style> tags for modern, responsive design
- Add JavaScript functionality in <script> tags if needed
- Use semantic HTML elements
- Make it visually appealing with good UX
- Ensure it works as a standalone HTML file

HTML:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>"""
        
        return prompt
    
    def clean_generated_html(self, generated_text):
        """Clean and extract HTML from generated text"""
        # Look for HTML content starting with <!DOCTYPE or <html>
        html_pattern = r'(<!DOCTYPE html>.*?</html>)'
        match = re.search(html_pattern, generated_text, re.DOTALL | re.IGNORECASE)
        
        if match:
            html_content = match.group(1)
        else:
            # Fallback: look for any HTML-like content
            html_start = generated_text.find('<html')
            if html_start == -1:
                html_start = generated_text.find('<!DOCTYPE')
            
            if html_start != -1:
                html_content = generated_text[html_start:]
                # Try to find the end of HTML
                html_end = html_content.rfind('</html>')
                if html_end != -1:
                    html_content = html_content[:html_end + 7]
            else:
                # Generate a basic HTML structure if none found
                html_content = self.create_fallback_html(generated_text)
        
        return html_content.strip()
    
    def create_fallback_html(self, description):
        """Create a basic HTML template when generation fails"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated App</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #5a67d8;
            text-align: center;
            margin-bottom: 20px;
        }}
        .feature {{
            background: #f7fafc;
            padding: 20px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #5a67d8;
        }}
        button {{
            background: #5a67d8;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
        }}
        button:hover {{
            background: #4c51bf;
        }}
        input, textarea {{
            width: 100%;
            padding: 10px;
            border: 2px solid #e2e8f0;
            border-radius: 6px;
            font-size: 16px;
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Generated Web Application</h1>
        <div class="feature">
            <h3>Description:</h3>
            <p>{description}</p>
        </div>
        <div class="feature">
            <h3>Interactive Elements:</h3>
            <button onclick="alert('Hello! This is your generated app.')">Click Me</button>
            <input type="text" placeholder="Enter some text...">
        </div>
        <div class="feature">
            <h3>Status:</h3>
            <p>Your web application has been generated successfully!</p>
        </div>
    </div>
    
    <script>
        console.log('Generated app loaded successfully!');
        
        // Add some basic interactivity
        document.addEventListener('DOMContentLoaded', function() {{
            const inputs = document.querySelectorAll('input[type="text"]');
            inputs.forEach(input => {{
                input.addEventListener('input', function() {{
                    console.log('User input:', this.value);
                }});
            }});
        }});
    </script>
</body>
</html>"""
    
    def generate_html(self, user_description):
        """Generate HTML code based on user description"""
        if not self.generator:
            return self.create_fallback_html(user_description)
        
        try:
            # Create the prompt
            prompt = self.create_prompt(user_description)
            
            # Generate code
            generated = self.generator(
                prompt,
                max_length=2048,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.generator.tokenizer.eos_token_id,
                truncation=True
            )
            
            # Extract and clean the generated HTML
            generated_text = generated[0]['generated_text']
            html_code = self.clean_generated_html(generated_text)
            
            # Validate that we have proper HTML
            if not html_code.strip().lower().startswith('<!doctype') and not html_code.strip().lower().startswith('<html'):
                html_code = self.create_fallback_html(user_description)
            
            return html_code
            
        except Exception as e:
            st.error(f"Generation error: {str(e)}")
            return self.create_fallback_html(user_description)
