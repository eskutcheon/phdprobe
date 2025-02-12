#from scraper import scrape_phd_program, save_program_data
from scraper import scrape_all_links
from semantic_parser import parse_html_files


def main():
    # Example: define a dictionary of universities -> list of program page URLs
    # In reality, you might have multiple programs or departmental pages to scrape per university.
    university_urls = {
        "MIT": [
            "https://www.eecs.mit.edu/academics/graduate-programs", #/graduate-program-requirements/",
        ],
        "Stanford": [
            "https://www.cs.stanford.edu/admissions/phd-admissions",
        ],
        "CMU": [
            "https://www.csd.cmu.edu/academics/doctoral/overview",
        ]
    }
    for uni_name, url_list in university_urls.items():
        for url in url_list:
            start_url = url
            # program_data = scrape_phd_program(url, uni_name)
            # if program_data:
            #     save_program_data(program_data, uni_name)
            # else:
            #     print(f"[WARN] Could not scrape data for {url}")
            print(f"[INFO] Scraping all links from {start_url} for {uni_name}...")
            file_paths = scrape_all_links(start_url, uni_name, max_depth=2)
            print(f"[INFO] Scraping complete. Total pages saved: {len(file_paths)}")
            print(f"[INFO] Now performing semantic parse for admission requirements...")
            parse_html_files(file_paths, uni_name)


if __name__ == "__main__":
    main()
