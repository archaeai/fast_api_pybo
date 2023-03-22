from pydantic import BaseModel, validator, EmailStr

class UserCreate(BaseModel):
    username: str
    password1: str
    password2: str
    email: EmailStr
    
    @validator('username','password1','password2','email')
    def not_empty(cls,v):
        if not v or not v.strip():
            raise ValueError('빈폴은 허용하지 않습니다')
        return v 
# cls는 데코레이터 첫번쨰 인ㅇ자로 선언되어 있기 때문에 해당함수에서 반드시 선언되어 있어야함. 
    @validator('password2')
    def passwords_match(cls,v,values):
        if 'password1' in values and v !=values['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v

class Token(BaseModel):
    access_token : str
    token_type : str
    username : str
    
class User(BaseModel):
    id: int
    username:str
    email:str
    
    class Config:
        orm_mode =True