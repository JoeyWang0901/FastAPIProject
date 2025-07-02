from fastapi import FastAPI, HTTPException
import ddddocr
import os
import base64

from models import APIResponse
from models import OCRRequest
from models import OCRResponse


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    ocr = ddddocr.DdddOcr()
    ROOT_DIR = os.path.abspath(os.curdir)
    print(ROOT_DIR)

    # with open("./testfile/01.png", "rb") as f:
    #     image_data = base64.b64encode(f.read()).decode()
    #
    # print(f"image_data: {image_data}")
    # result = ocr.classification(image_data)
    # print(f"base64 result = {result}")

    for i in range(1, 11):
        # image = open(ROOT_DIR + "/testfile/"+ str(i).zfill(2) + ".png", "rb").read()
        image = open(f"{ROOT_DIR}/testfile/{str(i).zfill(2)}.png", "rb").read()
        result = ocr.classification(image)
        print(result)

    return {"message": f"Hello {name}"}

@app.post("/ocr", response_model=APIResponse)
async def ocr_recognition(request: OCRRequest):
    try:
        try:
            image_data = base64.b64decode(request.image)
            print(f"image_data: {image_data}")
        except Exception:
            raise HTTPException(status_code=400, detail="圖片base64解碼失敗")
        ocr = ddddocr.DdddOcr()
        result = ocr.classification(image_data)
        print(result)

        response_data = OCRResponse(text=result, probability=None)

        if is_error_not_five_digit_string(result):
            raise HTTPException(status_code=400, detail="辨識失敗")

        return APIResponse(success=True, message="OCR辨識成功", data=response_data.dict())

    # except HTTPException:
    #     raise
    except Exception as e:
        return APIResponse(success=False, message=f"OCR辨識失敗: {str(e)}")

def is_error_not_five_digit_string(result_string):
    """
    檢查字串結果是否為錯誤（非五位數字字串）。
    如果不是五位數字字串，返回 True (表示錯誤)；否則返回 False (表示正確)。
    """
    # 確保輸入確實是字串
    if not isinstance(result_string, str):
        return True # 如果不是字串，直接視為錯誤

    # 檢查長度是否為5 並且 所有字元是否都是數字
    if len(result_string) == 5 and result_string.isdigit():
        return False # 它是五位數字字串，所以不是錯誤
    else:
        return True # 不是五位數字字串，所以是錯誤