import shutil
import tempfile
from pathlib import Path
from typing import List

import fitz
import paddle
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from paddleocr._pipelines.ocr import PaddleOCR
from paddlex.inference.pipelines.ocr.result import OCRResult

from src.api.common.response import TResponse
from src.api.dependency import get_model

router = APIRouter()


@router.get(
    path="/version",
    response_model=TResponse[str],
)
def get_version():
    return TResponse(data=paddle.__version__)


@router.post(
    path="/detect",
    response_model=TResponse,
)
async def detect(model: PaddleOCR = Depends(get_model), file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Chỉ chấp nhận định dạng PDF từ bản vẽ.")
    with tempfile.TemporaryDirectory() as temp_dir:
        filePath = Path(temp_dir) / file.filename
        with open(filePath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        with fitz.open(filePath) as doc:
            ocr = []
            for page_index in range(len(doc)):
                page = doc.load_page(page_index)
                pix = page.get_pixmap(dpi=300)
                img_path = Path(temp_dir) / f"page_{page_index + 1}.png"
                pix.save(img_path.as_posix())
                results: List[OCRResult] = model.predict(img_path.as_posix())
                for result in results:
                    # ----- Process
                    temp: dict = result._to_json()["res"]
                    ocr.append({page_index: temp["rec_texts"]})
            return TResponse(data=ocr)
