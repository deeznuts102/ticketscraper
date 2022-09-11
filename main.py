from scrape.ticketswap_scraper import TicketSwapScraper



def main():
    scraper = TicketSwapScraper()
    scraper.scrape_weekend_tickets()

if __name__ == "__main__":
    main()
