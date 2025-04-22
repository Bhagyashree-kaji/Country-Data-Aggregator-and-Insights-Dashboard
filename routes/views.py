import logging
from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import Country
from app import db
from services.data_fetcher import RestCountriesAPI
from services.data_processor import CountryDataProcessor

# Set up logger
logger = logging.getLogger(__name__)

# Create blueprint
views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    """
    Render the dashboard homepage.
    
    Returns:
        Rendered dashboard template.
    """
    # Get statistics for dashboard
    try:
        total_countries = Country.query.count()
        regions = db.session.query(Country.region).distinct().all()
        region_list = [region[0] for region in regions if region[0]]
        
        # Check if we need to load initial data
        if total_countries == 0:
            initial_load = True
        else:
            initial_load = False
        
        return render_template(
            'index.html', 
            total_countries=total_countries,
            regions=region_list,
            initial_load=initial_load
        )
    
    except Exception as e:
        logger.error(f"Error loading dashboard: {str(e)}")
        return render_template('index.html', error=str(e))

@views_bp.route('/countries')
def country_list():
    """
    Render the countries list page.
    
    Query Parameters:
        region (str, optional): Filter countries by region.
        sort (str, optional): Sort field (name, population, area).
        order (str, optional): Sort order (asc, desc).
    
    Returns:
        Rendered country list template.
    """
    try:
        # Get query parameters
        region = request.args.get('region')
        sort_by = request.args.get('sort', 'name')
        order = request.args.get('order', 'asc')
        
        # Start with base query
        query = Country.query
        
        # Apply region filter if provided
        if region:
            query = query.filter(Country.region == region)
        
        # Apply sorting
        valid_sort_fields = {'name', 'population', 'area', 'region'}
        if sort_by in valid_sort_fields:
            sort_field = getattr(Country, sort_by)
            
            if order.lower() == 'desc':
                query = query.order_by(sort_field.desc())
            else:
                query = query.order_by(sort_field.asc())
        
        # Execute query
        countries = query.all()
        
        # Get regions for filter dropdown
        regions = db.session.query(Country.region).distinct().all()
        region_list = [region[0] for region in regions if region[0]]
        
        return render_template(
            'country_list.html',
            countries=countries,
            regions=region_list,
            current_region=region,
            current_sort=sort_by,
            current_order=order
        )
    
    except Exception as e:
        logger.error(f"Error loading countries list: {str(e)}")
        return render_template('country_list.html', error=str(e))

@views_bp.route('/countries/<string:name>')
def country_detail(name):
    """
    Render the country detail page.
    
    Args:
        name (str): Name of the country.
    
    Returns:
        Rendered country detail template.
    """
    try:
        # Search for country by name
        country = Country.query.filter(Country.name.ilike(f"%{name}%")).first()
        
        if not country:
            flash(f'Country {name} not found', 'danger')
            return redirect(url_for('views.country_list'))
        
        return render_template('country_detail.html', country=country)
    
    except Exception as e:
        logger.error(f"Error loading country detail for {name}: {str(e)}")
        return render_template('country_detail.html', error=str(e))
