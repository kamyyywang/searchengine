import requests
import json
import time

""" Load data from Anteater API into json files """

COURSEDATA_URL = "https://anteaterapi.com/v2/rest/coursesCursor" # load API url
MAJOR_URL = "https://anteaterapi.com/v2/rest/programs/majors"
MINOR_URL = "https://anteaterapi.com/v2/rest/programs/minors"

TAKE = 100 # load data in batches

def fetch_courses(cursor=None, take=TAKE):
    batch_number = 1
    all_course_data = []

    while True:
        params = {"take": take}

        if cursor is not None:
            params["cursor"] = cursor

        response = requests.get(COURSEDATA_URL, params=params)
        response.raise_for_status()

        data = response.json().get("data")

        # check if data exists --> prevent crashes
        if data is None:
            items = []
            cursor = None
        # extract items and nextCursor if data exists
        else:
            items = data.get("items", [])
            cursor = data.get("nextCursor")

        # store batch
        all_course_data.extend(items)

        print(f"Batch {batch_number}: Fetched {len(items)} courses")
        batch_number += 1

        # stop if no more data
        if not cursor:
            break

    # write to json
    with open("all_course_data.json", "w") as f:
        json.dump(all_course_data, f, indent=2)

    print(f"Total courses saved to all_course_data.json: {len(all_course_data)}")

def fetch_majors():
    response = requests.get(MAJOR_URL)
    response.raise_for_status()
    majors = response.json().get("data", [])

    # check if data exists
    if majors is None:
        return []
    
    # fetch requirements for each major
    all_major_data = []

    # retrieve all major ids and extract data from api
    for major in majors:
        program_id = major["id"]
        URL = f"https://anteaterapi.com/v2/rest/programs/major?programId={program_id}"
        response = requests.get(URL)
        response.raise_for_status()
        requirements = response.json().get("data", [])

        # merge major information with requirements
        major_copy = major.copy()
        major_copy["requirements"] = requirements

        all_major_data.append(major_copy)
        time.sleep(0.5)  # sleep 100ms between requests --> avoid client error
    
    # write to json file
    with open("all_major_data.json", "w") as f:
        json.dump(all_major_data, f, indent=2)

    print(f"Saved {len(all_major_data)} majors.")

def fetch_minors():
    response = requests.get(MINOR_URL)
    response.raise_for_status()
    minors = response.json().get("data", [])

    # check if data exists
    if not minors:
        return []
    
    # fetch requirements for each minor
    all_minor_data = []

    # retrieve all minor ids and extract data from api
    for minor in minors:
        program_id = minor["id"]
        URL = f"https://anteaterapi.com/v2/rest/programs/minor?programId={program_id}"
        response = requests.get(URL)
        response.raise_for_status()
        requirements = response.json().get("data", [])

        # merge minor information with requirements
        minor_copy = minor.copy()
        minor_copy["requirements"] = requirements

        all_minor_data.append(minor_copy)
        time.sleep(0.5)  # sleep 100ms between requests --> avoid client error
    
    # write to json file
    with open("all_minor_data.json", "w") as f:
        json.dump(all_minor_data, f, indent=2)

    print(f"Saved {len(all_minor_data)} minors.")

if __name__ == "__main__":
    fetch_courses()
    fetch_majors()
    fetch_minors()