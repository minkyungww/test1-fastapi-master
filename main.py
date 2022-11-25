from databases import Database
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# https://apis.data.go.kr/6260000/AttractionService/getAttractionKr?serviceKey=L4O6Jd5locofQV0Sa674EwMQ4GyHi380DNlzkWVMQLw8O2LvzNMvBKe1RxTj4jssgmQKPrDvinJFtSOIs9KmbA%3D%3D&pageNo=1&numOfRows=10&resultType=json


class ResponseDTO(BaseModel):
    code: int
    message: str
    data: object | None


class Cat(BaseModel):
    name: str
    id: int = 0


class RequestInsertRegionDTO(BaseModel):
    regionName: str


class RequestUpdateRegionDTO(BaseModel):
    regionName: str
    # regionId: int


app = FastAPI()


origins = [
    "http://127.0.0.1:5500",  # liveserver은 5500번 포트를 씀
    "*",  # *은 모든 포트 가능
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database = Database("sqlite:///C:\programming\sqlite\hr")


@app.get("/first/{id}")
async def root(id: int):
    return {"message": "Hello World", "id": id}


@app.get("/second")
async def second(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


@app.post("/cat")
async def cat(cat: Cat):
    return cat


@app.get("/error")
async def error():
    dto = ResponseDTO(
        code=0,
        message="페이지가 없습니다.",
        data=None
    )
    return JSONResponse(status_code=404, content=jsonable_encoder(dto))


@app.get("/error1")
async def error1():
    raise HTTPException(status_code=404, detail={"message": "Item not found"})


@app.post("/files/")
async def check_file(
    uploadFile: UploadFile = File(), token: str = Form()
):
    return {
        "token": token,
        # "uploadFileSize": len(await upload_file.read()),
        "uploadFileName": uploadFile.filename,
        "uploadFileContentType": uploadFile.content_type,
    }


@app.get("/findall")
async def fetch_data():

    await database.connect()  # await는 연결할 때까지 기다리겠다는 뜻

    query = "SELECT * FROM REGIONS"
    results = await database.fetch_all(query=query)  # fetch는 데이터를 가져오겠다느 뜻

    await database.disconnect()  # 데이터베이스 다 쓰고 나면 disconnect를 해줘야 함

    return results


@app.post("/insert")
async def fetch_data(requestInsertRegionDTO: RequestInsertRegionDTO):

    await database.connect()

    error = False

    try:
        query = f"""INSERT INTO REGIONS
                      (region_name)
                    values
                      ('{requestInsertRegionDTO.regionName}')"""
        results = await database.execute(query)
    except:
        error = True
    finally:
        await database.disconnect()

    if (error):
        return "에러발생"

    return results


@app.put("/update/{id}")
# RequestUpdateRegionDTO 추가하기
async def update_data(id: int, requestUpdateRegionDTO: RequestUpdateRegionDTO):

    await database.connect()

    error = False

    try:
        query = f"UPDATE REGIONS SET REGION_NAME =('{requestUpdateRegionDTO.regionName}') WHERE REGION_ID =({id})"

        results = await database.execute(query)
    except:
        error = True
    finally:
        await database.disconnect()

    if (error):
        return "에러발생"

    return results


@app.delete("/delete/{id}")
async def update_data(id: int):

    await database.connect()

    error = False

    try:
        query = f"DELETE FROM REGIONS WHERE REGION_ID IN ({id})"

        results = await database.execute(query)
    except:
        error = True
    finally:
        await database.disconnect()

    if (error):
        return "에러발생"

    return results  # delete의 result는 1일 나와야 정상

@app.post("/files-base64/")
async def bas64_file(
    uploadFile: str = Form(), token: str = Form()
):
    
    
    
    # print(uploadFile)
    return {
        "token": token,
        "uploadFile": uploadFile
    }