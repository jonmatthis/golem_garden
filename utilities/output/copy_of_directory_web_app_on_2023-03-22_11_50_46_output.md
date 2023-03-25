# Copy of directory: web_app on 2023-03-22_11_50_46
Configurations: self.excuded_directories: ['__pycache__', 'venv', 'build', 'dist', 'golem_garden.egg-info', 'tests', 'system', 'utilities', 'notes', 'experimental'], self.included_file_types: ['.py', '.txt', '.md', '.html', '.css', '.js', '.json'] 
 
### C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\user_interface\web_app\app.py

```python
# web_app/app.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

app = None

def get_web_app():
    global app
    if app is None:
        app = FastAPI()
    return app


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat(payload: dict):
    user_input = payload["user_input"]
    golem_response = await golem_garden.pass_message_to_golem(
        message=user_input, golem_name="GreeterGolem"
    )
    return JSONResponse(content={"golem_response": golem_response})

```

### C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\user_interface\web_app\templates\index.html

```python
<!-- web_app/templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Golem Garden</title>
</head>
<body>
    <h1>Welcome to Golem Garden</h1>
    <form id="chat-form">
        <input type="text" id="user-input" placeholder="Type your message...">
        <button type="submit">Send</button>
    </form>
    <div id="chat-area"></div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function() {
            $('#chat-form').on('submit', function(event) {
                event.preventDefault();
                var user_input = $('#user-input').val();
                if (user_input) {
                    $.ajax({
                        type: "POST",
                        url: "/chat",
                        data: JSON.stringify({user_input: user_input}),
                        contentType: "application/json",
                        success: function(data) {
                            var golem_response = data.golem_response;
                            $('#chat-area').append('<p>User: ' + user_input + '</p>');
                            $('#chat-area').append('<p>Golem: ' + golem_response + '</p>');
                            $('#user-input').val('');
                        }
                    });
                }
            });
        });
    </script>
</body>
</html>

```
