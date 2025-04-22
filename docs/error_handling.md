# Error Handling Guide

This document provides information about common errors in the Country Data Aggregator application and how to resolve them.

## Table of Contents

1. [API Errors](#api-errors)
2. [Database Errors](#database-errors)
3. [Frontend Errors](#frontend-errors)
4. [External API Issues](#external-api-issues)
5. [Deployment Issues](#deployment-issues)

## API Errors

### Error: Failed to fetch country data from API

**Problem**: The application cannot retrieve data from the REST Countries API.

**Possible Causes**:
- Internet connectivity issues
- REST Countries API is down or has changed
- Request timeout

**Solution**:
1. Check your internet connection
2. Visit [REST Countries API](https://restcountries.com) to verify it's operational
3. Try refreshing the data again using the "Refresh Data" button
4. Check browser console for specific error messages

### Error: Country {name} not found

**Problem**: A specific country could not be found in the database.

**Possible Causes**:
- The country name is misspelled
- The country data hasn't been loaded yet
- The country may be listed under a different name

**Solution**:
1. Check the spelling of the country name
2. Ensure you've loaded the initial data via the dashboard
3. Try searching for partial names (e.g., "States" instead of "United States")
4. Check the country list for the correct country name

## Database Errors

### Error: Database connection failed

**Problem**: The application cannot connect to the PostgreSQL database.

**Possible Causes**:
- Database server is not running
- Incorrect database credentials
- Missing environment variables

**Solution**:
1. Verify the PostgreSQL service is running
2. Check that DATABASE_URL environment variable is correctly set
3. Ensure database credentials are correct
4. Check database logs for any specific errors

### Error: Duplicate key value violates unique constraint

**Problem**: An attempt to insert a duplicate country name.

**Possible Causes**:
- Country already exists in the database
- Data refresh operation has a conflict

**Solution**:
This is typically handled automatically by the application, which updates existing countries rather than creating duplicates. If you see this error in logs, it's usually informational and doesn't require action.

## Frontend Errors

### Error: Charts not displaying

**Problem**: Dashboard or country detail charts are not rendering.

**Possible Causes**:
- JavaScript is disabled in the browser
- Incomplete data in the database
- Browser compatibility issues

**Solution**:
1. Ensure JavaScript is enabled in your browser
2. Check browser console for specific errors
3. Refresh the page
4. Try a different modern browser (Chrome, Firefox, Edge)
5. Make sure you've loaded the initial data

### Error: "Loading..." message doesn't go away

**Problem**: The loading indicator remains on screen indefinitely.

**Possible Causes**:
- Network request failed
- JavaScript error prevented completion
- Server is still processing a large dataset

**Solution**:
1. Check your internet connection
2. Review browser console for JavaScript errors
3. Refresh the page
4. If the issue persists, restart the application

## External API Issues

### Error: Error refreshing countries data

**Problem**: The application couldn't refresh data from the REST Countries API.

**Possible Causes**:
- REST Countries API is down or has changed its endpoints
- Network connectivity issues
- Rate limiting or IP blocking

**Solution**:
1. Check if the REST Countries API is up at [restcountries.com](https://restcountries.com)
2. Verify your internet connection
3. Wait a few minutes and try again (in case of rate limiting)
4. Check the application logs for more specific error details

### Error: Data format has changed

**Problem**: The application receives data in an unexpected format from the API.

**Possible Causes**:
- The REST Countries API has updated its response format
- Partial or corrupted response

**Solution**:
This requires a code update if the API has permanently changed its format. Contact the application maintainer if you suspect this is the case.

## Deployment Issues

### Error: Application fails to start

**Problem**: The application server doesn't start correctly.

**Possible Causes**:
- Missing environment variables
- Port conflict
- Missing dependencies

**Solution**:
1. Ensure all required environment variables are set:
   - DATABASE_URL
   - FLASK_SECRET_KEY (optional)
2. Check if another application is using port 5000
3. Verify all dependencies are installed
4. Check application logs for specific startup errors

### Error: "Internal Server Error" (500)

**Problem**: The server encounters an unhandled exception.

**Possible Causes**:
- Bug in application code
- Database connection issues
- Missing data or unexpected data format

**Solution**:
1. Check the application logs for the specific error
2. Refresh the page
3. Try clearing browser cache
4. If the issue persists, contact the application maintainer with details from the logs

## Logging

The application uses Python's logging module to record important events and errors. Logs can be found:

- In the console output when running in development mode
- In application logs when deployed

To increase log verbosity for troubleshooting, you can modify the logging level in `app.py`.

## Getting Support

If you encounter an error not covered in this guide:

1. Check the application logs for detailed error messages
2. Search the project repository issues for similar problems
3. Create a new issue in the repository with:
   - Detailed description of the error
   - Steps to reproduce
   - Screenshots if applicable
   - Browser and OS information
   - Any relevant log output