import logging
from flask import Blueprint, jsonify, request, current_app
from models import Country
from app import db
from services.data_fetcher import RestCountriesAPI
from services.data_processor import CountryDataProcessor

# Set up logger
logger = logging.getLogger(__name__)

# Create blueprint
api_bp = Blueprint('api', __name__)

@api_bp.route('/refresh', methods=['POST'])
def refresh_countries():
    """
    Refresh country data from the REST Countries API.
    
    Returns:
        JSON response with refresh status.
    """
    try:
        # Fetch all countries data
        countries_data = RestCountriesAPI.retry_fetch(RestCountriesAPI.fetch_all_countries)
        
        if not countries_data:
            return jsonify({
                'success': False,
                'message': 'Failed to fetch country data from API'
            }), 500
        
        # Process and save country data
        processed_countries = CountryDataProcessor.process_countries_list(countries_data)
        saved_count = CountryDataProcessor.save_countries_to_db(processed_countries)
        
        return jsonify({
            'success': True,
            'message': f'Successfully refreshed {saved_count} countries data',
            'total_countries': len(countries_data),
            'saved_countries': saved_count
        })
    
    except Exception as e:
        logger.error(f"Error refreshing countries data: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error refreshing countries data: {str(e)}'
        }), 500

@api_bp.route('/countries', methods=['GET'])
def get_countries():
    """
    Get all countries or filter by region.
    
    Query Parameters:
        region (str, optional): Filter countries by region.
        sort (str, optional): Sort field (name, population, area).
        order (str, optional): Sort order (asc, desc).
        
    Returns:
        JSON response with countries data.
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
        
        # Convert to dict
        countries_data = [country.to_dict() for country in countries]
        
        return jsonify({
            'success': True,
            'count': len(countries_data),
            'data': countries_data
        })
    
    except Exception as e:
        logger.error(f"Error getting countries: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error getting countries: {str(e)}'
        }), 500

@api_bp.route('/countries/<string:name>', methods=['GET'])
def get_country(name):
    """
    Get a specific country by name.
    
    Args:
        name (str): Name of the country.
        
    Returns:
        JSON response with country data.
    """
    try:
        # Search for country by name
        country = Country.query.filter(Country.name.ilike(f"%{name}%")).first()
        
        if not country:
            return jsonify({
                'success': False,
                'message': f'Country {name} not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': country.to_dict()
        })
    
    except Exception as e:
        logger.error(f"Error getting country {name}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error getting country: {str(e)}'
        }), 500

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Get statistics about countries.
    
    Returns:
        JSON response with statistics.
    """
    try:
        # Get total count
        total_countries = Country.query.count()
        
        # Get region counts
        region_query = db.session.query(
            Country.region, 
            db.func.count(Country.id).label('count')
        ).group_by(Country.region).all()
        
        region_stats = [{'region': region, 'count': count} for region, count in region_query]
        
        # Get population stats
        total_population = db.session.query(db.func.sum(Country.population)).scalar() or 0
        avg_population = db.session.query(db.func.avg(Country.population)).scalar() or 0
        
        # Get area stats
        total_area = db.session.query(db.func.sum(Country.area)).scalar() or 0
        avg_area = db.session.query(db.func.avg(Country.area)).scalar() or 0
        
        return jsonify({
            'success': True,
            'stats': {
                'total_countries': total_countries,
                'regions': region_stats,
                'population': {
                    'total': total_population,
                    'average': avg_population
                },
                'area': {
                    'total': total_area,
                    'average': avg_area
                }
            }
        })
    
    except Exception as e:
        logger.error(f"Error getting statistics: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error getting statistics: {str(e)}'
        }), 500

@api_bp.route('/regions', methods=['GET'])
def get_regions():
    """
    Get all unique regions.
    
    Returns:
        JSON response with regions.
    """
    try:
        regions = db.session.query(Country.region).distinct().all()
        region_list = [region[0] for region in regions if region[0]]
        
        return jsonify({
            'success': True,
            'data': region_list
        })
    
    except Exception as e:
        logger.error(f"Error getting regions: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error getting regions: {str(e)}'
        }), 500
