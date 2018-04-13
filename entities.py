from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy import Column, DateTime, String, Float, Integer, ForeignKey, func
from base import Base, inverse_relationship, create_tables

class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key = True)
    api_url = Column(String, unique = True)
    name = Column(String)
    height = Column(String)
    mass = Column(String)
    birth_year = Column(String)

    planet_id = Column(Integer, ForeignKey('planets.id'))
    planet = relationship('Planet', backref = inverse_relationship('residents'))

    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, default = func.now(), onupdate = func.now())

    def parse_dictionary(self, json_data):
        self.api_url = json_data['url']
        self.name = json_data['name']
        self.height = json_data['height']
        self.mass = json_data['mass']
        self.birth_year = json_data['birth_year']

class Planet(Base):
    __tablename__ = 'planets'

    id = Column(Integer, primary_key = True)
    api_url = Column(String, unique = True)
    name = Column(String)
    climate = Column(String)
    gravity = Column(String)
    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, default = func.now(), onupdate = func.now())

    def parse_dictionary(self, json_data):
        self.api_url = json_data['url']
        self.name = json_data['name']
        self.climate = json_data['climate']
        self.gravity = json_data['gravity']

class Starship(Base):
    __tablename__ = 'starships'

    id = Column(Integer, primary_key = True)
    api_url = Column(String, unique = True)
    name = Column(String)
    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, default = func.now(), onupdate = func.now())

    def parse_dictionary(self, json_data):
        self.api_url = json_data['url']
        self.name = json_data['name']

class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key = True)
    api_url = Column(String, unique = True)
    name = Column(String)
    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, default = func.now(), onupdate = func.now())

    def parse_dictionary(self, json_data):
        self.api_url = json_data['url']
        self.name = json_data['name']    

class Pilot(Base):
    __tablename__ = 'pilots'

    id = Column(Integer, primary_key = True)

    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, default = func.now(), onupdate = func.now())

    starship_id = Column(Integer, ForeignKey('starships.id'))
    starship = relationship('Starship', backref = inverse_relationship('piloted_by'))
    person_id = Column(Integer, ForeignKey('people.id'))
    person = relationship('Person', backref = inverse_relationship('pilot_of'))

class Driver(Base):
    __tablename__ = 'drivers'

    id = Column(Integer, primary_key = True)

    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, default = func.now(), onupdate = func.now())

    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    vehicle = relationship('Vehicle', backref = inverse_relationship('driven_by'))
    person_id = Column(Integer, ForeignKey('people.id'))
    person = relationship('Person', backref = inverse_relationship('driver_of'))


if __name__ != '__main__':
    create_tables()