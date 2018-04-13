import requests, json
from pprint import pprint
from base import DbManager
from entities import Driver, Person, Pilot, Planet, Starship, Vehicle
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from inspect import getmembers

SWAPI_API = 'https://swapi.co/api/{}/{}/'
db = DbManager()

def get_json_dict(url):
    if (url is None):
        return None
    print(url)
    resp = requests.get(url)
    if (resp is None or resp.text is None):
        return None
    return json.loads(resp.text)

def persist_driver(person, vehicle):
    if (person is None or vehicle is None):
        return
    try:
        db.open().query(Driver).filter(and_(Driver.person_id == person.id, Driver.vehicle_id == vehicle.id)).one()
        return
    except NoResultFound:
        pass
    except Exception as exp:
        print(exp)
        pass
    driver = Driver()
    driver.person = person
    driver.vehicle = vehicle
    print('persisting driver: {} ({}) : {} ({})'.format(person.name, person.id, vehicle.name, vehicle.id))
    try:
        db.save(driver)
    except Exception as exp:
        print(exp)

def persist_pilot(person, starship):
    if (person is None or starship is None):
        return
    try:
        db.open().query(Pilot).filter(and_(Pilot.person_id == person.id, Pilot.starship_id == starship.id)).one()
        return
    except NoResultFound:
        pass
    except Exception as exp:
        print(exp)
        pass
    pilot = Pilot()
    pilot.person = person
    pilot.starship = starship
    print('persisting pilot: {} ({}) : {} ({})'.format(person.name, person.id, starship.name, starship.id))
    try:
        db.save(pilot)
    except Exception as exp:
        print(exp)

def get_person(url):
    if (url is None or len(url) < 1):
        return None
    person = None
    try:
        person = db.open().query(Person).filter(Person.api_url == url).one()
    except NoResultFound:
        pass
    except Exception as exp:
        print(exp)
        pass
    if (person is None):
        json_dict = get_json_dict(url)
        if (json_dict is not None and 'url' in json_dict):
            person = Person()
            person.parse_dict(json_dict)
            try:
                db.save(person)
            except Exception as exp:
                print(exp)
            planet = get_planet(json_dict['homeworld'])
            if (planet is not None):
                person.planet = planet
                try:
                    db.save(person)
                except Exception as exp:
                    print(exp)
            for starship_url in json_dict['starships']:
                starship = get_starship(starship_url)
                persist_pilot(person, starship)
            for vehicle_url in json_dict['vehicles']:
                vehicle = get_vehicle(vehicle_url)
                persist_driver(person, vehicle)
    return person

def get_planet(url):
    if (url is None or len(url) < 1):
        return None
    planet = None
    try:
        planet = db.open().query(Planet).filter(Planet.api_url == url).one()
    except NoResultFound:
        pass
    except Exception as exp:
        print(exp)
        pass
    if (planet is None):
        json_dict = get_json_dict(url)
        if (json_dict is not None and 'url' in json_dict):
            planet = Planet()
            planet.parse_dict(json_dict)
            try:
                db.save(planet)
            except Exception as exp:
                print(exp)
            for person_url in json_dict['residents']:
                get_person(person_url)
    return planet

def get_starship(url):
    if (url is None or len(url) < 1):
        return None
    starship = None
    try:
        starship = db.open().query(Starship).filter(Starship.api_url == url).one()
    except NoResultFound:
        pass
    except Exception as exp:
        print(exp)
        pass
    if (starship is None):
        json_dict = get_json_dict(url)
        if (json_dict is not None and 'url' in json_dict):
            starship = Starship()
            starship.parse_dict(json_dict)
            try:
                db.save(starship)
            except Exception as exp:
                print(exp)
            for person_url in json_dict['pilots']:
                person = get_person(person_url)
                persist_pilot(person, starship)
    return starship

def get_vehicle(url):
    if (url is None or len(url) < 1):
        return None
    vehicle = None
    try:
        vehicle = db.open().query(Vehicle).filter(Vehicle.api_url == url).one()
    except NoResultFound:
        pass
    except Exception as exp:
        print(exp)
        pass
    if (vehicle is None):
        json_dict = get_json_dict(url)
        if (json_dict is not None and 'url' in json_dict):
            vehicle = Vehicle()
            vehicle.parse_dict(json_dict)
            try:
                db.save(vehicle)
            except Exception as exp:
                print(exp)
            for person_url in json_dict['pilots']:
                person = get_person(person_url)
                persist_driver(person, vehicle)
    return vehicle

def page_thru(enum_url, fn):
    while (True):
        res_dict = get_json_dict(enum_url)
        if (res_dict is not None and 'results' in res_dict):
            for json_dict in res_dict['results']:
                fn(json_dict['url'])
        if (res_dict is None or 'next' not in res_dict):
            break
        enum_url = res_dict['next']

page_thru('https://swapi.co/api/planets/', get_planet)
page_thru('https://swapi.co/api/starships/', get_starship)
page_thru('https://swapi.co/api/vehicles/', get_vehicle)

