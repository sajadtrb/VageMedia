from fastapi import APIRouter, File, UploadFile, HTTPException
from Models.csv_upload import RemoveCSV
import pandas as pd
from io import StringIO
from uuid import uuid4
import os
import hashlib
from datetime import datetime, timezone

router = APIRouter()

@router.post("/")
async def create_upload_file(file: UploadFile = File(...)):
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

@router.get("/list")
async def list_files():
    if not os.path.exists("DB"):
        os.makedirs("DB")
    files = os.listdir("DB")
    files = [file for file in files if file.endswith(".csv")]
    return {"result": files}

# remove
@router.post("/remove")
async def remove_file(file_data: RemoveCSV):
    filename = file_data.file
    if not os.path.exists("DB"):
        os.makedirs("DB")
    files = os.listdir("DB")
    files = [file for file in files if file.endswith(".csv")]
    if filename in files:
        # os.remove("DB/" + filename)
        # move to Removed folder
        if not os.path.exists("Removed"):
            os.makedirs("Removed")
        os.rename("DB/" + filename, "Removed/" + filename)
        return {"result": "success"}
    else:
        raise HTTPException(status_code=400, detail="File not found")
