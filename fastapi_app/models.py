from pydantic import BaseModel


class RegionsOfInterestItem(BaseModel):
    x: int
    y: int
    width: int
    height: int


class Coordinate(BaseModel):
    x: int
    y: int


class Candidate(BaseModel):
    plate: str
    confidence: float
    matches_template: bool


class Result(BaseModel):
    plate: str
    confidence: float
    matches_template: bool
    plate_index: int
    region: str
    region_confidence: float
    processing_time_ms: float
    requested_topn: int
    coordinates: list[Coordinate]
    candidates: list[Candidate]


class RequestResponse(BaseModel):
    version: int
    data_type: str
    epoch_time: int
    img_width: int
    img_height: int
    processing_time_ms: float
    regions_of_interest: list[RegionsOfInterestItem]
    results: list[Result]
