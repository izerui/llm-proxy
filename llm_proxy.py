import json

import httpx
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import StreamingResponse


class AppLogger:
    def __init__(self, log_file="llm.log"):
        """Initialize the logger with a file that will be cleared on startup."""
        self.log_file = log_file
        # Clear the log file on startup
        with open(self.log_file, 'w') as f:
            f.write("")

    def log(self, message, end="\n"):
        """Log a message to both file and console."""

        # Log to file
        with open(self.log_file, 'a') as f:
            f.write(message + end)

        # Log to console
        print(message, end=end)


app = FastAPI(title="LLM API Logger")
logger = AppLogger("llm.log")


@app.post("/v1/chat/completions")
async def proxy_request(request: Request):

    body_bytes = await request.body()
    body_str = body_bytes.decode('utf-8')
    logger.log(f"模型请求：{body_str}")
    body = await request.json()

    logger.log("模型返回：", end="")

    async def event_stream():
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                    "POST",
                    "https://api.deepseek.com/v1/chat/completions",
                    json=body,
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "text/event-stream",
                        "Authorization": request.headers.get("Authorization"),
                    },
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        try:
                            if line == "data: [DONE]":
                                logger.log('\n [DONE]')
                            else:
                                data = line[6:]  # Remove "data: " prefix
                                response_data = json.loads(data)
                                if "choices" in response_data and response_data["choices"]:
                                    content = response_data["choices"][0].get("delta", {}).get("content", "")
                                    if content:
                                        logger.log(content, end="")
                        except json.JSONDecodeError:
                            logger.log(f"Failed to parse JSON: {line}")
                            continue
                    yield f"{line}\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)