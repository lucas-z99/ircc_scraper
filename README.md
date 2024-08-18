# For

Scrap IRCC's ExpressEntry draws, save in a excel so you can analysis


# How to use
1. Requires python & python modules: **pip install requests selenium pandas beautifulsoup4**

2. Run run.py
   
3. If you never update Chrome, setup your Chrome version in

    **setup_chromedriver.py**
   
   
# How it works
Data on IRCC's website is loaded dynamically with .js 

So BeautifulSoup is not enough

The workaround is pretending to be a browser (with Chromedriver), click some button

After that, it's simple parse and save.
