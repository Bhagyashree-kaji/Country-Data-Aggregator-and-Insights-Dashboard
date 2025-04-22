# User Guide - Country Data Aggregator

This guide provides detailed instructions on how to use the Country Data Aggregator and Insights Dashboard.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [Country List](#country-list)
4. [Country Detail](#country-detail)
5. [Refreshing Data](#refreshing-data)
6. [Troubleshooting](#troubleshooting)

## Getting Started

When you first access the application, you'll need to load the initial country data:

1. Navigate to the dashboard (home page)
2. Click the "Load Initial Data" button
3. Wait for the data to be fetched from the REST Countries API
4. Once completed, you'll be redirected to the dashboard with visualizations

## Dashboard Overview

The dashboard provides a comprehensive overview of global country data:

### Statistics Cards
- **Total Countries**: Number of countries in the database
- **Total Population**: Sum of all countries' populations
- **Average Population**: Average population per country
- **Total Regions**: Number of distinct geographical regions

### Charts
- **Countries by Region**: Doughnut chart showing distribution of countries across regions
- **Top 10 Countries by Population**: Bar chart showing most populous countries
- **Top 10 Countries by Area**: Bar chart showing largest countries by area
- **Top 10 Countries by Population Density**: Bar chart showing most densely populated countries

### Quick Access
- **Explore by Region**: Direct links to filter countries by specific regions
- **View Countries**: Links to the country list with different sorting options

## Country List

The country list page allows you to browse and filter all countries:

### Filtering and Sorting
1. Use the **Region** dropdown to filter countries by geographical region
2. Use the **Sort By** dropdown to sort by name, population, area, or region
3. Use the **Order** dropdown to choose ascending or descending order
4. Click **Apply Filters** to update the list

### View Options
- Toggle between **Table View** and **Card View** using the switch in the top right
- Table view provides a compact listing with key information
- Card view provides a more visual representation with essential details

### Country Details
- Click the **Details** button for any country to view more information

## Country Detail

The country detail page provides comprehensive information about a specific country:

### Basic Information
- Country name, official name, and flag
- Capital, region, and subregion
- Population, area, and population density
- Country code and other identifiers

### Additional Information
- Currencies used in the country
- Languages spoken
- Independence and UN membership status
- Last data update timestamp

### Comparisons
- **Population Comparison**: Chart comparing the country's population to regional average
- **Area Comparison**: Chart comparing the country's area to regional average
- **Similar Countries**: List of countries in the same region with similar characteristics

## Refreshing Data

To update the country data from the REST Countries API:

1. Click the **Refresh Data** button in the navigation bar
2. Wait for the data to be fetched and processed
3. The page will automatically reload when complete

## Troubleshooting

If you encounter issues:

- **No data displayed**: Ensure you've clicked "Load Initial Data" on the dashboard
- **Charts not loading**: Check your internet connection and browser JavaScript settings
- **Slow performance**: The application may be processing a large amount of data, especially during initial load
- **Display issues**: Try refreshing the page or using a different browser

For technical issues, please refer to the [Error Handling Guide](error_handling.md).