import os
import requests
import json


# Assuming these are the correct environment variables
leetcode_session = os.getenv('leetcode_session')
csrf_token = os.getenv('csrf_token')

headers = {
    'Cookie': f'LEETCODE_SESSION={leetcode_session};',
    'X-CSRFToken': csrf_token,
    'Referer': 'https://leetcode.com'
}

# Hypothetical URL, replace with actual API endpoint if available
url = "https://leetcode.com/api/problems/all/"

response = requests.get(url, headers=headers)

if response.status_code == 200:
    problems_data = response.json()
    print(problems_data)  # or process this data
else:
    print("Failed to fetch data:", response.status_code)
    

# Assuming 'problems_data' is the JSON response from the API
problems = problems_data.get('stat_status_pairs', [])

# Process data as needed here
processed_problems = [
    {
        "title": problem["stat"]["question__title"],  # Accessing the 'stat' dictionary for title
        "url": f"https://leetcode.com/problems/{problem['stat']['question__title_slug']}/",  # Constructing URL using 'question__title_slug'
        "total_acs": problem["stat"]["total_acs"],  # Total "Accepted" submission count
        "total_submitted": problem["stat"]["total_submitted"],  # Total submission count
        "is_new_question": problem["stat"]["is_new_question"]  # Flag indicating if it's a new question
    }
    for problem in problems if problem["status"] == "ac"  # This condition was to filter solved problems; adjust as needed
]

# Now, 'processed_problems' should contain the processed list of problems
print(f"Processed Problems: {processed_problems[:3]}")  # Print the first 3 processed problems for verification

# Save to a JSON file
with open('leetcode_problems.json', 'w') as f:
    json.dump(processed_problems, f, indent=4)
