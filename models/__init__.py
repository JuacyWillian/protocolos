import datetime
from os.path import isfile
from sqlite3 import *
from time import sleep


DATABASE_NAME = "storage.db"


def convertToDateTime(value):
    new_value = value.replace(' ', ':').replace('-', ':').replace('T', ':')\
        .split('.')[0]
    return datetime.datetime(*[int(i) for i in new_value.split(':')])


class Protocolo():

    __id = None
    number = None
    __start = None
    __end = None
    reason = None

    def __init__(self, number, start, end, reason, ):
        self.number = number
        self.start = start
        self.end = end
        self.reason = reason

    def __repr__(self, ):
        return f'<Protocolo (number={self.number}, start={self.start})'

    @property
    def start(self, ):
        return self.__start

    @start.setter
    def start(self, v):
        if isinstance(v, str):
            v = convertToDateTime(v)
        self.__start = v

    @property
    def end(self, ):
        return self.__end

    @end.setter
    def end(self, v):
        if isinstance(v, str):
            v = convertToDateTime(v)
        self.__end = v

    @property
    def id(self, ):
        return self.__id

    @staticmethod
    def getAll():
        sql = """
            SELECT * 
            FROM protocolos
            ORDER BY start DESC
            """
        protocolos = []

        with connect(DATABASE_NAME) as db:
            for row in db.execute(sql):
                protocolos.append(Protocolo(*row[1:]))
        return protocolos

    @staticmethod
    def getByNumber(number: str):
        sql = """
            SELECT * FROM protocolos
            WHERE number=?
            """
        with connect(DATABASE_NAME) as db:
            result = db.execute(sql, (number,))
            return Protocolo(*result.fetchone()[1:])

    def update(self, ):
        sql = """
            UPDATE protocolos SET start=?, end=?, reason=? 
            WHERE number=?
            """
        with connect(DATABASE_NAME) as db:
            db.execute(sql, (self.start, self.end, self.reason, self.number))
            db.commit()

    def remove(self, ):
        sql = """
            DELETE FROM protocolos 
            WHERE number=?
            """
        with connect(DATABASE_NAME) as db:
            db.execute(sql, (self.number,))
            db.commit()

    def insert(self, ):
        sql = """
            INSERT INTO protocolos (number, start, end, reason) 
            VALUES (?, ?, ?, ?)
            """
        with connect(DATABASE_NAME) as db:
            db.execute(sql, (self.number, self.start, self.end, self.reason))
            db.commit()


def create_db():
    with connect(DATABASE_NAME) as db:
        db.execute("""
            CREATE TABLE protocolos(
                id integer primary key autoincrement,
                number varchar(32) unique,
                start datetime,
                end datetime,
                reason varchar)
            """)
        db.commit()


if not isfile(DATABASE_NAME):
    create_db()
