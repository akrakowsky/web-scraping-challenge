# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# create instance of Flask app
app = Flask(__name__)

 # Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# create route that renders index.html template
@app.route("/")
def index():
    team_list = list(range(0,1000))
    return render_template("index.html", list=team_list)


if __name__ == "__main__":
    app.run(debug=True)


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = { "executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = {}

    url = "https://raleigh.craigslist.org/search/hhh?max_price=1500&availabilityMode=0"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    try:
        listings["headline"] = soup.find("a", class_="result-title").get_text()
        listings["price"] = soup.find("span", class_="result-price").get_text()
        listings["hood"] = soup.find("span", class_="result-hood").get_text()
    except: 
        print("Scrape Complete")
    return listings
https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html
    

# Define database and collection
db = client.craigslist_db
collection = db.items

# URL of page to be scraped
url = 'https://newjersey.craigslist.org/search/sss?sort=rel&query=guitar'


# Retrieve page with the requests module
response = requests.get(url, verify=False)
# Create BeautifulSoup object; parse with 'lxml'
soup = BeautifulSoup(response.text, 'lxml')
response.text

# Examine the results, then determine element that contains sought info
# results are returned as an iterable list
results = soup.find_all('li', class_='result-row')


# Loop through returned results
for result in results:
    # Error handling
    try:
        # Identify and return title of listing
        title = result.find('a', class_='result-title').text
        # Identify and return price of listing
        price = result.a.span.text
        # Identify and return link to listing
        link = result.a['href']

        # Run only if title, price, and link are available
        if (title and price and link):
            # Print results
            print('-------------')
            print(title)
            print(price)
            print(link)

            # Dictionary to be inserted as a MongoDB document
            post = {
                'title': title,
                'price': price,
                'url': link
            }

            collection.insert_one(post)

    except Exception as e:
        print(e)


# Display items in MongoDB collection
listings = db.items.find()

for listing in listings:
    print(listing)