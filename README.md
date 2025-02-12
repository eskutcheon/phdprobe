# PhDProbe

PhDProbe is a new tool designed to assist prospective PhD students in making more informed decisions before applying to a degree program. This project aims to streamline various aspects of the initial investigation prior to application.

## Future Application

### Project Goals
- **Data Collection**: Scrape and collect data about PhD programs from various .edu websites.
- **Data Normalization**: Standardize the collected data into a consistent schema.
- **Data Storage**: Store the data in a structured and easily accessible format.
- **Data Sharing**: Enable easy sharing and updating of analyzed data among a small team of developers/researchers.

### Key Data Points
- Acceptance rates
- Number of applicants
- Application requirements
- Funding availability
- Faculty interests
- Deadlines
- GRE/TOEFL requirements

### Architecture & Tech Stack
1. **Scraping Layer**: Tools to fetch HTML from target sites, handle scheduling, throttling, and error handling.
2. **Parsing & Extraction Layer**: Clean and extract relevant data fields, normalize data to a consistent schema.
3. **Storage Layer**:
   - Structured Storage: For tabular data.
   - Document Storage: For unstructured content like program descriptions or faculty research areas.
4. **Access & Visualization Layer**: APIs or dashboards for querying and visualizing the data.

### Recommended Tech Stack
- **Programming Language**: Python
- **Scraping**: Requests + BeautifulSoup, Selenium, Scrapy
- **Data Storage**: PostgreSQL, MongoDB, Google Sheets

### Core Features
- Automated Crawling
- Data Extraction
- Storage & Retrieval
- Versioning

### Data Storage Considerations
- **Structured Data**: Use a relational database like PostgreSQL.
- **Unstructured Data**: Use a document-based store like MongoDB.

### Webscraping Considerations
- **Frameworks**: Requests + BeautifulSoup, Selenium, Scrapy
- **Scheduling**: Recurring scrapes using Cron jobs
- **Ethical & Legal Compliance**: Check `robots.txt` and Terms of Service
- **Data Quality & Parsing Challenges**: Handle unique HTML structures, errors, and missing fields
- **Data Normalization**: Consistent naming scheme and data types

### Collaboration & Project Management
- **Version Control**: Use Git/GitHub
- **Data Versioning**: Store each scrape as a dated CSV/JSON
- **Documentation**: Maintain a README with setup instructions
- **Environment Management**: Use `conda` or `virtualenv`

### Ongoing Maintenance & Considerations
- Check for Website Changes
- Handle Data Gaps
- Scalability
- Privacy & Compliance
- Deployment & Costs
- Performance Optimization

By following this plan, PhDProbe will provide a solid foundation for collecting, storing, analyzing, and sharing PhD program data across multiple universities, eventually building out more sophisticated data science or NLP-driven features.