from pydantic import BaseModel

class UploadResponse(BaseModel):
    filename : str
    rows : int
    columns : int
    column_names : list[str]
    status : str