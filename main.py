import scraper
import parser
import setup_chromedriver
import parser_OINP
import scraper_OINP


# express entry draws
setup_chromedriver.run()
scraper.run()
parser.run()


# OINP draws
scraper_OINP.run()
parser_OINP.run()
