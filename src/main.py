from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from paddleocr import PaddleOCR

from src.api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    ocr = PaddleOCR(
        lang="japan",
        ocr_version="PP-OCRv3",
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
    )
    app.state.model = ocr
    yield
    pass


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)


@app.get("/")
def upload_page(request: Request):
    return Jinja2Templates(directory="templates").TemplateResponse("ocr.html", {"request": request})


app.include_router(router)


# Handle Undefined API
@app.api_route(
    path="/{path:path}",
    methods=["GET", "POST"],
    include_in_schema=False,
)
def undefined(path: str, request: Request):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"{request.method} {request.url.path} is undefined"
    )
