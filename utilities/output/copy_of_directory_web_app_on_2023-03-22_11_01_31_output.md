# Copy of directory: web_app on 2023-03-22_11_01_31
Configurations: self.excuded_directories: ['__pycache__', 'venv', 'build', 'dist', 'golem_garden.egg-info', 'tests', 'system', 'utilities', 'notes', 'experimental'], self.included_file_types: ['.py', '.txt', '.md'] 
 
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
