from models import Question, Answer
from datetime import datetime

# insert하는 양식 
q = Question(subject='pybo가 무엇인가요?', content='pybo에 대해서 알고 싶습니다.', create_date=datetime.now())

from database import SessionLocal

# db에 저장 
db = SessionLocal()
db.add(q)

# 여기서부터 roll back 안된다. 
db.commit()
