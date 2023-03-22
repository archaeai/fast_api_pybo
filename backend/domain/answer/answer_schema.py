from pydantic import BaseModel, validator
import datetime
from domain.user.user_schema import User

class AnswerCreate(BaseModel):
    content:str 
    
    #  스키마에 이녀석의 기능은 content값이 저장될떄마다 실행되는데
    # 값이 없으면 not_empty함수를 실행하도록 설정했다. 
    @validator('content')
    def not_empty(cls,v):
        if not v or not v.strip():
            raise ValueError('빈값은 허용되지 않습니다.')
        return v
    
    # http프로토콜의 url에 포함된 입력 값은 라우터의 스키마가 아닌 매개변수로 읽는다
    # http 프로토콜의 body에 포함된 입력값은 pydantic 스키마로 읽는다. 
    # 답변등록 api 는 post방식이고 content라는 입력 항목이 있다. 답변등록 라우터에서 content의 값을 읽기 위해서는 반드시 content 항목을 포함하는 pydantic스키마를 통해 일겅야 한다. 스키마를 사용하지 않고 
    # 라우터의 함수의 매개변수에 content : str을 추가하여 그값을 읽을 수는 없다. 왜냐하면 get이 아닌다른 방식의 입력값은 pydantic스키마로만 읽을 수 있기 때문이다. 
    
class Answer(BaseModel):
    id:int
    content:str
    create_date:datetime.datetime
    user: User | None
    question_id: int
    modify_date: datetime.datetime | None = None
    voter: list[User] = []
    
    class Config:
        orm_mode = True
        
class AnswerUpdate(AnswerCreate):
    answer_id: int
    
class AnswerDelete(BaseModel):
    answer_id: int
    
class AnswerVote(BaseModel):
    answer_id: int
    