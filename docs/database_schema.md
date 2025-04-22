# Database Schema Documentation

This document describes the database schema used in the Country Data Aggregator application.

## Overview

The application uses a PostgreSQL database with SQLAlchemy as the ORM (Object-Relational Mapping) layer. The database stores country information fetched from the REST Countries API.

## Database Configuration

The database connection is configured in `app.py` using environment variables:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
```

## Table Structure

### Country Table

The `country` table stores information about all countries.

#### Columns

| Column Name | Data Type | Constraints | Description |
|-------------|-----------|------------|-------------|
| id | INTEGER | PRIMARY KEY | Unique identifier for the country |
| name | VARCHAR(100) | NOT NULL, UNIQUE | Common name of the country |
| official_name | VARCHAR(200) | | Official name of the country |
| capital | VARCHAR(100) | | Capital city |
| region | VARCHAR(100) | | Geographic region |
| subregion | VARCHAR(100) | | Geographic subregion |
| population | INTEGER | | Total population |
| area | FLOAT | | Land area in square kilometers |
| flag_emoji | VARCHAR(10) | | Flag emoji character |
| flag_url | VARCHAR(255) | | URL to the SVG flag image |
| country_code | VARCHAR(3) | | ISO 3-letter country code |
| currencies | VARCHAR(255) | | Comma-separated list of currencies |
| languages | VARCHAR(255) | | Comma-separated list of languages |
| independent | BOOLEAN | DEFAULT TRUE | Whether the country is independent |
| un_member | BOOLEAN | DEFAULT TRUE | Whether the country is a UN member |
| last_updated | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | When the record was last updated |

#### Indexes

- Primary Key: `id`
- Unique Index: `name`
- Index: `region`

#### SQL Definition

```sql
CREATE TABLE country (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    official_name VARCHAR(200),
    capital VARCHAR(100),
    region VARCHAR(100),
    subregion VARCHAR(100),
    population INTEGER,
    area FLOAT,
    flag_emoji VARCHAR(10),
    flag_url VARCHAR(255),
    country_code VARCHAR(3),
    currencies VARCHAR(255),
    languages VARCHAR(255),
    independent BOOLEAN DEFAULT TRUE,
    un_member BOOLEAN DEFAULT TRUE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_country_region ON country(region);
```

## SQLAlchemy Model

The ORM model for the Country table is defined in `models.py`:

```python
class Country(db.Model):
    """Model for country data."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    official_name = db.Column(db.String(200))
    capital = db.Column(db.String(100))
    region = db.Column(db.String(100))
    subregion = db.Column(db.String(100))
    population = db.Column(db.Integer)
    area = db.Column(db.Float)
    flag_emoji = db.Column(db.String(10))
    flag_url = db.Column(db.String(255))
    country_code = db.Column(db.String(3))
    currencies = db.Column(db.String(255))
    languages = db.Column(db.String(255))
    independent = db.Column(db.Boolean, default=True)
    un_member = db.Column(db.Boolean, default=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
```

## Data Relationships

The current schema has a single table with no relationships to other tables. Future versions may include:

- Relationships to continent/region tables
- Many-to-many relationships for currencies and languages
- Historical data tracking

## Database Migrations

The application does not currently use a migration framework. The tables are created directly through SQLAlchemy's `create_all()` method:

```python
with app.app_context():
    db.create_all()
```

For future schema changes, it is recommended to implement a proper migration system using a tool like Alembic or Flask-Migrate.

## Query Patterns

Common query patterns used in the application:

### Get All Countries
```python
Country.query.all()
```

### Filter by Region
```python
Country.query.filter(Country.region == region).all()
```

### Sort by Field
```python
Country.query.order_by(Country.population.desc()).all()
```

### Get Country by Name (Case-insensitive)
```python
Country.query.filter(Country.name.ilike(f"%{name}%")).first()
```

### Get Regional Statistics
```python
db.session.query(
    Country.region, 
    db.func.count(Country.id).label('count')
).group_by(Country.region).all()
```

## Performance Considerations

- The database includes appropriate indexes on frequently queried fields
- The connection pool is configured with recycling to prevent stale connections
- Pre-ping is enabled to detect and replace broken connections
- Text fields have appropriate size limits to optimize storage

## Future Schema Enhancements

Potential improvements to the database schema:

1. Normalize currencies and languages into separate tables
2. Add versioning for historical data tracking
3. Add geographical coordinates for mapping functionality
4. Add table for user preferences and saved favorites
5. Implement full-text search capabilities