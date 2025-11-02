from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
import pandas as pd
import io
from get_rate import get_rates_and_update_excel
app = FastAPI()

@app.post("/process-excel")
async def process_excel(file: UploadFile = File(...), year: str = Form(...), month: str = Form(...)):
    """
    接收使用者上傳的 Excel，處理後回傳新的 Excel
    """

    # 1️⃣ 讀取上傳的 Excel
    contents = await file.read()
    df = pd.read_excel(io.BytesIO(contents))
    print("原始 df shape:", df.head())
    new_df = get_rates_and_update_excel(df, year, month)
    print(new_df.head())

    # 3️⃣ 將結果寫入記憶體中的 Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        new_df.to_excel(writer, index=False, sheet_name="Result")

    # 重設指標到開頭，讓 FastAPI 能讀出資料
    output.seek(0)

    # 4️⃣ 回傳 Excel 檔案
    headers = {
        "Content-Disposition": "attachment; filename=processed.xlsx"
    }
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )


@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}
