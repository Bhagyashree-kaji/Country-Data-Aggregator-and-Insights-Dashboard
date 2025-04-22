# Country Data Aggregator and Insights Dashboard

A comprehensive web application that fetches, processes, and visualizes data from the REST Countries API. This project provides an interactive dashboard and detailed country information through a clean, responsive interface.

## Features

- **Data Aggregation**: Automatically fetches and updates country data from REST Countries API
- **Interactive Dashboard**: Visual representation of global data through charts and statistics
- **Country Explorer**: Browse countries with filtering and sorting capabilities
- **Detailed Country Profiles**: In-depth information about each country with regional comparisons
- **Data Visualization**: Multiple chart types for population, area, and regional distribution
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Technology Stack

- **Backend**: Python with Flask framework
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript with Bootstrap
- **Data Visualization**: Chart.js
- **API Integration**: REST Countries API
- **Deployment**: Gunicorn web server

## Project Structure

```
country-data-aggregator/
├── app.py                 # Application configuration
├── main.py                # Application entry point
├── models.py              # Database models
├── routes/                # Route handlers
│   ├── api.py             # API endpoints
│   └── views.py           # Frontend view routes
├── services/              # Business logic
│   ├── data_fetcher.py    # API data fetching 
│   └── data_processor.py  # Data processing and storage
├── static/                # Static assets
│   ├── css/               # CSS styles
│   └── js/                # JavaScript files
└── templates/             # HTML templates
    ├── base.html          # Base template
    ├── index.html         # Dashboard page
    ├── country_list.html  # Country listing page
    └── country_detail.html # Country detail page
```

## Getting Started

See the [User Guide](docs/user_guide.md) for detailed instructions on using the application.

For API documentation, refer to the [API Documentation](docs/api_docs.md).

The database schema is documented in the [Database Schema](docs/database_schema.md) file.

If you encounter any issues, please check the [Error Handling Guide](docs/error_handling.md).

## License

This project is licensed under the MIT License - see the LICENSE file for details.