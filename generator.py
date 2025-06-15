import streamlit as st
import re
import random
import requests
import json
import os

class HTMLGenerator:
    def __init__(self):
        self.use_openai = False
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            self.use_openai = True
        
        # Load templates for fallback
        self.templates = self._load_templates()
        
        # Initialize model properties
        self.generator = None
        self.model_name = "none"
        
        # Try to load DeepSeek Coder or fallback models
        self._try_load_simple_model()
    
    def _try_load_simple_model(self):
        """Try to load AI models with multiple fallbacks"""
        try:
            import transformers
            from transformers import pipeline
            
            st.info("🔄 Loading AI model for code generation...")
            
            # List of models to try in order (from best to most reliable)
            models_to_try = [
                {
                    "name": "deepseek-ai/deepseek-coder-6.7b-instruct",
                    "display_name": "DeepSeek Coder 6.7B",
                    "max_length": 2048,
                    "temperature": 0.3,
                    "model_id": "deepseek-coder"
                },
                {
                    "name": "microsoft/DialoGPT-medium",
                    "display_name": "Microsoft DialoGPT Medium", 
                    "max_length": 512,
                    "temperature": 0.7,
                    "model_id": "dialogpt"
                },
                {
                    "name": "distilgpt2",
                    "display_name": "DistilGPT2",
                    "max_length": 512,
                    "temperature": 0.8,
                    "model_id": "distilgpt2"
                },
                {
                    "name": "gpt2",
                    "display_name": "GPT2",
                    "max_length": 512,
                    "temperature": 0.8,
                    "model_id": "gpt2"
                }
            ]
            
            for model_config in models_to_try:
                try:
                    st.info(f"🔄 Trying to load {model_config['display_name']}...")
                    
                    # Set timeout and retry parameters
                    pipeline_kwargs = {
                        "model": model_config["name"],
                        "max_length": model_config["max_length"],
                        "device_map": "auto" if model_config["model_id"] == "deepseek-coder" else None,
                        "trust_remote_code": True if model_config["model_id"] == "deepseek-coder" else False
                    }
                    
                    # Add timeout for model loading
                    import requests
                    requests.adapters.DEFAULT_TIMEOUT = 30
                    
                    self.generator = pipeline("text-generation", **pipeline_kwargs)
                    self.model_name = model_config["model_id"]
                    self.model_config = model_config
                    
                    st.success(f"✅ {model_config['display_name']} loaded successfully!")
                    return
                    
                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg or "rate limit" in error_msg.lower():
                        st.warning(f"⚠️ {model_config['display_name']}: Rate limited by Hugging Face. Trying next model...")
                    elif "timeout" in error_msg.lower():
                        st.warning(f"⚠️ {model_config['display_name']}: Download timeout. Trying next model...")
                    else:
                        st.warning(f"⚠️ {model_config['display_name']}: {error_msg}")
                    continue
            
            # If all models fail, fall back to template generation
            st.warning("⚠️ All AI models unavailable due to rate limits or errors. Using template-based generation.")
            self.generator = None
            self.model_name = "template"
            
        except ImportError:
            st.info("ℹ️ Transformers not available. Using smart template-based generation.")
            self.generator = None
            self.model_name = "template"
        except Exception as e:
            st.warning(f"⚠️ AI models not available: {str(e)}. Using template-based generation.")
            self.generator = None
            self.model_name = "template"
    
    def _load_templates(self):
        """Load HTML templates for different types of apps"""
        return {
            'calculator': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculator App</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .calculator {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            max-width: 300px;
            width: 100%;
        }
        .display {
            width: 100%;
            height: 60px;
            font-size: 24px;
            text-align: right;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 8px;
            margin-bottom: 15px;
            background: #f9f9f9;
            box-sizing: border-box;
        }
        .buttons {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }
        button {
            height: 60px;
            font-size: 18px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .number, .operator {
            background: #e8e8e8;
            color: #333;
        }
        .number:hover, .operator:hover {
            background: #d0d0d0;
        }
        .equals {
            background: #667eea;
            color: white;
        }
        .equals:hover {
            background: #5a6fd8;
        }
        .clear {
            background: #ff6b6b;
            color: white;
        }
        .clear:hover {
            background: #ee5a5a;
        }
    </style>
</head>
<body>
    <div class="calculator">
        <input type="text" class="display" id="display" readonly>
        <div class="buttons">
            <button class="clear" onclick="clearDisplay()">C</button>
            <button class="operator" onclick="appendToDisplay('/')">/</button>
            <button class="operator" onclick="appendToDisplay('*')">×</button>
            <button class="operator" onclick="appendToDisplay('-')">-</button>
            <button class="number" onclick="appendToDisplay('7')">7</button>
            <button class="number" onclick="appendToDisplay('8')">8</button>
            <button class="number" onclick="appendToDisplay('9')">9</button>
            <button class="operator" onclick="appendToDisplay('+')">+</button>
            <button class="number" onclick="appendToDisplay('4')">4</button>
            <button class="number" onclick="appendToDisplay('5')">5</button>
            <button class="number" onclick="appendToDisplay('6')">6</button>
            <button class="equals" onclick="calculate()" rowspan="2">=</button>
            <button class="number" onclick="appendToDisplay('1')">1</button>
            <button class="number" onclick="appendToDisplay('2')">2</button>
            <button class="number" onclick="appendToDisplay('3')">3</button>
            <button class="number" onclick="appendToDisplay('0')" colspan="2">0</button>
            <button class="number" onclick="appendToDisplay('.')">.</button>
        </div>
    </div>
    <script>
        function appendToDisplay(value) {
            document.getElementById('display').value += value;
        }
        function clearDisplay() {
            document.getElementById('display').value = '';
        }
        function calculate() {
            try {
                let result = eval(document.getElementById('display').value.replace('×', '*'));
                document.getElementById('display').value = result;
            } catch(error) {
                document.getElementById('display').value = 'Error';
            }
        }
    </script>
</body>
</html>''',
            'todo': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>To-Do List App</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: #0984e3;
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 28px;
        }
        .input-section {
            padding: 20px;
            border-bottom: 1px solid #eee;
        }
        .input-group {
            display: flex;
            gap: 10px;
        }
        input[type="text"] {
            flex: 1;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }
        .add-btn {
            padding: 12px 24px;
            background: #00b894;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.2s;
        }
        .add-btn:hover {
            background: #00a085;
        }
        .todo-list {
            padding: 20px;
        }
        .todo-item {
            display: flex;
            align-items: center;
            padding: 15px;
            margin-bottom: 10px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #0984e3;
        }
        .todo-text {
            flex: 1;
            font-size: 16px;
            margin-left: 10px;
        }
        .todo-text.completed {
            text-decoration: line-through;
            color: #999;
        }
        .delete-btn {
            background: #e17055;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        .delete-btn:hover {
            background: #d63031;
        }
        .empty-state {
            text-align: center;
            color: #999;
            font-style: italic;
            padding: 40px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 My To-Do List</h1>
        </div>
        <div class="input-section">
            <div class="input-group">
                <input type="text" id="todoInput" placeholder="Add a new task..." onkeypress="handleKeyPress(event)">
                <button class="add-btn" onclick="addTodo()">Add Task</button>
            </div>
        </div>
        <div class="todo-list" id="todoList">
            <div class="empty-state">No tasks yet. Add one above!</div>
        </div>
    </div>
    <script>
        let todos = [];
        function addTodo() {
            const input = document.getElementById('todoInput');
            const text = input.value.trim();
            if (text) {
                todos.push({
                    id: Date.now(),
                    text: text,
                    completed: false
                });
                input.value = '';
                renderTodos();
            }
        }
        function deleteTodo(id) {
            todos = todos.filter(todo => todo.id !== id);
            renderTodos();
        }
        function toggleTodo(id) {
            todos = todos.map(todo => 
                todo.id === id ? {...todo, completed: !todo.completed} : todo
            );
            renderTodos();
        }
        function renderTodos() {
            const container = document.getElementById('todoList');
            if (todos.length === 0) {
                container.innerHTML = '<div class="empty-state">No tasks yet. Add one above!</div>';
                return;
            }
            container.innerHTML = todos.map(todo => `
                <div class="todo-item">
                    <input type="checkbox" ${todo.completed ? 'checked' : ''} onchange="toggleTodo(${todo.id})">
                    <span class="todo-text ${todo.completed ? 'completed' : ''}">${todo.text}</span>
                    <button class="delete-btn" onclick="deleteTodo(${todo.id})">Delete</button>
                </div>
            `).join('');
        }
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                addTodo();
            }
        }
    </script>
</body>
</html>''',
            'contact': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Form</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .form-container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            max-width: 500px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 28px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
        }
        input, textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
            box-sizing: border-box;
        }
        input:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        textarea {
            height: 120px;
            resize: vertical;
        }
        .submit-btn {
            width: 100%;
            padding: 15px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
            transition: background 0.3s;
        }
        .submit-btn:hover {
            background: #5a6fd8;
        }
        .success-message {
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <h1>📞 Contact Us</h1>
        <form id="contactForm">
            <div class="form-group">
                <label for="name">Full Name *</label>
                <input type="text" id="name" name="name" required>
            </div>
            <div class="form-group">
                <label for="email">Email Address *</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="phone">Phone Number</label>
                <input type="tel" id="phone" name="phone">
            </div>
            <div class="form-group">
                <label for="subject">Subject *</label>
                <input type="text" id="subject" name="subject" required>
            </div>
            <div class="form-group">
                <label for="message">Message *</label>
                <textarea id="message" name="message" placeholder="Tell us how we can help you..." required></textarea>
            </div>
            <button type="submit" class="submit-btn">Send Message</button>
        </form>
        <div id="successMessage" class="success-message">
            Thank you for your message! We'll get back to you soon.
        </div>
    </div>
    <script>
        document.getElementById('contactForm').addEventListener('submit', function(e) {
            e.preventDefault();
            document.getElementById('successMessage').style.display = 'block';
            this.reset();
            setTimeout(() => {
                document.getElementById('successMessage').style.display = 'none';
            }, 5000);
        });
    </script>
</body>
</html>'''
        }
    
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
    
    def _match_description_to_template(self, description):
        """Match user description to the most appropriate template"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ['calculator', 'calc', 'math', 'arithmetic', 'number']):
            return 'calculator'
        elif any(word in description_lower for word in ['todo', 'task', 'list', 'checklist', 'reminder']):
            return 'todo'
        elif any(word in description_lower for word in ['contact', 'form', 'email', 'message', 'feedback']):
            return 'contact'
        else:
            # Default to a random template
            return random.choice(['calculator', 'todo', 'contact'])
    
    def _customize_template(self, template, description):
        """Customize the template based on the user description"""
        # Extract potential title from description
        words = description.split()
        if len(words) > 0:
            # Simple title generation
            title_words = [word.capitalize() for word in words[:3] if word.lower() not in ['a', 'an', 'the', 'for', 'with', 'app', 'application']]
            if title_words:
                custom_title = ' '.join(title_words) + ' App'
                template = template.replace('<title>Calculator App</title>', f'<title>{custom_title}</title>')
                template = template.replace('<title>To-Do List App</title>', f'<title>{custom_title}</title>')
                template = template.replace('<title>Contact Form</title>', f'<title>{custom_title}</title>')
        
        return template
    
    def _generate_with_openai(self, description):
        """Generate HTML using OpenAI API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.openai_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are an expert web developer. Generate complete, functional HTML applications with embedded CSS and JavaScript. Always return valid HTML that works as a standalone file."
                    },
                    {
                        "role": "user", 
                        "content": f"Create a complete HTML web application for: {description}. Include modern CSS styling and JavaScript functionality. Make it responsive and visually appealing."
                    }
                ],
                "max_tokens": 2000,
                "temperature": 0.7
            }
            
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                st.error(f"OpenAI API error: {response.status_code}")
                return None
                
        except Exception as e:
            st.error(f"OpenAI generation error: {str(e)}")
            return None
    
    def _generate_with_simple_model(self, description):
        """Generate HTML using transformer model with optimized prompts"""
        try:
            if not hasattr(self, 'model_config'):
                # Fallback config for older instances
                self.model_config = {
                    "max_length": 512,
                    "temperature": 0.8,
                    "model_id": self.model_name
                }
            
            if self.model_name == "deepseek-coder":
                # Use DeepSeek Coder specific prompt format
                prompt = f"""<|begin▁of▁sentence|>You are an expert web developer. Create a complete, functional HTML application.

Task: {description}

Requirements:
- Complete HTML document with DOCTYPE, head, and body
- Modern CSS styling with responsive design  
- JavaScript functionality where needed
- Professional appearance and user experience
- All code in a single HTML file

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>"""
                
            else:
                # Use optimized prompt for other models
                prompt = f"""Create a complete HTML web application for: {description}

Make it include:
- Modern CSS styling
- Interactive JavaScript
- Responsive design
- Professional look

HTML code:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>"""
            
            # Generate with model-specific parameters
            result = self.generator(
                prompt, 
                max_length=self.model_config["max_length"], 
                num_return_sequences=1, 
                temperature=self.model_config["temperature"],
                do_sample=True,
                pad_token_id=self.generator.tokenizer.eos_token_id if hasattr(self.generator, 'tokenizer') else None
            )
            
            generated_text = result[0]['generated_text']
            
            # Clean and extract HTML
            return self.clean_generated_html(generated_text)
            
        except Exception as e:
            st.error(f"Model generation error: {str(e)}")
            return None
    
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
            box-sizing: border-box;
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
        try:
            # Try OpenAI first if available
            if self.use_openai:
                html_code = self._generate_with_openai(user_description)
                if html_code:
                    return html_code
            
            # Try simple transformer model if available
            if self.generator:
                html_code = self._generate_with_simple_model(user_description)
                if html_code:
                    return html_code
            
            # Fall back to template-based generation
            template_type = self._match_description_to_template(user_description)
            template = self.templates.get(template_type, self.templates['calculator'])
            customized_html = self._customize_template(template, user_description)
            
            return customized_html
            
        except Exception as e:
            st.error(f"Generation error: {str(e)}")
            return self.create_fallback_html(user_description)
