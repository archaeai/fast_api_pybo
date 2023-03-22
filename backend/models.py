from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base


# table만드는 2가지 방식중에 하나인데, class 선언해서, 다대다 만들때는 back_poppulate?를 사용한다. gpt참고 
question_voter=Table(
    'question_voter',
    Base.metadata,
    Column('user_id',Integer,ForeignKey('user.id'),primary_key=True),
    Column('question_id',Integer,ForeignKey('question.id'),primary_key=True)
    # 이렇게 프라이머리키를 두개를 가지게 되면, 둘다 동시에 중복이 되지만 않으면 괜찮은 것일까?
)

answer_voter=Table(
    'answer_voter',
    Base.metadata,
    Column('user_id',Integer,ForeignKey('user.id'),primary_key=True),
    Column('answer_id',Integer,ForeignKey('answer.id'),primary_key=True)
)


class Question(Base):
    __tablename__="question"
    #  primary 키는 지정하지 않아도 auto increse 자동 내포 되어있음
    id = Column(Integer,primary_key=True)
    subject = Column(String,nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime,nullable=False)
    user_id = Column(Integer,ForeignKey("user.id"), nullable=True)
    user = relationship("User",backref="question_users")
    modify_date = Column(DateTime,nullable=True)
    voter = relationship('User',secondary=question_voter,backref='question_voters')


class Answer(Base):
    __tablename__="answer"
    id = Column(Integer,primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime,nullable=False)
    # 여기서 question.id 의 question은 테이블명을 의미한다.
    question_id = Column(Integer,ForeignKey("question.id"))
    # 이렇게 relationship으로 참조를 하면 answer.question.subject 이런식으로 참조할 수 있다. 
    # backref는 역참조인데, 어떤 a_question에 대해서 a_question.answers 이런식으로 그 질문에 달린 여러가지 답을 참조할 수 있다. 
    question = relationship("Question", backref="answers")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="answer_users")
    modify_date = Column(DateTime,nullable=True)
    voter = relationship('User',secondary=answer_voter,backref='answer_voters')

    
class User(Base):
    __tablename__="user"
    
    id = Column(Integer,primary_key=True)
    username = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    
    
