from fastapi import FastAPI, UploadFile, HTTPException
# from Middleware.Authentication import AuthenticationMiddleware
from fastapi.middleware.cors import CORSMiddleware
from Routes import dashboard, csv_upload
import pandas as pd
from io import StringIO
from uuid import uuid4
import os
import hashlib
from datetime import datetime, timezone
from starlette.responses import FileResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# app.add_middleware(AuthenticationMiddleware)

app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(csv_upload.router, prefix="/csv_upload", tags=["csv_upload"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/v2/uploadCSV")
async def create_upload_file(file: UploadFile):
    if file.filename.endswith(".csv"):
        try:
            contents = await file.read()
            string_io = StringIO(contents.decode())
            df = pd.read_csv(string_io)
            now_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S-UTC")
            if '19fb00edda2bbe1c00d0be090b9f5084' not in hashlib.md5(str(df.columns.values.tolist()).encode()).hexdigest():
                # save to Failed folder
                if not os.path.exists("Failed"):
                    os.makedirs("Failed")
                df.to_csv(f'Failed/{now_time}-{file.filename}.csv', index=False)
                raise HTTPException(status_code=400, detail="Invalid CSV file")

            # uuid = uuid4()
            if not os.path.exists("DB"):
                os.makedirs("DB")
            filename = f'{now_time}-{file.filename}'
            df.to_csv("DB/" + filename, index=False)
            return {"result": filename}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="Invalid CSV file")
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=True)
