from bs4 import BeautifulSoup
import re


def get_salary(s):
    pattern = r'\d{1,9}'
    #salary = re.findall(pattern, s)[0]
    salary = re.search(pattern, s).group()
    print(salary)

def main():
    file = open('index.html').read()
    soup = BeautifulSoup(file, 'lxml')

    salary = soup.find_all('div', {'data-set': 'salary'})
    for i in salary:
        get_salary(i.text.strip())


if __name__ == "__main__":
    main()