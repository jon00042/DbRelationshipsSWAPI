from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy import Column, DateTime, String, Float, Integer, ForeignKey, func
from base import Base, inverse_relationship, create_tables

class Person(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True)
    api_url = Column(String, unique=True)
    name = Column(String)
    height = Column(String)
    mass = Column(String)
    birth_year = Column(String)
    planet_id = Column(Integer, ForeignKey('planets.id'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    planet = relationship('Planet', backref=inverse_relationship('residents'))

    def parse_dict(self, dict):
        self.api_url = dict['url']
        self.name = dict['name']
        self.height = dict['height']
        self.mass = dict['mass']
        self.birth_year = dict['birth_year']

class Planet(Base):
    __tablename__ = "planets"
    id = Column(Integer, primary_key=True)
    api_url = Column(String, unique=True)
    name = Column(String)
    climate = Column(String)
    gravity = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def parse_dict(self, dict):
        self.api_url = dict['url']
        self.name = dict['name']
        self.climate = dict['climate']
        self.gravity = dict['gravity']

class Starship(Base):
    __tablename__ = 'starships'
    id = Column(Integer, primary_key=True)
    api_url = Column(String, unique=True)
    name = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def parse_dict(self, dict):
        self.api_url = dict['url']
        self.name = dict['name']

class Pilot(Base):
    __tablename__ = 'pilots'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('people.id'))
    starship_id = Column(Integer, ForeignKey('starships.id'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    person = relationship('Person', backref=inverse_relationship('pilot_of'))
    starship = relationship('Starship', backref=inverse_relationship('piloted_by'))

class Vehicle(Base):
    __tablename__ = 'vehicles'
    id = Column(Integer, primary_key=True)
    api_url = Column(String, unique=True)
    name = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def parse_dict(self, dict):
        self.api_url = dict['url']
        self.name = dict['name']

class Driver(Base):
    __tablename__ = 'drivers'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('people.id'))
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    person = relationship('Person', backref=inverse_relationship('driver_of'))
    vehicle = relationship('Vehicle', backref=inverse_relationship('driven_by'))

if __name__ != '__main__':
    create_tables()

