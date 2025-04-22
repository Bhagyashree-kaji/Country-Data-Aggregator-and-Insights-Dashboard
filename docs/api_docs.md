# API Documentation - Country Data Aggregator

This document provides detailed information about the RESTful API endpoints available in the Country Data Aggregator.

## Base URL

All API endpoints are prefixed with `/api`.

## Authentication

The API currently does not require authentication.

## Response Format

All API responses follow this general structure:

```json
{
  "success": true|false,
  "message": "Optional status message",
  "data": [...],  // For successful data retrieval requests
  "count": 0,     // For list endpoints, indicates number of results
  "error": "..."  // For unsuccessful requests
}
```

## Endpoints

### Refresh Country Data

Fetches fresh data from the REST Countries API and updates the database.

- **URL:** `/api/refresh`
- **Method:** `POST`
- **Request Body:** None
- **Response:**
  ```json
  {
    "success": true,
    "message": "Successfully refreshed 250 countries data",
    "total_countries": 250,
    "saved_countries": 250
  }
  ```

### Get All Countries

Retrieves all countries with optional filtering and sorting.

- **URL:** `/api/countries`
- **Method:** `GET`
- **Query Parameters:**
  - `region` (optional): Filter by region (e.g., "Europe", "Asia")
  - `sort` (optional): Sort field (name, population, area)
  - `order` (optional): Sort order (asc, desc)
- **Response:**
  ```json
  {
    "success": true,
    "count": 250,
    "data": [
      {
        "id": 1,
        "name": "Afghanistan",
        "official_name": "Islamic Republic of Afghanistan",
        "capital": "Kabul",
        "region": "Asia",
        "subregion": "Southern Asia",
        "population": 40218234,
        "area": 652230.0,
        "flag_emoji": "🇦🇫",
        "flag_url": "https://flagcdn.com/af.svg",
        "country_code": "AFG",
        "currencies": "AFN (Afghan afghani, ؋)",
        "languages": "Pashto, Dari",
        "independent": true,
        "un_member": true,
        "last_updated": "2023-10-15T14:30:22.123456"
      },
      // ...more countries
    ]
  }
  ```

### Get Country by Name

Retrieves detailed information for a specific country.

- **URL:** `/api/countries/<name>`
- **Method:** `GET`
- **URL Parameters:**
  - `name`: The name of the country (case-insensitive, partial match supported)
- **Response:**
  ```json
  {
    "success": true,
    "data": {
      "id": 1,
      "name": "Afghanistan",
      "official_name": "Islamic Republic of Afghanistan",
      "capital": "Kabul",
      "region": "Asia",
      "subregion": "Southern Asia",
      "population": 40218234,
      "area": 652230.0,
      "flag_emoji": "🇦🇫",
      "flag_url": "https://flagcdn.com/af.svg",
      "country_code": "AFG",
      "currencies": "AFN (Afghan afghani, ؋)",
      "languages": "Pashto, Dari",
      "independent": true,
      "un_member": true,
      "last_updated": "2023-10-15T14:30:22.123456"
    }
  }
  ```

### Get Global Statistics

Retrieves aggregate statistics about countries.

- **URL:** `/api/stats`
- **Method:** `GET`
- **Response:**
  ```json
  {
    "success": true,
    "stats": {
      "total_countries": 250,
      "regions": [
        {
          "region": "Africa",
          "count": 54
        },
        {
          "region": "Americas",
          "count": 56
        },
        // ...more regions
      ],
      "population": {
        "total": 7794798729,
        "average": 31179194
      },
      "area": {
        "total": 148940000.0,
        "average": 595760.0
      }
    }
  }
  ```

### Get Unique Regions

Retrieves all unique regions.

- **URL:** `/api/regions`
- **Method:** `GET`
- **Response:**
  ```json
  {
    "success": true,
    "data": [
      "Africa",
      "Americas",
      "Antarctic",
      "Asia",
      "Europe",
      "Oceania"
    ]
  }
  ```

## Error Handling

If an error occurs, the API will return a response with `success: false` and an error message:

```json
{
  "success": false,
  "message": "Error description"
}
```

Common HTTP status codes:
- `200 OK`: Request succeeded
- `400 Bad Request`: Invalid parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

## Rate Limiting

There are currently no rate limits on the API.

## Examples

### cURL Examples

Fetch all countries:
```bash
curl -X GET http://localhost:5000/api/countries
```

Fetch countries in Europe, sorted by population:
```bash
curl -X GET "http://localhost:5000/api/countries?region=Europe&sort=population&order=desc"
```

Refresh country data:
```bash
curl -X POST http://localhost:5000/api/refresh
```

## Changes and Deprecations

The API is currently in v1 and there are no deprecated endpoints.