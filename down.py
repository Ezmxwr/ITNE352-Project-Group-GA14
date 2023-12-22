import requests
from bs4 import BeautifulSoup

# URL of the page containing the links to download
url = "https://blackboard.uob.edu.bh/ultra/courses/_56313_1/outline/edit/document/_1930261_1?courseId=_56313_1&view=content"

# Make a request to the page
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links to download files
    download_links = soup.find_all('a', {'class': 'download-link'})

    # Download each file
    for link in download_links:
        file_url = link['href']
        file_name = link.text.strip()

        # Download the file
        file_response = requests.get(file_url)

        # Save the file locally
        with open(file_name, 'wb') as file:
            file.write(file_response.content)

        print(f"Downloaded: {file_name}")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
