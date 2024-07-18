from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Train(Base):
    __tablename__ = 'trains'
    train_id = Column(String, primary_key=True)
    passenger_capacity = Column(Integer, nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Platform(Base):
    __tablename__ = 'platforms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(String, ForeignKey('stations.id'), nullable=False)
    passenger_capacity = Column(Integer, nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Station(Base):
    __tablename__ = 'stations'
    id = Column(String, primary_key=True)
    platforms = relationship('Platform', backref='station')

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Track(Base):
    __tablename__ = 'tracks'
    id = Column(String, primary_key=True)  # Removed autoincrement=True
    from_station_id = Column(String, ForeignKey('stations.id'), nullable=False)
    to_station_id = Column(String, ForeignKey('stations.id'), nullable=False)
    direction_code = Column(String, nullable=False)
    average_section_running_time = Column(Integer, nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Trip(Base):
    __tablename__ = 'trips'
    id = Column(Integer, primary_key=True, autoincrement=True)
    train_id = Column(String, nullable=False)
    origin_station_id = Column(String, nullable=False)
    destination_station_id = Column(String, nullable=False)
    length = Column(Integer, nullable=False)
    num_passengers = Column(Integer, nullable=False)
    srt = Column(Integer, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    delay = Column(Integer, nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
