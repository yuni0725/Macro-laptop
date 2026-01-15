import asyncio
import sys

if sys.platform == "win32":
    print("--> Applying Windows-specific asyncio event loop policy.")
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from playwright_version import run_apply_script

app = FastAPI()


class Credentials(BaseModel):
    student_id: str
    password: str
    laptop_number: int


@app.post("/apply")
async def apply(credentials: Credentials):
    try:
        print(f"Received request for student ID: {credentials.student_id}")
        result = await run_apply_script(
            credentials.student_id,
            credentials.password,
            credentials.laptop_number,
            False,
        )
        print(f"{credentials.student_id} : {result.get('status')}")
        result["id"] = credentials.student_id
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to run the apply script.")
