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
else:
    print("Failed to fetch data:", response.status_code)
    problems_data = {}  # Ensure problems_data is a dictionary even on failure

# Assuming 'problems_data' is the JSON response from the API
problems = problems_data.get('stat_status_pairs', [])

# Initialize lists for different difficulties
easy_problems = []
medium_problems = []
hard_problems = []

# Process data as needed here
for problem in problems:
    processed_problem = {
        "title": problem["stat"]["question__title"],  # Accessing the 'stat' dictionary for title
        "url": f"https://leetcode.com/problems/{problem['stat']['question__title_slug']}/",  # Constructing URL using 'question__title_slug'
        "total_acs": problem["stat"]["total_acs"],  # Total "Accepted" submission count
        "total_submitted": problem["stat"]["total_submitted"],  # Total submission count
        "is_new_question": problem["stat"]["is_new_question"]  # Flag indicating if it's a new question
    }
    
    # Categorize by difficulty
    if problem["difficulty"]["level"] == 1:  # Easy
        easy_problems.append(processed_problem)
    elif problem["difficulty"]["level"] == 2:  # Medium
        medium_problems.append(processed_problem)
    elif problem["difficulty"]["level"] == 3:  # Hard
        hard_problems.append(processed_problem)

# Now, 'easy_problems', 'medium_problems', and 'hard_problems' contain the processed lists of problems by difficulty
print(f"Easy Problems: {easy_problems[:3]}")  # Print the first 3 easy problems for verification
print(f"Medium Problems: {medium_problems[:3]}")  # Print the first 3 medium problems for verification
print(f"Hard Problems: {hard_problems[:3]}")  # Print the first 3 hard problems for verification

# Save to JSON files by difficulty
with open('leetcode_easy_problems.json', 'w') as f:
    json.dump(easy_problems, f, indent=4)

with open('leetcode_medium_problems.json', 'w') as f:
    json.dump(medium_problems, f, indent=4)

with open('leetcode_hard_problems.json', 'w') as f:
    json.dump(hard_problems, f, indent=4)
