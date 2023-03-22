from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from database import get_db
from domain.question import question_schema, question_crud
from domain.user.user_router import get_current_user
from models import User

# 이 라우터 객체를 생성해서 등록해야만 사용할 수 있다. 
# 라우팅이란 fastapi가 요청받은 url을 해석하여 그에 맞는 함ㄴ수를 실행하여 그 결과를 리턴하는 행위를 말한다. 
router = APIRouter(
    prefix="/api/question",
)

# db 세션을 생성하고 해당 세션을 이요하여 질문 목록을 조회함여 리턴하는 함수이다. 그리고 사용한 세션은 db.close를수행하여 사용한세션을 반환했다. 
# 시선이 가면 속도가 줄어들고 정확도가 하향한다. 
@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10, keyword: str = ''):
    total, _question_list = question_crud.get_question_list(
        db, skip=page * size, limit=size, keyword=keyword)
    return {
        'total': total,
        'question_list': _question_list
    }


# def question_list():
#     with get_db() as db:
#         _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
#     return _question_list


#{question_id}이거랑, question_detail에 들어가는 변수 question_id 이름이 같아야 오류가 안생긴다. 
@router.get("/detail/{question_id}",response_model=question_schema.Question)
def question_detail(question_id:int,db: Session = Depends(get_db)):
    question = question_crud.get_question(db,question_id = question_id)
    return question

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    question_crud.create_question(db=db, question_create=_question_create,
                                  user=current_user)
    
    
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_update: question_schema.QuestionUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_update.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    question_crud.update_question(db=db, db_question=db_question,
                                  question_update=_question_update)
            
            
@router.delete("/delete",status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete,
                    db: Session = Depends(get_db),
                    current_user : User = Depends(get_current_user)):
    db_question = question_crud.get_question(db,question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='삭제권한이 없습니다.')
    question_crud.delete_question(db=db,db_question=db_question)
    
    
@router.post("/vote",status_code=status.HTTP_204_NO_CONTENT)
def question_vote(_question_vote: question_schema.QuestionVote,
                  db: Session=Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db,question_id = _question_vote.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='데이터를 찾을 수 없습니다')
    question_crud.vote_question(db,db_question=db_question,db_user=current_user)