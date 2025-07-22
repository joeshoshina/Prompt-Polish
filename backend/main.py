"""
Python 3.12.7
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from enhancer import get_boosted_prompt

app = FastAPI()

# CORS configuration to allow requests from the extension as it doenst have a dedicated port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension:jejbdolnndbgmjmjnbefbdnhnkgoafdh"],
    allow_credentials=True,
    allow_methods=["post"],
    allow_headers=["*"],
)

# Define expected shape of JSON request
class PromptRequest(BaseModel):
    user_prompt: str

@app.post("/enhance")
async def enhance_endpoint(request: PromptRequest):
    raw_prompt = request.user_prompt
    print(f"Received raw prompt: {raw_prompt}")
    try:
        enhanced_prompt = get_boosted_prompt(raw_prompt)
        return {"enhanced_prompt": enhanced_prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))