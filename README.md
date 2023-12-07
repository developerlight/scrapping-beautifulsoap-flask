# Finance News and Information Web Scraper

## Overview

This Python Flask web application scrapes and displays finance-related news and information from various sources, providing users with a centralized platform to stay updated on market trends and news.

## Features

1. **Homepage Overview:**
    - Displays top news and information from multiple sources.
    - Sections include Antara, CNBC, Kompas, Bareksa, and HSB Trading & Forex.

2. **Detailed Views:**
    - Click on news articles to view detailed information.
    - Explore articles from different categories.

3. **Reporter Profiles:**
    - Discover more about reporters and authors contributing to the news articles.

4. **Specialized Sections:**
    - Access specific sections such as Travel news from Antara, Forex news from Bareksa, and HSB's Trading and Forex articles.

5. **Finance Tables:**
    - Explore a dynamic table showcasing real-time data from Google Finance.

## Technologies Used

- Flask: A micro web framework for Python.
- BeautifulSoup: A library for pulling data out of HTML and XML files.
- Requests: A simple HTTP library for Python.
- Jinja2: A fast, expressive, succinct, and extensible template engine.

## Setup Instructions

1. Clone the repository:

    ```bash
    git clone https://github.com/developerlight/scrapping-beautifulsoap-flask.git
    ```

2. Navigate to the project directory:

    ```bash
    cd scrapping-beautifulsoap-flask
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:

    ```bash
    python app.py
    ```

5. Open your browser and go to [http://localhost:5000](http://localhost:5000) to view the application.

## Disclaimer

This web scraper is for educational purposes only. The information provided on this platform may not be accurate or up-to-date. Users should verify information independently and use it at their own risk.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
