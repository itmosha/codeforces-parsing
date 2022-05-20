import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from writer import write_json

url = 'https://codeforces.com/problemset'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

items = soup.find_all('tr')

pages = soup.find('div', class_='pagination')
pageNumbers = pages.find_all('span', class_='page-index')
last_page_number = int(pageNumbers[len(pageNumbers) - 1].text)

data = {'problems': []}

for i in tqdm(range(1, last_page_number + 1)):
    url = 'https://codeforces.com/problemset/page/' + str(i)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    problems = soup.find_all('tr')

    for problem, i in enumerate(problems, start=0):
        all_a = i.find_all('a')

        id = all_a[0].text.strip() if len(all_a) > 0 else None

        name = all_a[1].text.strip() if len(all_a) > 1 else None

        difficulty = i.find('span', class_='ProblemRating')
        difficulty = difficulty.text.strip() if difficulty else None

        solves_count = i.find('a', {'title': 'Participants solved the problem'})
        solves_count = solves_count.text.strip() if solves_count else None
        solves_count = solves_count[1::] if solves_count else None

        tags = i.find_all('a', class_='notice')
        for i in range(len(tags)):
            tags[i] = tags[i].text.strip()

        if id or name or difficulty or solves_count or solves_count or tags:
            problem_ = { 'id' : id,
                         'name' : name,
                         'difficulty' : difficulty,
                         'solves_count' : solves_count,
                         'tags' : tags
                        }

            data['problems'].append(problem_)

print('Parsed successfully')
write_json(data)