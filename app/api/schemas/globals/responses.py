from pydantic import BaseModel


class APIResponse(BaseModel):

    success: bool
    message: str
    payload: dict | None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Test Success",
                "payload": {}
            }
        }
        



class Error404(BaseModel):
    code: str
    detail: str 
    class Config:
        json_schema_extra = {
            "example": {
                "code": 404,
                "detail": "Not Found"
            }
        }


class Error500(BaseModel):
    code: str
    detail: str 
    class Config:
        json_schema_extra = {
            "example": {
                "code": 500,
                "detail": "Internal Server Error"
            }
        }




class APIResponseError(APIResponse):
    
    payload: Error404 | Error500
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "message": "Error",
                "payload": {
                    "code": 404,
                    "detail": "Not Found"
                }
            },
            "example": {
                "success": False,
                "message": "Error",
                "payload": {
                    "code": 500,
                    "detail": "Internal Server Error"
                }
            }
        }