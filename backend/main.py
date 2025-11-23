from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import config


import search

app = FastAPI()


class ChatRequest(BaseModel):
    message: str
    model: str = config.DEFAULT_MODEL
    max_tokens: int = config.DEFAULT_MAX_TOKENS


class RAGChatRequest(BaseModel):
    message: str
    model: str = config.DEFAULT_MODEL
    max_tokens: int = config.DEFAULT_MAX_TOKENS
    top_k: int = 3 


@app.get("/")
def read_root():
    return {"message": "RAG（support TXT/PDF/Excel）"
           }

@app.post("/api/chat")
async def chat_with_gpt(request: ChatRequest):
    try:
        url = f"{config.OPENAI_BASE_URL}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {config.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": request.model,
            "messages": [{"role": "user", "content": request.message}],
            "max_tokens": request.max_tokens
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=30.0)
            response.raise_for_status()
            data = response.json()
        
        return {
            "success": True,
            "response": data["choices"][0]["message"]["content"],
            "model": request.model,
            "usage": data.get("usage", {})
        }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"HTTP error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/rag/chat")
async def rag_chat(request: RAGChatRequest):
    try:
        
        context = search.search_similar_docs(request.message, top_k=request.top_k)
       
        system_prompt = f"""Please answer the user question based on the following context. If the context does not provide relevant information, please provide a brief answer.
        Context:
        {context}
        """
        
        url = f"{config.OPENAI_BASE_URL}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {config.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": request.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message}
            ],
            "max_tokens": request.max_tokens
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=60.0)
            response.raise_for_status()
            data = response.json()
        
        return {
            "success": True,
            "response": data["choices"][0]["message"]["content"],
            "context": context,
            "model": request.model,
            "usage": data.get("usage", {})
        }
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))