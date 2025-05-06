import json
import random
import uuid
from faker import Faker

# ZIP codes extracted from CITY_DATA
zip_codes = [
    "07030", "60607", "10003", "60614", "53202", "80203", "60657", "10011", "10014",
    "92101", "94702", "90026", "98115", "20002", "94601", "07104", "20782", "90014",
    "20001", "77003", "19123", "10039", "76102", "11211", "19146", "11222", "11216",
    "63103", "90013", "78702", "11237", "10026", "21224", "11221", "20010", "77007",
    "98402", "37408", "11205", "11206", "73104", "30317", "80205", "29492", "33602",
    "55101", "37403", "11238", "20005", "63101", "92113", "97227", "78208", "10031",
    "33620", "28202", "46204", "70115", "93650", "80207", "31401", "70112", "19122",
    "78721", "97211", "23219", "28801", "20003", "91204", "30316", "23459", "78401",
    "29403", "22305", "10032", "32204", "30312"
]

fake = Faker("en_US")


def generate_inspector(zip_code):
    inspector_id = str(uuid.uuid4())
    name = fake.name()
    email = fake.email()
    company = fake.company()
    license_number = fake.bothify(text='INS-#####')
    years_experience = random.randint(1, 30)
    phone = fake.phone_number()
    certification = random.choice([
        "Certified Residential",
        "Certified Commercial",
        "Home Inspector",
        "Structural Inspector",
        "Electrical Safety Inspector"
    ])

    return {
        "inspector_id": inspector_id,
        "zip_code": zip_code,
        "name": name,
        "email": email,
        "company": company,
        "license_number": license_number,
        "years_experience": years_experience,
        "phone": phone,
        "certification": certification
    }


def main():
    inspectors = []
    for zip_code in zip_codes:
        inspectors.append(generate_inspector(zip_code))

    output_file = 'synthetic_property_inspectors.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(inspectors, f, indent=2)

    print(f"Successfully wrote {len(inspectors)} inspector records to {output_file}.")


if __name__ == '__main__':
    main()