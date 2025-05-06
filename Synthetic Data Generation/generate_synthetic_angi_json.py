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

# Service categories to simulate
service_categories = [
    "Handyperson", "Landscaping", "Plumbing", "Electrical",
    "Remodeling", "Roofing", "Painting", "Cleaning",
    "HVAC", "Windows", "Concrete"
]

fake = Faker("en_US")

def generate_contractor(zip_code, category):
    """Generate a synthetic Angi-style contractor record with email."""
    contractor_id = str(uuid.uuid4())
    name = fake.name()
    email = fake.email()
    company = fake.company()
    rating = round(random.uniform(1.0, 5.0), 1)
    num_reviews = random.randint(0, 300)
    latest_review_date = fake.date_between(start_date='-1y', end_date='today').isoformat()
    latest_review = fake.sentence(nb_words=12)

    # Rates in USD per hour or per typical job
    estimated_rate = random.randint(50, 200)
    usual_rate_min = max(20, estimated_rate - random.randint(5, 30))
    usual_rate_max = estimated_rate + random.randint(5, 50)

    # Additional details
    license_number = fake.bothify(text='??#####')
    years_experience = random.randint(1, 40)
    phone = fake.phone_number()
    website = f"https://{fake.domain_name()}"

    return {
        'contractor_id': contractor_id,
        'zip_code': zip_code,
        'service_category': category,
        'name': name,
        'email': email,
        'company': company,
        'rating': rating,
        'num_reviews': num_reviews,
        'latest_review_date': latest_review_date,
        'latest_review': latest_review,
        'estimated_rate': estimated_rate,
        'usual_rate_min': usual_rate_min,
        'usual_rate_max': usual_rate_max,
        'license_number': license_number,
        'years_experience': years_experience,
        'phone': phone,
        'website': website
    }


def main():
    """Generate multiple contractors and write to JSON."""
    rows = []
    for zip_code in zip_codes:
        for category in service_categories:
            for _ in range(5):
                rows.append(generate_contractor(zip_code, category))

    # Write to JSON file
    output_file = 'synthetic_angi_contractors_j.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(rows, f, indent=2)

    print(f"Successfully wrote {len(rows)} contractor records to {output_file}.")


if __name__ == '__main__':
    main()