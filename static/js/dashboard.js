document.addEventListener('DOMContentLoaded', function() {
    // Fetch statistics data for the dashboard
    fetchStats();
    
    // Initialize charts
    initializeCharts();
});

/**
 * Fetch country statistics from the API
 */
function fetchStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateStatCards(data.stats);
                updateRegionCounts(data.stats.regions);
            } else {
                console.error('Error fetching stats:', data.message);
            }
        })
        .catch(error => {
            console.error('Error fetching stats:', error);
        });
}

/**
 * Update statistic cards with data
 */
function updateStatCards(stats) {
    // Update total population
    const totalPopulationElement = document.getElementById('total-population-stat');
    if (totalPopulationElement) {
        totalPopulationElement.textContent = formatNumber(stats.population.total);
    }
    
    // Update average population
    const avgPopulationElement = document.getElementById('avg-population-stat');
    if (avgPopulationElement) {
        avgPopulationElement.textContent = formatNumber(Math.round(stats.population.average));
    }
}

/**
 * Update region counts in the region list
 */
function updateRegionCounts(regions) {
    regions.forEach(region => {
        const regionElement = document.getElementById(`region-count-${region.region.replace(' ', '-').toLowerCase()}`);
        if (regionElement) {
            regionElement.textContent = region.count;
        }
    });
}

/**
 * Initialize all dashboard charts
 */
function initializeCharts() {
    // Fetch data for region chart
    fetch('/api/stats')
        .then(response => response.json())
        .then(statsData => {
            if (statsData.success) {
                initializeRegionChart(statsData.stats.regions);
            }
        })
        .catch(error => {
            console.error('Error fetching region data:', error);
        });
    
    // Fetch data for population chart
    fetch('/api/countries?sort=population&order=desc')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                initializePopulationChart(data.data.slice(0, 10));
                initializeAreaChart(data.data.sort((a, b) => b.area - a.area).slice(0, 10));
                initializeDensityChart(data.data);
            }
        })
        .catch(error => {
            console.error('Error fetching countries data:', error);
        });
}

/**
 * Initialize the region distribution chart
 */
function initializeRegionChart(regionsData) {
    const ctx = document.getElementById('regionChart');
    if (!ctx) return;
    
    const labels = regionsData.map(region => region.region);
    const data = regionsData.map(region => region.count);
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    '#6610f2', // Indigo
                    '#3b9ae8', // Blue
                    '#20c997', // Teal
                    '#fd7e14', // Orange
                    '#ffc107', // Yellow
                    '#e83e8c', // Pink
                    '#6f42c1', // Purple
                    '#17a2b8'  // Cyan
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw;
                            const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

/**
 * Initialize the population chart
 */
function initializePopulationChart(countries) {
    const ctx = document.getElementById('populationChart');
    if (!ctx) return;
    
    const labels = countries.map(country => country.name);
    const data = countries.map(country => country.population);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Population',
                data: data,
                backgroundColor: 'rgba(59, 154, 232, 0.7)',
                borderColor: 'rgba(59, 154, 232, 1)',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            if (value >= 1000000000) {
                                return (value / 1000000000).toFixed(1) + 'B';
                            } else if (value >= 1000000) {
                                return (value / 1000000).toFixed(1) + 'M';
                            } else if (value >= 1000) {
                                return (value / 1000).toFixed(1) + 'K';
                            }
                            return value;
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let value = context.raw;
                            return 'Population: ' + formatNumber(value);
                        }
                    }
                }
            }
        }
    });
}

/**
 * Initialize the area chart
 */
function initializeAreaChart(countries) {
    const ctx = document.getElementById('areaChart');
    if (!ctx) return;
    
    const labels = countries.map(country => country.name);
    const data = countries.map(country => country.area);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Area (km²)',
                data: data,
                backgroundColor: 'rgba(253, 126, 20, 0.7)',
                borderColor: 'rgba(253, 126, 20, 1)',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            if (value >= 1000000) {
                                return (value / 1000000).toFixed(1) + 'M';
                            } else if (value >= 1000) {
                                return (value / 1000).toFixed(1) + 'K';
                            }
                            return value;
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let value = context.raw;
                            return 'Area: ' + formatNumber(value) + ' km²';
                        }
                    }
                }
            }
        }
    });
}

/**
 * Initialize the population density chart
 */
function initializeDensityChart(countries) {
    const ctx = document.getElementById('densityChart');
    if (!ctx) return;
    
    // Calculate density and filter out countries with no area
    const countriesWithDensity = countries
        .filter(country => country.area && country.area > 0)
        .map(country => ({
            name: country.name,
            density: country.population / country.area
        }))
        .sort((a, b) => b.density - a.density)
        .slice(0, 10);
    
    const labels = countriesWithDensity.map(country => country.name);
    const data = countriesWithDensity.map(country => country.density);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Population Density (people/km²)',
                data: data,
                backgroundColor: 'rgba(32, 201, 151, 0.7)',
                borderColor: 'rgba(32, 201, 151, 1)',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            if (value >= 1000) {
                                return (value / 1000).toFixed(1) + 'K';
                            }
                            return value.toFixed(0);
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let value = context.raw;
                            return 'Density: ' + value.toFixed(2) + ' people/km²';
                        }
                    }
                }
            }
        }
    });
}

/**
 * Format numbers for display (adding commas, abbreviations)
 */
function formatNumber(number) {
    if (number >= 1000000000) {
        return (number / 1000000000).toFixed(2) + ' billion';
    } else if (number >= 1000000) {
        return (number / 1000000).toFixed(2) + ' million';
    } else if (number >= 1000) {
        return (number / 1000).toFixed(2) + ' thousand';
    }
    return number.toString();
}
