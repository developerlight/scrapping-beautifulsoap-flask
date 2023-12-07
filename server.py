from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/")
def home():
    antara = scrape_antara()
    cnbc = scrape_cnbc()
    bareksa =scrape_bareksa()
    kompas = scrape_kompas()
    hsb_header, hsb_body = scrape_hsb()
    hsb_forex_header, hsb_forex_body = scrape_hsb_forex()

    return render_template("index.html", antara = antara, cnbc = cnbc, kompas = kompas, bareksa = bareksa, hsb_header = hsb_header, hsb_body = hsb_body, forex_header= hsb_forex_header, forex_body= hsb_forex_body)

def scrape_antara():
    html_doc = requests.get("https://www.antaranews.com/lifestyle/travel")
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    popular_area = soup.find(attrs={'class': 'main-content mag-content clearfix'})

    area = popular_area.findAll(attrs={'class': 'simple-post simple-big clearfix'})
    antara = []
    for item in area:
        img = item.find('img')['data-src']
        link = item.find('a')['href']
        title = item.find('div', class_='simple-thumb').find('a')['title']
        time = item.find('p', class_='simple-share').find('span').text

        antara.append({
            'img' : img,
            'link' : link,
            'title' : title,
            'time' : time
        })
    return antara

def scrape_kompas():
    html_doc = requests.get("https://travel.kompas.com/jalan-jalan")
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    popular_area = soup.find(attrs={'class': 'col-bs10-7'})

    area = popular_area.find_all(attrs={'class': 'article__list clearfix'})
    kompas = []
    for item in area:
        img = item.find('img')['data-src']
        title = item.find('a', class_='article__link').text
        time = item.find('div', {'class':'article__date'}).text
        link = item.find('a')['href']
        kompas.append({
            'img' : img,
            'title' : title,
            'time' : time,
            'link' : link
        })

    return kompas

def scrape_bareksa():
     # Dapatkan halaman web
    url = "https://www.bareksa.com/berita"
    response = requests.get(url)

    # Periksa apakah permintaan berhasil
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        artikel = soup.find_all(attrs={'class': 'sc-brqgnP hVKveG'})
        a = "https://www.bareksa.com"
        bareksa = []
        for item in artikel:
            link_tag_a = item.find('div', class_='caption').find('a')['href']
            link_tag = a + link_tag_a
            tag = item.find('div', class_='caption').find('a').find('div').text
            link_a = item.find('a')['href']
            link = a + link_a
            title = item.find('h6', class_='title').text
            caption = item.find('div', class_='desc').text
            img = item.find('img')['src']
            bareksa.append({
                'title' : title,
                'link': link,
                'link_tag' : link_tag,
                'caption': caption,
                'img' : img,
                'tag' : tag
            })
        
        return bareksa
    else:
            # Tindakan jika elemen tidak ditemukan
        # Siapkan daftar berita untuk ditampilkan di template
       
        # Jika permintaan tidak berhasil, Anda dapat menangani kesalahan di sini
        return "Gagal mengambil data berita."

def scrape_hsb():
    url_trading = 'https://blog.hsb.co.id/category/trading/'
    response = requests.get(url_trading)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        header = soup.find(attrs={'class': 'penci-clearfix penci-biggrid-data penci-dblock penci-fixh'})
        body = soup.find(attrs={'class': 'penci-wrapper-data penci-grid'})
        item_body = body.find_all('li', class_='grid-style')
    
        trading_header = []
        trading_body = []

        for i in range(1, 4):
            header_item = header.find('div', class_='penci-bgitem pcbg-big-item bgitem-{}'.format(i))
            if header_item:
                title = header_item.find('h3', class_='pcbg-title').text
                time = header_item.find('time', class_='entry-date published').text
                link = header_item.find('h3', class_='pcbg-title').find('a')['href']
                tag = header_item.find('a', class_='penci-cat-name penci-cat-1229').find('span').text
                link_tag = header_item.find('a', class_='penci-cat-name penci-cat-1229')['href']
                img = header_item.find('div', class_='pcbg-thumbin').find('div', class_='penci-image-holder penci-lazy')['data-bgset']
                trading_header.append({
                    'title' : title,
                    'time' : time,
                    'link' : link,
                    'tag' : tag,
                    'link_tag' : link_tag,
                    'img' : img
                })
            
        for i in range(4, 8):
            i =  0 if i > 6 else  i
            header_item = header.find('div', class_='penci-bgitem bgitem-{}'.format(i))
            if header_item:
                title = header_item.find('h3', class_='pcbg-title').text
                time = header_item.find('time', class_='entry-date published').text
                link = header_item.find('h3', class_='pcbg-title').find('a')['href']
                tag = header_item.find('a', class_='penci-cat-name penci-cat-1229').find('span').text
                link_tag = header_item.find('a', class_='penci-cat-name penci-cat-1229')['href']
                img = header_item.find('div', class_='pcbg-thumbin').find('div', class_='penci-image-holder penci-lazy')['data-bgset']                    
                trading_header.append({
                    'title' : title,
                    'time' : time,
                    'link' : link,
                    'tag' : tag,                        
                    'link_tag' : link_tag,
                    'img' : img
                })
        
        for item in item_body:
            title = item.find('h2', class_='penci-entry-title entry-title grid-title').find('a').text
            link = item.find('h2', class_='penci-entry-title entry-title grid-title').find('a')['href']
            tag = item.find('a', class_='penci-cat-name penci-cat-1229').text
            reporter = item.find('a', class_='author-url url fn n').text
            link_reporter = item.find('a', class_='author-url url fn n')['href']
            time = item.find('time', class_='entry-date published').text
            short_capt = item.find('div', class_='item-content entry-content').text
            img = item.find('div', class_='thumbnail').find('a')['data-bgset']
            trading_body.append({
                'title' : title,
                'link' : link,
                'tag' : tag,
                'reporter' : reporter,
                'link_reporter' : link_reporter,
                'time' : time,
                'short_capt' : short_capt,
                'img' : img
            })
        
        return trading_header, trading_body

    else:
        return 'gagal mengambil berita'

def scrape_hsb_forex():
    url_trading = 'https://blog.hsb.co.id/category/forex/'
    response = requests.get(url_trading)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        header = soup.find(attrs={'class': 'penci-clearfix penci-biggrid-data penci-dblock penci-fixh'})
        body = soup.find(attrs={'class': 'penci-wrapper-data penci-grid'})
        item_body = body.find_all('li', class_='grid-style')
    
        forex_header = []
        forex_body = []

        for i in range(1, 4):
            header_item = header.find('div', class_='penci-bgitem pcbg-big-item bgitem-{}'.format(i))
            if header_item:
                title = header_item.find('h3', class_='pcbg-title').text
                time = header_item.find('time', class_='entry-date published').text
                link = header_item.find('h3', class_='pcbg-title').find('a')['href']
                tag = header_item.find('a', class_='penci-cat-name penci-cat-1221').find('span').text
                link_tag = header_item.find('a', class_='penci-cat-name penci-cat-1221')['href']
                img = header_item.find('div', class_='pcbg-thumbin').find('div', class_='penci-image-holder penci-lazy')['data-bgset']
                forex_header.append({
                    'title' : title,
                    'time' : time,
                    'link' : link,
                    'tag' : tag,
                    'link_tag' : link_tag,
                    'img' : img
                })
            
        for i in range(4, 8):
            i =  0 if i > 6 else  i
            header_item = header.find('div', class_='penci-bgitem bgitem-{}'.format(i))
            if header_item:
                title = header_item.find('h3', class_='pcbg-title').text
                time = header_item.find('time', class_='entry-date published').text
                link = header_item.find('h3', class_='pcbg-title').find('a')['href']
                tag = header_item.find('a', class_='penci-cat-name penci-cat-1221').find('span').text
                link_tag = header_item.find('a', class_='penci-cat-name penci-cat-1221')['href']
                img = header_item.find('div', class_='pcbg-thumbin').find('div', class_='penci-image-holder penci-lazy')['data-bgset']                    
                forex_header.append({
                    'title' : title,
                    'time' : time,
                    'link' : link,
                    'tag' : tag,                        
                    'link_tag' : link_tag,
                    'img' : img
                })
        
        for item in item_body:
            title = item.find('h2', class_='penci-entry-title entry-title grid-title').find('a').text
            link = item.find('h2', class_='penci-entry-title entry-title grid-title').find('a')['href']
            tag = item.find('a', class_='penci-cat-name penci-cat-1221').text
            reporter = item.find('a', class_='author-url url fn n').text
            link_reporter = item.find('a', class_='author-url url fn n')['href']
            time = item.find('time', class_='entry-date published').text
            short_capt = item.find('div', class_='item-content entry-content').text
            link_img = item.find('div', class_='thumbnail')
            if link_img:
                img = link_img.find('a')['data-bgset']
                forex_body.append({
                'title' : title,
                'link' : link,
                'tag' : tag,
                'reporter' : reporter,
                'link_reporter' : link_reporter,
                'time' : time,
                'short_capt' : short_capt,
                'img' : img
            })
 
        return forex_header ,forex_body
    else:
        return 'gagal mengambil berita'

def scrape_table():
    url = "https://www.google.com/finance"

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('ul', class_='sbnBtf')
        tables = []
        for row in table:
            tag = row.find('div',  class_='uPT9Ec eYHKkf')
            name = row.find('div', class_='ZvmM7').text
            price_curr = row.find('div', class_='YMlKec').text
            total = row.find('div', class_='xVyTdb ghTit').text
            prosentase = row.find('div', class_='zWwE1')
            link = row.find('a')['href']
            link = url + link.lstrip('.')

            tables.append({
                'tag' : tag,
                'name' : name,
                'price_curr' : price_curr,
                'total' : total,
                'prosentase' : prosentase,
                'url' : link
            })

        return tables
    else:
        return "Gagal mengakses halaman web."

def scrape_title(div_elements):
    for div_element in div_elements:
        a_elements = div_element.find_all('a')
        
        # Hitung berapa banyak elemen <a> yang ditemukan
        num_a_elements = len(a_elements)
        # Jika ada dua elemen <a>, abaikan yang memiliki class "ProPill-proPillLink"
        if num_a_elements == 3:
            for a_element in a_elements:
                if 'ProPill-proPillLink' not in a_element.get('class', []):
                    return a_element, a_element['href']

        else:
            # Jika tidak ada dua elemen <a>, Anda dapat memprosesnya sesuai kebutuhan
            for a_element in a_elements:
                return a_element, a_element['href']

def scrape_cnbc():
    # Dapatkan halaman web
    url = "https://www.cnbc.com/world/?region=world"
    response = requests.get(url)

    # Periksa apakah permintaan berhasil
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Temukan elemen dengan class "body flexposts" yang berisi berita-berita
        area_latest_story = soup.find(attrs={'class': 'RiverPlus-riverPlusContainer'})

        # Temukan semua elemen berita
        if area_latest_story:
            news_items = area_latest_story.find_all('div', class_='RiverPlusCard-container')
            # Lanjutkan pemrosesan berita
            news = []
            # reporter = news_items.find('span', class_='RiverByline-authorByline')
            
            for item in news_items:
                # title = item.find('a')
                title, link= scrape_title(item)
                # if img:
                #     return 'ada'
                # else:
                #     return 'tidak ada'
                author_elements = item.find_all('span', class_='RiverByline-authorByline')
                reporter_href = ''
                # Pastikan ada elemen yang cocok sebelum mencoba mengaksesnya
                if author_elements:
                    # Mengambil elemen pertama dari hasil pencarian
                    first_author_element = author_elements[0]
                    
                    # Sekarang, Anda dapat mencari elemen 'a' dalam elemen pertama
                    reporter = first_author_element.find('span').find('a')

                    # Sekarang, Anda dapat mengakses atribut atau teks dalam elemen 'a'
                    if reporter:
                        reporter_text = reporter.text  # Ini akan memberikan teks di dalam elemen 'a'
                        reporter_href = reporter['href']  # Ini akan memberikan nilai atribut 'href' dari elemen 'a'
                else:
                    # Handle jika tidak ada elemen yang cocok
                    reporter_text = None
                    reporter_href = None
                # link = item.find('a')['href']
                tag = item.find('img')
                src_tag = ''
                if tag:
                    # Mengambil nilai atribut 'src' dari elemen gambar
                    tag_src = tag['src']
                    src_tag = tag_src
                # reporter = item.find('span', class_='RiverByline-authorByline')
                time = item.find('span', class_='RiverByline-datePublished')
                news.append({
                    'title': title,
                    'link': link,
                    # 'img' : src_img,
                    'name_re' : reporter_text,
                    'link_re' : reporter_href,
                    'tag' : src_tag,
                    'time': time
                })
            return news
        else:
            return 'file kosong'
    else:
            # Tindakan jika elemen tidak ditemukan
        # Siapkan daftar berita untuk ditampilkan di template
       
        # Jika permintaan tidak berhasil, Anda dapat menangani kesalahan di sini
        return "Gagal mengambil data berita."


@app.route("/cnbc-news")
def forex_news():
    # Dapatkan halaman web
    url = "https://www.cnbc.com/world/?region=world"
    response = requests.get(url)

    # Periksa apakah permintaan berhasil
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Temukan elemen dengan class "body flexposts" yang berisi berita-berita
        area_latest_story = soup.find(attrs={'class': 'RiverPlus-riverPlusContainer'})

        # Temukan semua elemen berita
        if area_latest_story:
            news_items = area_latest_story.find_all('div', class_='RiverPlusCard-container')
            # Lanjutkan pemrosesan berita
            news = []
            
            for item in news_items:
                title = item.find('a')
                author_elements = item.find_all('span', class_='RiverByline-authorByline')

                # Pastikan ada elemen yang cocok sebelum mencoba mengaksesnya
                if author_elements:
                    # Mengambil elemen pertama dari hasil pencarian
                    first_author_element = author_elements[0]
                    
                    # Sekarang, Anda dapat mencari elemen 'a' dalam elemen pertama
                    reporter = first_author_element.find('span').find('a')

                    # Sekarang, Anda dapat mengakses atribut atau teks dalam elemen 'a'
                    if reporter:
                        reporter_text = reporter.text  # Ini akan memberikan teks di dalam elemen 'a'
                        reporter_href = reporter['href']  # Ini akan memberikan nilai atribut 'href' dari elemen 'a'
                else:
                    # Handle jika tidak ada elemen yang cocok
                    reporter_text = None
                    reporter_href = None
                link = item.find('a')['href']
                tag = item.find('img')
                src_tag = ''
                if tag:
                    # Mengambil nilai atribut 'src' dari elemen gambar
                    tag_src = tag['src']
                    src_tag = tag_src
                time = item.find('span', class_='RiverByline-datePublished')

                news.append({
                    'title': title,
                    'link': link,
                    # 'img' : src_img,
                    'name_re' : reporter_text,
                    'link_re' : reporter_href,
                    'tag' : src_tag,
                    'time': time
                })
            return render_template("cnbc_news.html", news=news)
        else:
            return 'file kosong'
    else:
            # Tindakan jika elemen tidak ditemukan
        # Siapkan daftar berita untuk ditampilkan di template
       
        # Jika permintaan tidak berhasil, Anda dapat menangani kesalahan di sini
        return "Gagal mengambil data berita."

@app.route('/news/<int:index>')
def news_detail(index):
    #ambil url berdasarkan index
    news_data = scrape_news()
    if index >= 0 and index < len(news_data):
        
        news_url = news_data[index]['link']
        header, key_point, article = scrape_detail(news_url)
        # return redirect(news_url)
        return render_template("detail_news.html", header = header, key_point = key_point, article = article)
    
    return redirect(url_for('home'))

@app.route('/kompas/travel/<int:index>')
def kompas_travel(index):
    #ambil url berdasarkan index
    news_data = scrape_kompas()
    if index >= 0 and index < len(news_data):
        
        news_url = news_data[index]['link']
        news = scrape_kompas_travel(news_url)
        # return news
        return render_template("travel_kompas.html", news = news)
    return redirect(url_for('home'))

@app.route('/antara/travel/<int:index>')
def antara_travel(index):
    #ambil url berdasarkan index
    news_data = scrape_antara()
    if index >= 0 and index < len(news_data):
        
        news_url = news_data[index]['link']
        news = scrape_antara_travel(news_url)
        # return news
        return render_template("travel_kompas.html", news = news)
    return redirect(url_for('home'))

@app.route('/reporter/<int:index>')
def reporter_detail(index):
    #ambil url berdasarkan index
    news_data = scrape_news()
    if index >= 0 and index < len(news_data):
        
        reporter_url = news_data[index]['link_re']
        # header, key_point, article = scrape_reporter(reporter_url)
        biodata = scrape_reporter(reporter_url)
        return render_template("detail_reporter.html", biodata = biodata)
    
    return redirect(url_for('home'))

@app.route('/bareksa/news/<int:index>')
def bareksa_news(index):
    #ambil url berdasarkan index
    news_data = scrape_bareksa()
    if index >= 0 and index < len(news_data):
        
        url = news_data[index]['link']
        # header, key_point, article = scrape_reporter(reporter_url)
        news = scrape_bareksa_news(url)

        return render_template("bareksa_news.html", news = news)
    
    return redirect(url_for('home'))

@app.route('/hsb/trading/<int:index>')
def hbs_trading(index):
    #ambil url berdasarkan index
    header, body = scrape_hsb()
    if index >= 0 and index < len(body):
        
        url = body[index]['link']
        trading_body = scrape_hsb_trading(url)

        return render_template("hbs_trading.html", article = trading_body)
    
    return redirect(url_for('home'))

@app.route('/hsb/author/<int:index>')
def hbs_trading_author(index):
    #ambil url berdasarkan index
    header, body = scrape_hsb()
    if index >= 0 and index < len(body):
        
        url = body[index]['link_reporter']
        trading_body = scrape_hsb_trading_author(url)
        # return trading_body
        return render_template("hbs_author.html", author = trading_body)
    
    return redirect(url_for('home'))

@app.route('/hsb/treding/<int:index>')
def hbs_treding(index):
    #ambil url berdasarkan index
    header, body = scrape_hsb()
    if index >= 0 and index < len(header):
        
        url = header[index]['link']
        trading_header = scrape_hsb_trading(url)

        return render_template("hbs_trading.html", article = trading_header)
    
    return redirect(url_for('home'))

@app.route('/hsb/forex/<int:index>')
def hbs_forex(index):
    #ambil url berdasarkan index
    header, body = scrape_hsb_forex()
    if index >= 0 and index < len(header):
        
        url = header[index]['link']
        trading_header = scrape_hsb_trading(url)

        return render_template("hbs_forex.html", article = trading_header)
    
    return redirect(url_for('home'))

@app.route('/hsb/forex-body/<int:index>')
def hsb_forex_boody(index):
    #ambil url berdasarkan index
    header, body = scrape_hsb_forex()
    if index >= 0 and index < len(body):
        
        url = body[index]['link']
        trading_header = scrape_hsb_trading(url)

        return render_template("hbs_forex.html", article = trading_header)
    
    return redirect(url_for('home'))

@app.route('/hsb/author-body/<int:index>')
def hbs_trading_author_body(index):
    #ambil url berdasarkan index
    header, body = scrape_hsb_forex()
    if index >= 0 and index < len(body):
        
        url = body[index]['link_reporter']
        trading_body = scrape_hsb_trading_author(url)
        # return trading_body
        return render_template("hbs_author_forex.html", author = trading_body)
    
    return redirect(url_for('home'))

@app.route('/table/<int:index>')
def table_finance(index):
    #ambil url berdasarkan index
    table = scrape_table()
    if index >= 0 and index < len(table):
        
        url = table[index]['url']
        table_finance = scrape_table_item(url)
        table = table_finance[0]['data']['table'][0]

        return render_template("table_desc.html", tables= table_finance, table=table)
    
    return redirect(url_for('home'))


def scrape_news():
    # URL situs web berita yang akan di-scrape
    url = "https://www.cnbc.com/world/?region=world"  # Ganti dengan URL situs berita yang sesuai

    # Lakukan permintaan HTTP ke situs web
    response = requests.get(url)

    # Inisialisasi daftar untuk menyimpan data berita
    news_data = []

    # Periksa apakah permintaan berhasil
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Temukan elemen-elemen berita di situs web
        area = soup.find(attrs={'class': 'RiverPlus-riverPlusContainer'}) # Ganti dengan selektor yang sesuai

        if area:
            news_items = area.find_all('div', class_='RiverPlusCard-container')
            for item in news_items:
            # Ambil informasi yang Anda butuhkan (judul, waktu, URL, gambar, dll.)
                title, link = scrape_title(item)
                author_elements = item.find_all('span', class_='RiverByline-authorByline')

                link_re = ''
                # Pastikan ada elemen yang cocok sebelum mencoba mengaksesnya
                if author_elements:
                    # Mengambil elemen pertama dari hasil pencarian
                    first_author_element = author_elements[0]
                    
                    # Sekarang, Anda dapat mencari elemen 'a' dalam elemen pertama
                    link_re = first_author_element.find('span').find('a')['href']
                # link_re = item.find('span').find('a')['href']

                # Simpan data berita dalam bentuk kamus
                news_item = {
                    'title': title,
                    'link': link,
                    'link_re' : link_re
                }

                # Tambahkan data berita ke dalam daftar
                news_data.append(news_item)

    return news_data

def scrape_detail(url):
    response = requests.get(url)

    # Periksa apakah permintaan berhasil
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Temukan elemen dengan class "body flexposts" yang berisi berita-berita
        headers = soup.find(attrs={'class': 'ArticleHeader-headerContentContainer'})
        # area_img = soup.find(attrs={'class': 'InlineImage-imageContainer'})
        # print(area_img)
        header = []
        # Temukan semua elemen berita
        if headers:
            city = headers.find('a').text
            title = headers.find('h1', class_='ArticleHeader-headline').text
            time = headers.find('time').text
            header.append({
                'city' : city,
                'title' : title,
                'time' : time
            })
        key_points = soup.find(attrs={'class': 'RenderKeyPoints-wrapper'})
        key_point = []
        if key_points:
            title = key_points.find('div', class_='RenderKeyPoints-header').text
            content = key_points.find('div', class_='group')
            key_point.append({
                'title' : title,
                'content' : content
            })
        area_article = soup.find(attrs={'class': 'ArticleBody-articleBody'})
        article = []
        if area_article:

            # img_embed = area_article.find('div', class_='InlineImage-imageEmbed')
            # img1 = area_article.find('div', class_='InlineImage-imageEmbed')
            # img2 = img1.find('div', class_='InlineImage-wrapper')
            # img3 = img2.find('div', class_='InlineImage-imagePlaceholder')
            # img = img3.find('div', class_='transition-fade-appear-done transition-fade-enter-done')
            # print(img)
            img_caption = area_article.find('div', class_='InlineImage-imageEmbedCaption')
            img_credit = area_article.find('div', class_='InlineImage-imageEmbedCredit')
            content = area_article.find('div', class_='group')
            article.append({
                'img_caption' : img_caption,
                'img_credit' : img_credit,
                'content' : content
            })

        return header, key_point, article

def scrape_kompas_travel(url):
    response = requests.get(url)

    # Periksa apakah permintaan berhasil
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')
        area = soup.find(attrs={'class': 'container clearfix'})
        news = []
        # Temukan semua elemen berita
        if area:
            title = area.find('h1', class_='read__title').text
            tag = area.find('div', class_='topicSubtitle')
            credit = area.find('div', class_='credit')
            time = area.find('div', class_='read__time')
            img = area.find('div', class_='photo__wrap').find('img')['src']
            img_capt = area.find('div', class_='photo__caption').text
            konten = area.find('div', class_='read__content').find('div', class_='clearfix')
            for i in konten.find_all('script'):
                i.extract()

            for i in konten.find_all('iframe'):
                i.extract()

            news.append({
                'title' : title,
                'tag' : tag,
                'time' : time,
                'credit' : credit,
                'img' : img,
                'img_capt' : img_capt,
                'konten' : konten
            })
            print(news)
        
        return news

def scrape_antara_travel(url):
    response = requests.get(url)

    # Periksa apakah permintaan berhasil
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')
        area = soup.find(attrs={'class': 'post-wrapper clearfix'})
        news = []
        # Temukan semua elemen berita
        if area:
            title = area.find('h1', class_='post-title').text
            # tag = area.find('div', class_='topicSubtitle')
            credit = area.find('p', class_='text-muted small mt10')
            time = area.find('span', class_='article-date')
            img = area.find('figure', class_='image-overlay').find('img')['src']
            img_capt = area.find('p', class_='wp-caption-text').text
            konten = area.find('div', class_='post-content clearfix')
            for i in konten.find_all('p', class_='text-muted small mt10'):
                i.extract()

            for i in konten.find_all('span', class_='baca-juga'):
                i.extract()

            news.append({
                'title' : title,
                # 'tag' : tag,
                'time' : time,
                'credit' : credit,
                'img' : img,
                'img_capt' : img_capt,
                'konten' : konten
            })
            print(news)
        
        return news

def scrape_reporter(url):
    response = requests.get(url)

    # Periksa apakah permintaan berhasil
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Temukan elemen dengan class "body flexposts" yang berisi berita-berita
        bio = soup.find(attrs={'class': 'PageBuilder-col-12 PageBuilder-col'})
        reporter = []
        # Temukan semua elemen berita
        if bio:
            name = bio.find('h1').text
            job = bio.find('span').text
            
            deskripsi = bio.find('div', class_='RenderBioDetails-bioText')
            reporter.append({
                'name' : name,
                'job' : job,
                'deskripsi' : deskripsi
            })
        
        return reporter

def scrape_bareksa_news(url):
    response = requests.get(url)

    # Periksa apakah permintaan berhasil
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')
        a = 'https://www.bareksa.com'
        # Temukan elemen dengan class "body flexposts" yang berisi berita-berita
        area = soup.find(attrs={'class': 'tablet-lg:mx-auto tablet-lg:w-[640px] desktop:w-[668px] desktop:!mx-0'})
        news = []
        # Temukan semua elemen berita
        if area:
            title = area.find('h1', class_='heading-xl--bold tablet-lg:desktop-heading-4--bold text-neutral-gray-800 mt-4').text
            inti = area.find('p', class_='hidden tablet-lg:block mt-4 desktop-body-s--medium text-neutral-gray-700').text
            time_reporter = area.find('div', class_='desktop-body-xs--regular text-neutral-gray-500').text
            img_a = area.find('div', class_='relative mt-6 -mx-4 w-screen tablet:-mx-6 tablet-lg:w-full tablet-lg:mx-0 tablet-lg:my-0').find('img')['src']
            img = a + img_a
            fig_capt = area.find('figcaption', class_='mt-3 text-neutral-gray-500 text-s--regular tablet-lg:desktop-body-xs--regular').text
            konten = area.find('section', class_='text-neutral-gray-700 text-m--regular tablet-lg:desktop-body-s--regular mt-6 tablet-lg:mt-8')
    
            news.append({
                'title' : title,
                'inti' : inti,
                'time_reporter' : time_reporter,
                'img' : img,
                'fig_capt' : fig_capt,
                'konten' : konten
            })
        
        return news

def scrape_hsb_trading(url):
    response = requests.get(url)

    # Periksa apakah permintaan berhasil
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # Temukan elemen dengan class "body flexposts" yang berisi berita-berita
        area = soup.find(attrs={'class': 'post type-post status-publish'})
        news = []
        # Temukan semua elemen berita
        if area:
            title = area.find('h1', class_='post-title single-post-title entry-title').text
            time = area.find('time', class_='entry-date published').text
            reporter = area.find('a', class_='author-url url fn n').text
            link_reporter = area.find('a', class_='author-url url fn n')['href']
            img = area.find('div', class_='post-image').find('img')['data-src']
            konten = area.find('div', class_='inner-post-entry entry-content')
            
            for i in konten.find_all(class_='penci-ilrltpost-beaf'):
                i.extract()

            news.append({
                'title' : title,
                'time' : time,
                'reporter' : reporter,
                'link_reporter' : link_reporter,
                'img' : img,
                'konten' : konten
            })
        
        return news

def scrape_hsb_trading_author(url):
    response = requests.get(url)

    # Periksa apakah permintaan berhasil
    if response.status_code == 200:

        soup = BeautifulSoup(response.text, 'html.parser')
        # Temukan elemen dengan class "body flexposts" yang berisi berita-berita
        area = soup.find(attrs={'class': 'theiaStickySidebar'})
    
        news = []
        # Temukan semua elemen berita
        if area:
            title = area.find('div', class_='title-bar')
            nama = area.find('div', class_='author-content').find('h5').text
            link_nama = area.find('div', class_='author-content').find('h5').find('a')['href']
            position = area.find('div', class_='author-content').find('p').text
            news.append({
                'title' : title,
                'name' : nama,
                'link_nama' : link_nama,
                'position' : position
            })
        
        return news

def scrape_table_item(url):
    response = requests.get(url)

    # Periksa apakah permintaan berhasil
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Temukan elemen dengan class "body flexposts" yang berisi berita-berita
        areas = soup.find_all(attrs={'class': 'e1AOyf'})
        area = areas[1]
        details = []
        # Temukan semua elemen berita
        if area:
            title = area.find('div', class_='zzDege').text
            money = area.find('div', class_='YMlKec fxKbKc').text
            # desc_persentasi = area.find('div', class_='CGyduf')
            persentase = area.find('div', class_='JwB6zf')
            desc_money = area.find('div', class_='ygUjEc')
            desc = area.find_all('div', class_='mfs7Fc')
            val_desc = area.find_all('div', class_='P6K39c')
            # print(desc_persentasi)
            data = {
                'table': [{
                    'desc' : desc,
                    'val_desc' : val_desc
                }]
            }

            details.append({
               'title' : title,
               'money' : money,
               'persentase' : persentase,
            #    'desc_persentasi' : desc_persentasi,
               'desc_money' : desc_money,
               'data' : data
            })

            return details


@app.route('/cnbc-news/detail')
def detail_cnbc():
    url = "/news/<int:index>"
    response = requests.get(url)

    # Periksa apakah permintaan berhasil
    if response.status_code == 200:
        return 'ok'
        soup = BeautifulSoup(response.text, 'html.parser')

        # Temukan elemen dengan class "body flexposts" yang berisi berita-berita
        header = soup.find(attrs={'class': 'ArticleHeader-headerContentContainer'})

        # Temukan semua elemen berita
        if header:
            return 'ok'
            # news_items = header.find_all('div', class_='RiverPlusCard-container')
            # if news_items:
            #     return 'ada'
            # else:
            #     return 'tidak ada1'
            # Lanjutkan pemrosesan berita
            # news = []
            # reporter = news_items.find('span', class_='RiverByline-authorByline')
            
            # for item in news_items:
            #     item=''
            # return render_template("a_berita1.html", news=news)
        else:
            return 'file kosong'
    else:
            # Tindakan jika elemen tidak ditemukan
        # Siapkan daftar berita untuk ditampilkan di template
       
        # Jika permintaan tidak berhasil, Anda dapat menangani kesalahan di sini
        return "Gagal mengambil data berita."

@app.route("/antara-travel")
def travel_antara():
    html_doc = requests.get("https://www.antaranews.com/lifestyle/travel")
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    popular_area = soup.find(attrs={'class': 'main-content mag-content clearfix'})

    area = popular_area.findAll(attrs={'class': 'simple-post simple-big clearfix'})
    antara = []
    for item in area:
        img = item.find('img')['data-src']
        link = item.find('a')['href']
        title = item.find('div', class_='simple-thumb').find('a')['title']
        time = item.find('p', class_='simple-share').find('span').text

        antara.append({
            'img' : img,
            'link' : link,
            'title' : title,
            'time' : time
        })
    return antara

    return render_template("travel_antara.html", area = area)

@app.route("/travel-kompas")
def travel_kompas():
    html_doc = requests.get("https://travel.kompas.com/jalan-jalan")
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    popular_area = soup.find(attrs={'class': 'col-bs10-7'})

    area = popular_area.find_all(attrs={'class': 'article__list clearfix'})
    kompas = []
    for item in area:
        img = item.find('img')['data-src']
        title = item.find('a', class_='article__link').text
        time = item.find('div', {'class':'article__date'}).text
        link = item.find('a')['href']
        kompas.append({
            'img' : img,
            'title' : title,
            'time' : time,
            'link' : link
        })

    return kompas

@app.route('/forex-news')
def news_forex():
     # Dapatkan halaman web
    url = "https://www.bareksa.com/berita"
    response = requests.get(url)

    # Periksa apakah permintaan berhasil
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        artikel = soup.find_all(attrs={'class': 'sc-brqgnP hVKveG'})
        bareksa = []
        for item in artikel:
            link_caption = item.find('div', class_='caption').find('a')['href']
            tag = item.find('div', class_='caption').find('a').find('div').text
            time = item.find('div', class_='caption').find('div', variant_='caption')
            link = item.find('a')['href']
            title = item.find('h6', class_='title').text
            caption = item.find('div', class_='caption').text
            img = item.find('img')['src']
            bareksa.append({
                'title' : title,
                'link': link,
                'link_caption' : link_caption,
                'caption': caption,
                'img' : img,
                'tag' : tag,
                'time' : time
            })
        
        return bareksa
    else:
            # Tindakan jika elemen tidak ditemukan
        # Siapkan daftar berita untuk ditampilkan di template
       
        # Jika permintaan tidak berhasil, Anda dapat menangani kesalahan di sini
        return "Gagal mengambil data berita."

@app.route('/hsb')
def topik_hsb():
    url_trading = 'https://blog.hsb.co.id/category/trading/'
    response = requests.get(url_trading)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        header = soup.find(attrs={'class': 'penci-clearfix penci-biggrid-data penci-dblock penci-fixh'})
        body = soup.find(attrs={'class': 'penci-wrapper-data penci-grid'})
        item_body = body.find_all('li', class_='grid-style')
    
        trading_header = []
        trading_body = []

        for i in range(1, 4):
            header_item = header.find('div', class_='penci-bgitem pcbg-big-item bgitem-{}'.format(i))
            if header_item:
                title = header_item.find('h3', class_='pcbg-title').text
                time = header_item.find('time', class_='entry-date published').text
                link = header_item.find('h3', class_='pcbg-title').find('a')['href']
                tag = header_item.find('a', class_='penci-cat-name penci-cat-1229').find('span').text
                link_tag = header_item.find('a', class_='penci-cat-name penci-cat-1229')['href']
                img = header_item.find('div', class_='pcbg-thumbin').find('div', class_='penci-image-holder penci-lazy')['data-bgset']
                trading_header.append({
                    'title' : title,
                    'time' : time,
                    'link' : link,
                    'tag' : tag,
                    'link_tag' : link_tag,
                    'img' : img
                })
            
        for i in range(4, 8):
            i =  0 if i > 6 else  i
            header_item = header.find('div', class_='penci-bgitem bgitem-{}'.format(i))
            if header_item:
                title = header_item.find('h3', class_='pcbg-title').text
                time = header_item.find('time', class_='entry-date published').text
                link = header_item.find('h3', class_='pcbg-title').find('a')['href']
                tag = header_item.find('a', class_='penci-cat-name penci-cat-1229').find('span').text
                link_tag = header_item.find('a', class_='penci-cat-name penci-cat-1229')['href']
                img = header_item.find('div', class_='pcbg-thumbin').find('div', class_='penci-image-holder penci-lazy')['data-bgset']                    
                trading_header.append({
                    'title' : title,
                    'time' : time,
                    'link' : link,
                    'tag' : tag,                        
                    'link_tag' : link_tag,
                    'img' : img
                })
        
        for item in item_body:
            title = item.find('h2', class_='penci-entry-title entry-title grid-title').find('a').text
            link = item.find('h2', class_='penci-entry-title entry-title grid-title').find('a')['href']
            tag = item.find('a', class_='penci-cat-name penci-cat-1229').text
            reporter = item.find('a', class_='author-url url fn n').text
            link_reporter = item.find('a', class_='author-url url fn n')['href']
            time = item.find('time', class_='entry-date published').text
            short_capt = item.find('div', class_='item-content entry-content').text
            img = item.find('div', class_='thumbnail').find('a')['data-bgset']
            trading_body.append({
                'title' : title,
                'link' : link,
                'tag' : tag,
                'reporter' : reporter,
                'link_reporter' : link_reporter,
                'time' : time,
                'short_capt' : short_capt,
                'img' : img
            })
        return trading_header
    else:
        return 'gagal mengambil berita'

@app.route('/hsb-forex')
def topik_hsb_forex():
    url_trading = 'https://blog.hsb.co.id/category/forex/'
    response = requests.get(url_trading)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        header = soup.find(attrs={'class': 'penci-clearfix penci-biggrid-data penci-dblock penci-fixh'})
        body = soup.find(attrs={'class': 'penci-wrapper-data penci-grid'})
        item_body = body.find_all('li', class_='grid-style')
    
        forex_header = []
        forex_body = []

        for i in range(1, 4):
            header_item = header.find('div', class_='penci-bgitem pcbg-big-item bgitem-{}'.format(i))
            if header_item:
                title = header_item.find('h3', class_='pcbg-title').text
                time = header_item.find('time', class_='entry-date published').text
                link = header_item.find('h3', class_='pcbg-title').find('a')['href']
                tag = header_item.find('a', class_='penci-cat-name penci-cat-1221').find('span').text
                link_tag = header_item.find('a', class_='penci-cat-name penci-cat-1221')['href']
                img = header_item.find('div', class_='pcbg-thumbin').find('div', class_='penci-image-holder penci-lazy')['data-bgset']
                forex_header.append({
                    'title' : title,
                    'time' : time,
                    'link' : link,
                    'tag' : tag,
                    'link_tag' : link_tag,
                    'img' : img
                })
            
        for i in range(4, 8):
            i =  0 if i > 6 else  i
            header_item = header.find('div', class_='penci-bgitem bgitem-{}'.format(i))
            if header_item:
                title = header_item.find('h3', class_='pcbg-title').text
                time = header_item.find('time', class_='entry-date published').text
                link = header_item.find('h3', class_='pcbg-title').find('a')['href']
                tag = header_item.find('a', class_='penci-cat-name penci-cat-1221').find('span').text
                link_tag = header_item.find('a', class_='penci-cat-name penci-cat-1221')['href']
                img = header_item.find('div', class_='pcbg-thumbin').find('div', class_='penci-image-holder penci-lazy')['data-bgset']                    
                forex_header.append({
                    'title' : title,
                    'time' : time,
                    'link' : link,
                    'tag' : tag,                        
                    'link_tag' : link_tag,
                    'img' : img
                })
        
        for item in item_body:
            title = item.find('h2', class_='penci-entry-title entry-title grid-title').find('a').text
            link = item.find('h2', class_='penci-entry-title entry-title grid-title').find('a')['href']
            tag = item.find('a', class_='penci-cat-name penci-cat-1221').text
            reporter = item.find('a', class_='author-url url fn n').text
            link_reporter = item.find('a', class_='author-url url fn n')['href']
            time = item.find('time', class_='entry-date published').text
            short_capt = item.find('div', class_='item-content entry-content').text
            link_img = item.find('div', class_='thumbnail')
            if link_img:
                img = link_img.find('a')['data-bgset']
                forex_body.append({
                'title' : title,
                'link' : link,
                'tag' : tag,
                'reporter' : reporter,
                'link_reporter' : link_reporter,
                'time' : time,
                'short_capt' : short_capt,
                'img' : img
            })
 
        return forex_body
    else:
        return 'gagal mengambil berita'

@app.route('/google-table')
def table():
    url = "https://www.google.com/finance"

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('ul', class_='sbnBtf')
        tables = []
        for row in table:
            tag = row.find('div',  class_='uPT9Ec eYHKkf')
            name = row.find('div', class_='ZvmM7').text
            price_curr = row.find('div', class_='YMlKec').text
            total = row.find('div', class_='xVyTdb ghTit').text
            prosentase = row.find('div', class_='zWwE1')
            link = row.find('a')['href']
            link = url + link.lstrip('.')

            tables.append({
                'tag' : tag,
                'name' : name,
                'price_curr' : price_curr,
                'total' : total,
                'prosentase' : prosentase,
                'url' : link
            })

        return render_template('table.html', tables = tables)
    else:
        return "Gagal mengakses halaman web."


app.run(debug=True)

