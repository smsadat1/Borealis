from sqlmodel import Field, SQLModel


class History(SQLModel, table=True):

    __tablename__ = "history"

    id: int | None = Field(default=None, primary_key=True)
    api_key: str = Field(default=None, foreign_key='user.api_key')
    exec_id: str = Field(nullable=True, unique=True)
    language: str = Field(nullable=True)
    testcase: int = Field(nullable=True)
    status: str = Field(nullable=True)
    creation_time: str = Field(nullable=True)
    execution_time: str = Field(nullable=True)


class User(SQLModel, table=True):

    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    api_key: str = Field(index=True, nullable=False, unique=True)
    creation_time: str = Field(nullable=True)