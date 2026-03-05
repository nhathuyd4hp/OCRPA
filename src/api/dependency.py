from fastapi import Request
from paddleocr._pipelines.ocr import PaddleOCR


def get_model(request: Request) -> PaddleOCR:
    return request.app.state.model
