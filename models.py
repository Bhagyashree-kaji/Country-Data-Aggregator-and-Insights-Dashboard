from app import db
from datetime import datetime

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
    
    def __repr__(self):
        return f"<Country {self.name}>"
    
    def to_dict(self):
        """Convert Country object to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "official_name": self.official_name,
            "capital": self.capital,
            "region": self.region,
            "subregion": self.subregion,
            "population": self.population,
            "area": self.area,
            "flag_emoji": self.flag_emoji,
            "flag_url": self.flag_url,
            "country_code": self.country_code,
            "currencies": self.currencies,
            "languages": self.languages,
            "independent": self.independent,
            "un_member": self.un_member,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None
        }
