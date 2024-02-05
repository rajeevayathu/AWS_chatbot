from fastapi import FastAPI, HTTPException
import boto3
from fastapi.middleware.cors import CORSMiddleware
import os
print("AWS_ACCESS_KEY_ID", os.getenv("AWS_ACCESS_KEY_ID"))
print("AWS_SECRET_ACCESS_KEY:", os.getenv("AWS_SECRET_ACCESS_KEY"))

# Initialize FastAPI app
app = FastAPI()

# Configure CORS (adjust the origins according to your needs)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AWS Configuration
AWS_REGION = 'us-east-1'
BOT_ID = 'YNTXRQWRO4'
BOT_ALIAS_ID = 'OFKWVNTURC'

# Initialize boto3 Lex V2 Runtime client
lex_client = boto3.client('lexv2-runtime', region_name=AWS_REGION)

@app.post("/chat")
async def chat(message: str):
    try:
        # Sending user input to Amazon Lex V2 and receiving the response
        response = lex_client.recognize_text(
            botId=BOT_ID,
            botAliasId=BOT_ALIAS_ID,
            localeId='en_US',
            sessionId='userID',
            text=message
        )
        print("Lex Response:", response)
        return {"response": response}
    except Exception as e:

        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Run the server with Uvicorn or Hypercorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)





