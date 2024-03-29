import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_stack_overflow(tag="python", pages=10):
    questions = []

    for page in range(1, pages + 1):
        url = f"https://stackoverflow.com/questions/tagged/{tag}?tab=Newest&page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for question_summary in soup.select(".s-post-summary"):  # Updated selector
                q = {}
                q['title'] = question_summary.select_one('.s-link').get_text(strip=True)  # Updated selector
                q['votes'] = question_summary.select_one('.s-post-summary--stats-item-number').get_text(strip=True)  # Example update
                q['answers'] = question_summary.select('.s-post-summary--stats-item-number')[1].get_text(strip=True)  # Example update, assuming the second occurrence
                q['views'] = question_summary.select_one('.s-post-summary--stats-item:last-child .s-post-summary--stats-item-number').get_text(strip=True)  # Example update
                q['link'] = "https://stackoverflow.com" + question_summary.select_one('.s-link')['href']  # Assuming this selector is still valid
                questions.append(q)
        else:
            print(f"Failed to get a successful response from the server. Status Code: {response.status_code}")
            break

    return pd.DataFrame(questions)

# Scrape questions tagged with 'python'
df = scrape_stack_overflow(tag="python", pages=2)  # You can adjust the number of pages
print(df.head())

# Save the dataframe to a CSV file
df.to_csv('stackoverflow_python_questions.csv', index=False)
