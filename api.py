from entities import Person, Planet, Starship, Vehicle, Pilot, Driver
from base import DbManager
import requests, json 
from pprint import pprint

SWAPI_API = 'https://swapi.co/api/{}/{}/'
db = DbManager()

def get_json(url):
    print(url)
    response = requests.get(url)
    return json.loads(response.text)

def get_person(url):
    person = None
    try:
        person = db.open().query(Person).filter(Person.api_url == url).one()
    except:
        person = Person()
        json_data = get_json(url)
        person.parse_dictionary(json_data)
        db.save(person)

        for starship_url in json_data['starships']:
            starship = get_starship(starship_url)
            pilot = Pilot()
            pilot.person = person
            pilot.starship = starship
            db.save(pilot)

        for vehicle_url in json_data['vehicles']:
            vehicle = get_vehicle(vehicle_url)
            driver = Driver()
            driver.person = person
            driver.vehicle = vehicle
            db.save(driver)

    return person

def get_planet(url):
    planet = None
    try:
        planet = db.open().query(Planet).filter(Planet.api_url == url).one()
    except:
        planet = Planet()
        json_data = get_json(url)
        planet.parse_dictionary(json_data)
        db.save(planet)

        for person_url in json_data['residents']:
            person = get_person(person_url)
            person.planet = planet
            db.save(person)

    return planet

def get_starship(url):
    starship = None
    try:
        starship = db.open().query(Starship).filter(Starship.api_url == url).one()
    except:
        starship = Starship()
        json_data = get_json(url)
        starship.parse_dictionary(json_data)
        db.save(starship)
    return starship

def get_vehicle(url):
    vehicle = None
    try:
        vehicle = db.open().query(Vehicle).filter(Vehicle.api_url == url).one()
    except:
        vehicle = Vehicle()
        json_data = get_json(url)
        vehicle.parse_dictionary(json_data)
        db.save(vehicle)
    return vehicle


for planet in range(1,62):
    try:
        get_planet(SWAPI_API.format('planets', planet))
    except:
        print('Oops, no planet {}'.format(planet))