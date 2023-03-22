import datetime
from pydantic import BaseModel, validator
from domain.answer.answer_schema import Answer
from domain.user.user_schema import User

# 스키마를 설정하기 떄라서 테이블에서 원하는 값만 보여줄 수 있다. 
class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date:datetime.datetime
    answers: list[Answer] = []
    user:User | None
    modify_date: datetime.datetime | None =None
    voter: list[User]= []
    
    
    class Config:
        orm_mode=True
        
class QuestionCreate(BaseModel):
    subject:str
    content:str
    
    
    @validator('subject','content')
    def not_empty(cls,v):
        if not v or not v.strip():
            raise ValueError('None is Fuck')
        return v
    
# subject: str | None = None
# 위 코드의 의미는 subject 항목은 문자열 또는 None을 가질 수 있고 디폴트 값은 None이라는 뜻이다.

class QuestionList(BaseModel):
    total: int=0
    question_list:list[Question] = []
    
# QuestionCreate에 이미 있는 항목을 상속했기떄문에, question_id만 추가하면 된다. 
class QuestionUpdate(QuestionCreate):
    question_id: int
    
class QuestionDelete(BaseModel):
    question_id:int
    

class QuestionVote(BaseModel):
    question_id: int
    
    