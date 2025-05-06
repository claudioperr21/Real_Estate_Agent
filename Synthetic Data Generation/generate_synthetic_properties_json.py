import csv
import json
import random
import datetime
from faker import Faker

fake = Faker("en_US")

def random_date(start_year=1990, end_year=2023):
    """Generate a random ISO 8601 date between start_year and end_year."""
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    delta = (end - start).days
    rand_days = random.randint(0, delta)
    return (start + datetime.timedelta(days=rand_days)).isoformat() + "T00:00:00.000Z"

def random_bool():
    return random.choice([True, False])

# ----------------------------------------------------------------------------
# CLEANED CITY_DATA (REMOVED DUPLICATES / FIXED COMMAS)
# ----------------------------------------------------------------------------
CITY_DATA = [
    # Example / partial from your big list:
    {
        "zip": "07030",
        "city": "Hoboken",
        "state": "New Jersey",
        "lat_min": 40.73, "lat_max": 40.75,
        "lon_min": -74.04, "lon_max": -74.02
    },
    {
        "zip": "60607",
        "city": "Chicago",
        "state": "Illinois",
        "lat_min": 41.86, "lat_max": 41.88,
        "lon_min": -87.66, "lon_max": -87.62
    },
    {
        "zip": "10003",
        "city": "New York",
        "state": "New York",
        "lat_min": 40.71, "lat_max": 40.74,
        "lon_min": -73.99, "lon_max": -73.98
    },
    {
        "zip": "60614",
        "city": "Chicago",
        "state": "Illinois",
        "lat_min": 41.91, "lat_max": 41.93,
        "lon_min": -87.66, "lon_max": -87.63
    },
    {
        "zip": "53202",
        "city": "Milwaukee",
        "state": "Wisconsin",
        "lat_min": 43.04, "lat_max": 43.07,
        "lon_min": -87.91, "lon_max": -87.89
    },
    {
        "zip": "80203",
        "city": "Denver",
        "state": "Colorado",
        "lat_min": 39.72, "lat_max": 39.74,
        "lon_min": -104.99, "lon_max": -104.98
    },
    {
        "zip": "60657",
        "city": "Chicago",
        "state": "Illinois",
        "lat_min": 41.93, "lat_max": 41.95,
        "lon_min": -87.66, "lon_max": -87.64
    },
    {
        "zip": "10011",
        "city": "New York",
        "state": "New York",
        "lat_min": 40.73, "lat_max": 40.75,
        "lon_min": -74.00, "lon_max": -73.99
    },
    {
        "zip": "10014",
        "city": "New York",
        "state": "New York",
        "lat_min": 40.72, "lat_max": 40.74,
        "lon_min": -74.01, "lon_max": -73.99
    },
    {
        "zip": "92101",
        "city": "San Diego",
        "state": "California",
        "lat_min": 32.71, "lat_max": 32.73,
        "lon_min": -117.18, "lon_max": -117.15
    },
    {
        "zip": "94702",
        "city": "Berkeley",
        "state": "California",
        "lat_min": 37.85, "lat_max": 37.88,
        "lon_min": -122.30, "lon_max": -122.26
    },
    {
        "zip": "90026",
        "city": "Los Angeles",
        "state": "California",
        "lat_min": 34.06, "lat_max": 34.07,
        "lon_min": -118.27, "lon_max": -118.24
    },
    {
        "zip": "98115",
        "city": "Seattle",
        "state": "Washington",
        "lat_min": 47.67, "lat_max": 47.69,
        "lon_min": -122.30, "lon_max": -122.27
    },
    {
        "zip": "20002",
        "city": "Washington",
        "state": "DC",
        "lat_min": 38.89, "lat_max": 38.92,
        "lon_min": -76.99, "lon_max": -76.94
    },
    {
        "zip": "94601",
        "city": "Oakland",
        "state": "California",
        "lat_min": 37.76, "lat_max": 37.78,
        "lon_min": -122.21, "lon_max": -122.19
    },
    {
        "zip": "07104",
        "city": "Newark",
        "state": "New Jersey",
        "lat_min": 40.76, "lat_max": 40.78,
        "lon_min": -74.18, "lon_max": -74.15
    },
    {
        "zip": "20782",
        "city": "Hyattsville",
        "state": "Maryland",
        "lat_min": 38.95, "lat_max": 38.97,
        "lon_min": -76.96, "lon_max": -76.93
    },
    {
        "zip": "90014",
        "city": "Los Angeles",
        "state": "California",
        "lat_min": 34.03, "lat_max": 34.05,
        "lon_min": -118.26, "lon_max": -118.24
    },
    {
        "zip": "20001",
        "city": "Washington",
        "state": "DC",
        "lat_min": 38.90, "lat_max": 38.92,
        "lon_min": -77.02, "lon_max": -77.00
    },
    {
        "zip": "77003",
        "city": "Houston",
        "state": "Texas",
        "lat_min": 29.74, "lat_max": 29.76,
        "lon_min": -95.35, "lon_max": -95.33
    },
    {
        "zip": "19123",
        "city": "Philadelphia",
        "state": "Pennsylvania",
        "lat_min": 39.96, "lat_max": 39.98,
        "lon_min": -75.15, "lon_max": -75.13
    },
    {
        "zip": "10039",
        "city": "Manhattan",
        "state": "New York",
        "lat_min": 40.82, "lat_max": 40.83,
        "lon_min": -73.94, "lon_max": -73.93
    },
    {
        "zip": "76102",
        "city": "Fort Worth",
        "state": "Texas",
        "lat_min": 32.74, "lat_max": 32.76,
        "lon_min": -97.33, "lon_max": -97.31
    },
    {
        "zip": "11211",
        "city": "Brooklyn",
        "state": "New York",
        "lat_min": 40.71, "lat_max": 40.73,
        "lon_min": -73.96, "lon_max": -73.94
    },
    {
        "zip": "19146",
        "city": "Philadelphia",
        "state": "Pennsylvania",
        "lat_min": 39.93, "lat_max": 39.94,
        "lon_min": -75.19, "lon_max": -75.17
    },
    {
        "zip": "11222",
        "city": "Brooklyn",
        "state": "New York",
        "lat_min": 40.72, "lat_max": 40.73,
        "lon_min": -73.95, "lon_max": -73.93
    },
    {
        "zip": "11216",
        "city": "Brooklyn",
        "state": "New York",
        "lat_min": 40.67, "lat_max": 40.68,
        "lon_min": -73.95, "lon_max": -73.94
    },
    {
        "zip": "63103",
        "city": "St. Louis",
        "state": "Missouri",
        "lat_min": 38.63, "lat_max": 38.64,
        "lon_min": -90.21, "lon_max": -90.20
    },
    {
        "zip": "90013",
        "city": "Los Angeles",
        "state": "California",
        "lat_min": 34.04, "lat_max": 34.05,
        "lon_min": -118.25, "lon_max": -118.23
    },
    {
        "zip": "78702",
        "city": "Austin",
        "state": "Texas",
        "lat_min": 30.25, "lat_max": 30.27,
        "lon_min": -97.72, "lon_max": -97.70
    },
    {
        "zip": "11237",
        "city": "Brooklyn",
        "state": "New York",
        "lat_min": 40.70, "lat_max": 40.71,
        "lon_min": -73.92, "lon_max": -73.90
    },
    {
        "zip": "10026",
        "city": "Manhattan",
        "state": "New York",
        "lat_min": 40.80, "lat_max": 40.81,
        "lon_min": -73.95, "lon_max": -73.94
    },
    {
        "zip": "21224",
        "city": "Baltimore",
        "state": "Maryland",
        "lat_min": 39.29, "lat_max": 39.30,
        "lon_min": -76.56, "lon_max": -76.54
    },
    {
        "zip": "11221",
        "city": "Brooklyn",
        "state": "New York",
        "lat_min": 40.68, "lat_max": 40.69,
        "lon_min": -73.93, "lon_max": -73.92
    },
    {
        "zip": "20010",
        "city": "Washington",
        "state": "DC",
        "lat_min": 38.93, "lat_max": 38.94,
        "lon_min": -77.04, "lon_max": -77.03
    },
    {
        "zip": "77007",
        "city": "Houston",
        "state": "Texas",
        "lat_min": 29.77, "lat_max": 29.78,
        "lon_min": -95.42, "lon_max": -95.40
    },
    {
        "zip": "98402",
        "city": "Tacoma",
        "state": "Washington",
        "lat_min": 47.24, "lat_max": 47.26,
        "lon_min": -122.45, "lon_max": -122.43
    },
    {
        "zip": "37408",
        "city": "Chattanooga",
        "state": "Tennessee",
        "lat_min": 35.02, "lat_max": 35.04,
        "lon_min": -85.31, "lon_max": -85.29
    },
    {
        "zip": "11205",
        "city": "Brooklyn",
        "state": "New York",
        "lat_min": 40.68, "lat_max": 40.70,
        "lon_min": -73.97, "lon_max": -73.95
    },
    {
        "zip": "11206",
        "city": "Brooklyn",
        "state": "New York",
        "lat_min": 40.69, "lat_max": 40.71,
        "lon_min": -73.95, "lon_max": -73.92
    },
    {
        "zip": "73104",
        "city": "Oklahoma City",
        "state": "Oklahoma",
        "lat_min": 35.47, "lat_max": 35.49,
        "lon_min": -97.50, "lon_max": -97.47
    },
    {
        "zip": "30317",
        "city": "Atlanta",
        "state": "Georgia",
        "lat_min": 33.74, "lat_max": 33.76,
        "lon_min": -84.32, "lon_max": -84.30
    },
    {
        "zip": "80205",
        "city": "Denver",
        "state": "Colorado",
        "lat_min": 39.75, "lat_max": 39.77,
        "lon_min": -104.98, "lon_max": -104.95
    },
    {
        "zip": "29492",
        "city": "Charleston",
        "state": "South Carolina",
        "lat_min": 32.90, "lat_max": 32.92,
        "lon_min": -79.90, "lon_max": -79.88
    },
    {
        "zip": "33602",
        "city": "Tampa",
        "state": "Florida",
        "lat_min": 27.94, "lat_max": 27.96,
        "lon_min": -82.46, "lon_max": -82.44
    },
    {
        "zip": "55101",
        "city": "St. Paul",
        "state": "Minnesota",
        "lat_min": 44.93, "lat_max": 44.95,
        "lon_min": -93.08, "lon_max": -93.06
    },
    {
        "zip": "37403",
        "city": "Chattanooga",
        "state": "Tennessee",
        "lat_min": 35.03, "lat_max": 35.04,
        "lon_min": -85.29, "lon_max": -85.27
    },
    {
        "zip": "11238",
        "city": "Brooklyn",
        "state": "New York",
        "lat_min": 40.68, "lat_max": 40.69,
        "lon_min": -73.96, "lon_max": -73.94
    },
    {
        "zip": "20005",
        "city": "Washington",
        "state": "DC",
        "lat_min": 38.90, "lat_max": 38.91,
        "lon_min": -77.03, "lon_max": -77.02
    },
    {
        "zip": "63101",
        "city": "St. Louis",
        "state": "Missouri",
        "lat_min": 38.62, "lat_max": 38.63,
        "lon_min": -90.20, "lon_max": -90.19
    },
    {
        "zip": "92113",
        "city": "San Diego",
        "state": "California",
        "lat_min": 32.68, "lat_max": 32.70,
        "lon_min": -117.13, "lon_max": -117.10
    },
    {
        "zip": "97227",
        "city": "Portland",
        "state": "Oregon",
        "lat_min": 45.54, "lat_max": 45.56,
        "lon_min": -122.67, "lon_max": -122.65
    },
    {
        "zip": "78208",
        "city": "San Antonio",
        "state": "Texas",
        "lat_min": 29.43, "lat_max": 29.45,
        "lon_min": -98.45, "lon_max": -98.43
    },
    {
        "zip": "10031",
        "city": "Manhattan",
        "state": "New York",
        "lat_min": 40.82, "lat_max": 40.83,
        "lon_min": -73.95, "lon_max": -73.93
    },
    {
        "zip": "33620",
        "city": "Tampa",
        "state": "Florida",
        "lat_min": 28.05, "lat_max": 28.06,
        "lon_min": -82.42, "lon_max": -82.41
    },
    {
        "zip": "28202",
        "city": "Charlotte",
        "state": "North Carolina",
        "lat_min": 35.22, "lat_max": 35.24,
        "lon_min": -80.85, "lon_max": -80.84
    },
    {
        "zip": "46204",
        "city": "Indianapolis",
        "state": "Indiana",
        "lat_min": 39.76, "lat_max": 39.77,
        "lon_min": -86.16, "lon_max": -86.15
    },
    {
        "zip": "70115",
        "city": "New Orleans",
        "state": "Louisiana",
        "lat_min": 29.91, "lat_max": 29.92,
        "lon_min": -90.10, "lon_max": -90.09
    },
    {
        "zip": "93650",
        "city": "Fresno",
        "state": "California",
        "lat_min": 36.82, "lat_max": 36.83,
        "lon_min": -119.79, "lon_max": -119.78
    },
    {
        "zip": "80207",
        "city": "Denver",
        "state": "Colorado",
        "lat_min": 39.75, "lat_max": 39.76,
        "lon_min": -104.92, "lon_max": -104.90
    },
    {
        "zip": "31401",
        "city": "Savannah",
        "state": "Georgia",
        "lat_min": 32.07, "lat_max": 32.09,
        "lon_min": -81.10, "lon_max": -81.08
    },
    {
        "zip": "70112",
        "city": "New Orleans",
        "state": "Louisiana",
        "lat_min": 29.95, "lat_max": 29.96,
        "lon_min": -90.08, "lon_max": -90.07
    },
    {
        "zip": "19122",
        "city": "Philadelphia",
        "state": "Pennsylvania",
        "lat_min": 39.98, "lat_max": 40.00,
        "lon_min": -75.15, "lon_max": -75.13
    },
    {
        "zip": "78721",
        "city": "Austin",
        "state": "Texas",
        "lat_min": 30.26, "lat_max": 30.28,
        "lon_min": -97.68, "lon_max": -97.66
    },
    {
        "zip": "97211",
        "city": "Portland",
        "state": "Oregon",
        "lat_min": 45.57, "lat_max": 45.59,
        "lon_min": -122.67, "lon_max": -122.64
    },
    {
        "zip": "19146",
        "city": "Philadelphia",
        "state": "Pennsylvania",
        "lat_min": 39.93, "lat_max": 39.94,
        "lon_min": -75.19, "lon_max": -75.17
    },
    {
        "zip": "23219",
        "city": "Richmond",
        "state": "Virginia",
        "lat_min": 37.54, "lat_max": 37.55,
        "lon_min": -77.44, "lon_max": -77.43
    },
    {
        "zip": "28801",
        "city": "Asheville",
        "state": "North Carolina",
        "lat_min": 35.59, "lat_max": 35.60,
        "lon_min": -82.56, "lon_max": -82.55
    },
    {
        "zip": "20003",
        "city": "Washington",
        "state": "DC",
        "lat_min": 38.87, "lat_max": 38.88,
        "lon_min": -76.99, "lon_max": -76.97
    },
    {
        "zip": "91204",
        "city": "Glendale",
        "state": "California",
        "lat_min": 34.13, "lat_max": 34.14,
        "lon_min": -118.26, "lon_max": -118.25
    },
    {
        "zip": "30316",
        "city": "Atlanta",
        "state": "Georgia",
        "lat_min": 33.72, "lat_max": 33.74,
        "lon_min": -84.34, "lon_max": -84.31
    },
    {
        "zip": "23459",
        "city": "Virginia Beach",
        "state": "Virginia",
        "lat_min": 36.90,
        "lat_max": 36.92,
        "lon_min": -76.01,
        "lon_max": -75.99
    },
    {
        "zip": "10026",
        "city": "Manhattan",
        "state": "New York",
        "lat_min": 40.80,
        "lat_max": 40.81,
        "lon_min": -73.95,
        "lon_max": -73.94
    },
    {
        "zip": "78401",
        "city": "Corpus Christi",
        "state": "Texas",
        "lat_min": 27.79,
        "lat_max": 27.80,
        "lon_min": -97.40,
        "lon_max": -97.39
    },
    {
        "zip": "29403",
        "city": "Charleston",
        "state": "South Carolina",
        "lat_min": 32.79,
        "lat_max": 32.81,
        "lon_min": -79.95,
        "lon_max": -79.93
    },
    {
        "zip": "22305",
        "city": "Alexandria",
        "state": "Virginia",
        "lat_min": 38.83,
        "lat_max": 38.84,
        "lon_min": -77.06,
        "lon_max": -77.05
    },
    {
        "zip": "10032",
        "city": "Manhattan",
        "state": "New York",
        "lat_min": 40.83,
        "lat_max": 40.84,
        "lon_min": -73.94,
        "lon_max": -73.93
    },
    {
        "zip": "32204",
        "city": "Jacksonville",
        "state": "Florida",
        "lat_min": 30.31,
        "lat_max": 30.32,
        "lon_min": -81.68,
        "lon_max": -81.66
    },
    {
        "zip": "30312",
        "city": "Atlanta",
        "state": "Georgia",
        "lat_min": 33.73,
        "lat_max": 33.75,
        "lon_min": -84.38,
        "lon_max": -84.36
    }
]
def random_city_data():
    """Randomly pick a city from CITY_DATA and generate lat/lon in bounding box."""
    c = random.choice(CITY_DATA)
    lat = random.uniform(c["lat_min"], c["lat_max"])
    lon = random.uniform(c["lon_min"], c["lon_max"])
    return {
        "city": c["city"],
        "state": c["state"],
        "zip": c["zip"],
        "latitude": lat,
        "longitude": lon
    }

def random_features():
    """Generate random property features."""
    return {
        "architectureType": random.choice(["Contemporary", "Ranch", "Victorian", "Modern"]),
        "cooling": random_bool(),
        "coolingType": random.choice(["Central", "Window", "Geothermal"]),
        "exteriorType": random.choice(["Wood", "Brick", "Stucco"]),
        "fireplace": random_bool(),
        "fireplaceType": random.choice(["Masonry", "Insert", "Gas", "None"]),
        "floorCount": random.randint(1, 3),
        "foundationType": random.choice(["Slab / Mat / Raft", "Crawl Space", "Basement"]),
        "garage": random_bool(),
        "garageSpaces": random.randint(0, 3),
        "garageType": random.choice(["Garage", "Carport", "None"]),
        "heating": random_bool(),
        "heatingType": random.choice(["Forced Air", "Radiant", "Heat Pump"]),
        "pool": random_bool(),
        "poolType": random.choice(["Concrete", "Vinyl", "Fiberglass", "None"]),
        "roofType": random.choice(["Asphalt", "Metal", "Tile"]),
        "roomCount": random.randint(3, 10),
        "unitCount": random.randint(1, 2),
        "viewType": random.choice(["City", "Mountain", "Lake", "None"])
    }

def random_tax_assessments(start_year=2019, end_year=2023):
    """Generate random yearly tax assessments."""
    result = {}
    for y in range(start_year, end_year + 1):
        val = random.randint(60000, 700000)
        land_val = int(val * random.uniform(0.2, 0.4))
        improvements_val = val - land_val
        result[str(y)] = {
            "year": y,
            "value": val,
            "land": land_val,
            "improvements": improvements_val
        }
    return result

def random_property_taxes(start_year=2019, end_year=2023):
    """Generate random property tax data per year."""
    result = {}
    for y in range(start_year, end_year + 1):
        total_tax = random.randint(1000, 8000)
        result[str(y)] = {
            "year": y,
            "total": total_tax
        }
    return result

def random_history_events():
    """Generate 1-2 random sale events in the property history."""
    events = {}
    for _ in range(random.randint(1, 2)):
        sale_date = random_date(2000, 2022)
        price = random.randint(80000, 700000)
        events[sale_date[:10]] = {
            "event": "Sale",
            "date": sale_date,
            "price": price
        }
    return events

def random_owner():
    """Generate a random property owner record."""
    name = fake.name()
    c = random_city_data()
    mailing_street = fake.street_address()
    mailing_id = mailing_street.replace(" ", "-").replace(".", "") + f",-{c['city'].replace(' ','-')},-{c['state']}-{c['zip']}"
    formatted_mailing = f"{mailing_street}, {c['city']}, {c['state']} {c['zip']}"

    return {
        "names": [name],
        "type": random.choice(["Individual", "Organization"]),
        "mailingAddress": {
            "id": mailing_id,
            "formattedAddress": formatted_mailing,
            "addressLine1": mailing_street,
            "addressLine2": "",
            "city": c["city"],
            "state": c["state"],
            "zipCode": c["zip"]
        }
    }

# ---------------------------------------------------------------------
# AGENTS_CACHE: to store 10 agents per ZIP code. Then each property picks one.
# ---------------------------------------------------------------------
AGENTS_CACHE = {}  # dict with key=zip_code, value=list of 10 agent dicts

def get_agents_for_zip(zip_code):
    """
    If we haven't generated agents for this zip_code, create 10.
    Return the list of 10 agents for that ZIP.
    """
    if zip_code not in AGENTS_CACHE:
        AGENTS_CACHE[zip_code] = [random_agent(zip_code) for _ in range(10)]
    return AGENTS_CACHE[zip_code]

def random_agent(zip_code):
    """Generate a single real estate agent record with prefix, name, email, agency, phone."""
    prefix = random.choice(["Mr.", "Ms.", "Mrs.", "Dr."])
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}"
    agency = fake.company()  # or pick from a small realty list
    phone_number = str(random.randint(2000000000, 9999999999))

    return {
        "prefix": prefix,
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "realEstateAgency": agency,
        "phoneNumber": phone_number,
        "zipCode": zip_code
    }

def generate_record(i):
    """Generate a single property record with an assigned real estate agent from the zip."""
    # 1) Basic property info
    loc = random_city_data()
    full_street = fake.street_address()
    address_line1 = full_street
    address_line2 = None
    if " Apt " in full_street:
        parts = full_street.split(" Apt ")
        address_line1 = parts[0]
        address_line2 = "Apt " + parts[1]

    city = loc["city"]
    state = loc["state"]
    zip_code = loc["zip"]
    lat = loc["latitude"]
    lon = loc["longitude"]

    last_sale_price = random.randint(100000, 5000000)

    rec_id = address_line1.replace(" ", "-")
    if address_line2:
        rec_id += "-" + address_line2.replace(" ", "-")
    rec_id += f",-{city.replace(' ', '-')},-{state}-{zip_code}"

    # 2) Pick an agent for this property from the 10 agent pool for the ZIP
    agents_list = get_agents_for_zip(zip_code)
    chosen_agent = random.choice(agents_list)

    record = {
        "id": rec_id,
        "formattedAddress": f"{full_street}, {city}, {state} {zip_code}",
        "addressLine1": address_line1,
        "addressLine2": address_line2,
        "city": city,
        "state": state,
        "zipCode": zip_code,
        "county": fake.city_suffix().title(),
        "latitude": round(lat, 6),
        "longitude": round(lon, 6),
        "propertyType": random.choice(["Single Family", "Townhome", "Condo"]),
        "bedrooms": random.randint(1, 6),
        "bathrooms": random.randint(1, 4),
        "squareFootage": random.randint(600, 5000),
        "lotSize": random.randint(1000, 15000),
        "yearBuilt": random.randint(1950, 2022),
        "assessorID": f"{random.randint(10000,99999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
        "legalDescription": f"CB {random.randint(1000,9999)} BLK {random.randint(1,10)} LOT {random.randint(1,100)}",
        "subdivision": random.choice(["CONV A/S CODE", "Subdivision A", "Subdivision B", "Subdivision C"]),
        "zoning": random.choice(["RH", "R1", "RM", "C1"]),
        "lastSaleDate": random_date(2000, 2023),
        "lastSalePrice": last_sale_price,
        "hoa": {
            "fee": random.randint(0, 300)
        },
        "features": random_features(),
        "taxAssessments": random_tax_assessments(),
        "propertyTaxes": random_property_taxes(),
        "history": random_history_events(),
        "owner": random_owner(),
        "ownerOccupied": random_bool(),
        # 3) Real estate agent info
        "realEstateAgent": chosen_agent
    }
    return record
def main():
    num_records = 20000
    output_filename = "synthetic_properties_j.json"

    properties = []
    for i in range(num_records):
        record = generate_record(i)
        properties.append(record)

    with open(output_filename, mode="w", encoding="utf-8") as jsonfile:
        json.dump(properties, jsonfile, indent=2)

    print(f"Successfully wrote {num_records} records to {output_filename}.")

if __name__ == "__main__":
    main()

