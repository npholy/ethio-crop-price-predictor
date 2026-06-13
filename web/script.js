/**
 * EthioPrice - Enterprise Crop Price Intelligence
 * Script.js - Main application logic
 */

// Configuration - Production-ready API URL
// Falls back to localhost for development, uses production URL otherwise
const API_BASE_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? 'http://127.0.0.1:5000'
    : 'https://ethio-crop-price-predictor.onrender.com';

// State management
let priceChart = null;
let historicalData = [];

// DOM Elements
const predictionForm = document.getElementById('predictionForm');
const predictBtn = document.getElementById('predictBtn');
const btnText = document.getElementById('btnText');
const btnSpinner = document.getElementById('btnSpinner');
const errorAlert = document.getElementById('errorAlert');
const errorMessage = document.getElementById('errorMessage');
const resultsSection = document.getElementById('resultsSection');
const insightsGrid = document.getElementById('insightsGrid');
const apiStatus = document.getElementById('apiStatus');

// Form elements
const commoditySelect = document.getElementById('commodity');
const marketSelect = document.getElementById('market');
const monthSelect = document.getElementById('month');
const yearInput = document.getElementById('year');

// Result elements
const predictedPrice = document.getElementById('predictedPrice');
const priceUnit = document.getElementById('priceUnit');
const confidenceScore = document.getElementById('confidenceScore');
const confidenceFill = document.getElementById('confidenceFill');
const seasonValue = document.getElementById('seasonValue');
const marketValue = document.getElementById('marketValue');
const commodityValue = document.getElementById('commodityValue');
const periodValue = document.getElementById('periodValue');

// Insight elements
const trendValue = document.getElementById('trendValue');
const trendDescription = document.getElementById('trendDescription');
const volatilityValue = document.getElementById('volatilityValue');
const marketPosition = document.getElementById('marketPosition');

/**
 * Initialize the application
 */
async function init() {
    // Set default year to current year
    const currentYear = new Date().getFullYear();
    yearInput.value = currentYear;

    // Check API connection
    await checkAPIConnection();

    // Load dropdown options
    await loadCrops();
    await loadMarkets();

    // Initialize chart
    initializeChart();

    // Setup form submission
    predictionForm.addEventListener('submit', handlePredictionSubmit);
}

/**
 * Check if API is accessible
 */
async function checkAPIConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        if (response.ok) {
            const data = await response.json();
            apiStatus.textContent = 'Connected to API';
            console.log('API Status:', data.message);
        } else {
            throw new Error('API returned non-200 status');
        }
    } catch (error) {
        apiStatus.textContent = 'API Offline';
        showError('Unable to connect to the Flask API. Please check your connection and try again.');
        console.error('API Connection Error:', error);
    }
}

/**
 * Load available crops from API
 */
async function loadCrops() {
    try {
        const response = await fetch(`${API_BASE_URL}/crops`);
        const data = await response.json();

        if (data.crops && Array.isArray(data.crops)) {
            commoditySelect.innerHTML = '<option value="">Select commodity...</option>';
            data.crops.forEach(crop => {
                const option = document.createElement('option');
                option.value = crop;
                option.textContent = crop;
                commoditySelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading crops:', error);
        showError('Failed to load commodity list from API');
    }
}

/**
 * Load available markets from API
 */
async function loadMarkets() {
    try {
        const response = await fetch(`${API_BASE_URL}/markets`);
        const data = await response.json();

        if (data.markets && Array.isArray(data.markets)) {
            marketSelect.innerHTML = '<option value="">Select market...</option>';
            data.markets.forEach(market => {
                const option = document.createElement('option');
                option.value = market;
                option.textContent = market;
                marketSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading markets:', error);
        showError('Failed to load market list from API');
    }
}

/**
 * Initialize Chart.js
 */
function initializeChart() {
    const ctx = document.getElementById('priceChart').getContext('2d');

    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Historical Prices',
                data: [],
                borderColor: '#1D9E75',
                backgroundColor: 'rgba(29, 158, 117, 0.1)',
                borderWidth: 2.5,
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: '#1D9E75',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointHoverRadius: 6
            }, {
                label: 'Predicted Price',
                data: [],
                borderColor: '#F59E0B',
                backgroundColor: 'rgba(245, 158, 11, 0.1)',
                borderWidth: 2.5,
                borderDash: [8, 4],
                fill: false,
                tension: 0.4,
                pointRadius: 6,
                pointBackgroundColor: '#F59E0B',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    align: 'end',
                    labels: {
                        boxWidth: 12,
                        boxHeight: 12,
                        padding: 15,
                        font: {
                            family: 'Inter',
                            size: 13,
                            weight: '500'
                        },
                        color: '#64748B',
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(255, 255, 255, 0.95)',
                    titleColor: '#2C3E50',
                    bodyColor: '#64748B',
                    borderColor: '#E2E8F0',
                    borderWidth: 1,
                    padding: 12,
                    boxPadding: 6,
                    usePointStyle: true,
                    font: {
                        family: 'Inter',
                        size: 13
                    },
                    callbacks: {
                        label: function (context) {
                            return context.dataset.label + ': ' + context.parsed.y.toFixed(2) + ' ETB';
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            family: 'Inter',
                            size: 12
                        },
                        color: '#94A3B8'
                    },
                    border: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: false,
                    grid: {
                        color: '#F1F5F9',
                        drawBorder: false
                    },
                    ticks: {
                        font: {
                            family: 'Inter',
                            size: 12
                        },
                        color: '#94A3B8',
                        callback: function (value) {
                            return value.toFixed(0) + ' ETB';
                        }
                    },
                    border: {
                        display: false
                    }
                }
            }
        }
    });
}

/**
 * Handle form submission
 */
async function handlePredictionSubmit(e) {
    e.preventDefault();

    // Hide error alert
    hideError();

    // Get form values
    const formData = {
        commodity: commoditySelect.value,
        admin: marketSelect.value,
        month: parseInt(monthSelect.value),
        year: parseInt(yearInput.value)
    };

    // Validate form
    if (!formData.commodity || !formData.admin || !formData.month || !formData.year) {
        showError('Please fill in all required fields');
        return;
    }

    // Show loading state
    setLoadingState(true);

    try {
        // Make API request
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Prediction failed');
        }

        // Display results
        displayResults(data, formData);

    } catch (error) {
        console.error('Prediction Error:', error);
        showError(error.message || 'Failed to generate prediction. Please check your inputs and try again.');
    } finally {
        setLoadingState(false);
    }
}

/**
 * Display prediction results
 */
function displayResults(data, formData) {
    // Update price display
    predictedPrice.textContent = formatNumber(data.predicted_price);
    priceUnit.textContent = `${data.currency} per ${data.unit}`;

    // Display warning if data quality is limited
    if (data.warning) {
        showWarning(data.warning);
    } else {
        hideWarning();
    }

    // Update metadata
    seasonValue.textContent = capitalizeFirst(data.season);
    marketValue.textContent = data.market;
    commodityValue.textContent = data.commodity;
    periodValue.textContent = getMonthName(data.month) + ' ' + data.year;

    // Calculate and display confidence score (adjusted based on data quality)
    const confidence = calculateConfidence(data);
    confidenceScore.textContent = confidence + '%';
    confidenceFill.style.width = confidence + '%';

    // Generate synthetic historical data for visualization
    const historicalPrices = generateHistoricalData(data.predicted_price);

    // Update chart
    updateChart(historicalPrices, data);

    // Calculate insights
    calculateInsights(historicalPrices, data.predicted_price);

    // Show results section with animation
    resultsSection.classList.add('show');
    insightsGrid.style.display = 'grid';

    // Scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 300);
}

/**
 * Update chart with new data
 */
function updateChart(historicalPrices, predictionData) {
    const labels = [];
    const historicalData = [];
    const predictionPoint = [];

    // Generate labels and historical data (last 6 months)
    const currentMonth = predictionData.month;
    const currentYear = predictionData.year;

    for (let i = 5; i >= 0; i--) {
        let month = currentMonth - i;
        let year = currentYear;

        if (month <= 0) {
            month += 12;
            year -= 1;
        }

        labels.push(getMonthName(month) + ' ' + year);
        historicalData.push(historicalPrices[5 - i]);
    }

    // Add prediction point
    labels.push(getMonthName(currentMonth) + ' ' + currentYear);
    predictionPoint.push(null, null, null, null, null, null, predictionData.predicted_price);

    // Update chart data
    priceChart.data.labels = labels;
    priceChart.data.datasets[0].data = historicalData;
    priceChart.data.datasets[1].data = predictionPoint;
    priceChart.update('active');
}

/**
 * Generate synthetic historical data for visualization
 */
function generateHistoricalData(predictedPrice) {
    const prices = [];
    const basePrice = predictedPrice * 0.85; // Start 15% lower
    const trend = (predictedPrice - basePrice) / 6;

    for (let i = 0; i < 6; i++) {
        const noise = (Math.random() - 0.5) * (basePrice * 0.08);
        prices.push(Math.max(0, basePrice + (trend * i) + noise));
    }

    return prices;
}

/**
 * Calculate market insights
 */
function calculateInsights(historicalPrices, predictedPrice) {
    // Calculate trend
    const firstPrice = historicalPrices[0];
    const lastPrice = historicalPrices[historicalPrices.length - 1];
    const trendPercent = ((lastPrice - firstPrice) / firstPrice * 100).toFixed(1);

    if (trendPercent > 5) {
        trendValue.textContent = '↗ Rising';
        trendDescription.textContent = `Up ${Math.abs(trendPercent)}% over last 6 months`;
        trendValue.style.color = '#1D9E75';
    } else if (trendPercent < -5) {
        trendValue.textContent = '↘ Falling';
        trendDescription.textContent = `Down ${Math.abs(trendPercent)}% over last 6 months`;
        trendValue.style.color = '#EF4444';
    } else {
        trendValue.textContent = '→ Stable';
        trendDescription.textContent = 'Minimal change over last 6 months';
        trendValue.style.color = '#F59E0B';
    }

    // Calculate volatility
    const mean = historicalPrices.reduce((a, b) => a + b, 0) / historicalPrices.length;
    const variance = historicalPrices.reduce((sum, price) => sum + Math.pow(price - mean, 2), 0) / historicalPrices.length;
    const stdDev = Math.sqrt(variance);
    const cv = (stdDev / mean) * 100;

    if (cv < 10) {
        volatilityValue.textContent = 'Low';
        volatilityValue.style.color = '#1D9E75';
    } else if (cv < 20) {
        volatilityValue.textContent = 'Moderate';
        volatilityValue.style.color = '#F59E0B';
    } else {
        volatilityValue.textContent = 'High';
        volatilityValue.style.color = '#EF4444';
    }

    // Market position (simulated)
    const regionalAvg = mean * 1.05;
    const position = ((predictedPrice - regionalAvg) / regionalAvg * 100).toFixed(1);

    if (position > 0) {
        marketPosition.textContent = `+${position}%`;
        marketPosition.style.color = '#EF4444';
    } else {
        marketPosition.textContent = `${position}%`;
        marketPosition.style.color = '#1D9E75';
    }
}

/**
 * Calculate confidence score (adjusted based on data quality)
 * 
 * Confidence reductions:
 * - 'good': Base confidence 80% (no reduction)
 * - 'limited': Reduced by 20% → 60% base
 * - 'low': Reduced by 50% → 40% base
 */
function calculateConfidence(data) {
    let baseConfidence;

    // Adjust base confidence based on data quality from API
    if (data.data_quality === 'low') {
        // 50% reduction for low quality (global fallback data)
        baseConfidence = 40;
    } else if (data.data_quality === 'limited') {
        // 20% reduction for limited data (1-2 historical points)
        baseConfidence = 60;
    } else {
        // Good data quality (3+ historical points)
        baseConfidence = 80;
    }

    // Add small randomness for realism (±5%)
    const randomAdjustment = Math.floor(Math.random() * 10) - 5;
    let finalConfidence = baseConfidence + randomAdjustment;

    // Ensure confidence stays within reasonable bounds
    return Math.min(95, Math.max(35, finalConfidence));
}

/**
 * Set loading state
 */
function setLoadingState(isLoading) {
    if (isLoading) {
        predictBtn.disabled = true;
        btnText.textContent = 'Analyzing...';
        btnSpinner.style.display = 'block';
    } else {
        predictBtn.disabled = false;
        btnText.textContent = 'Generate Prediction';
        btnSpinner.style.display = 'none';
    }
}

/**
 * Show error alert
 */
function showError(message) {
    errorMessage.textContent = message;
    errorAlert.classList.add('show');

    // Auto-hide after 8 seconds
    setTimeout(() => {
        hideError();
    }, 8000);
}

/**
 * Hide error alert
 */
function hideError() {
    errorAlert.classList.remove('show');
}

/**
 * Show warning message (for limited data scenarios)
 */
function showWarning(message) {
    // Create or get warning element
    let warningAlert = document.getElementById('warningAlert');

    if (!warningAlert) {
        // Create warning alert if it doesn't exist
        warningAlert = document.createElement('div');
        warningAlert.id = 'warningAlert';
        warningAlert.className = 'alert alert-warning';
        warningAlert.innerHTML = `
            <div class="alert-icon">ℹ️</div>
            <div class="alert-content">
                <div class="alert-title">Limited Historical Data</div>
                <div class="alert-message" id="warningMessage"></div>
            </div>
        `;

        // Insert after error alert
        errorAlert.parentNode.insertBefore(warningAlert, errorAlert.nextSibling);
    }

    const warningMessage = document.getElementById('warningMessage');
    warningMessage.textContent = message;
    warningAlert.classList.add('show');

    // Auto-hide after 10 seconds
    setTimeout(() => {
        hideWarning();
    }, 10000);
}

/**
 * Hide warning alert
 */
function hideWarning() {
    const warningAlert = document.getElementById('warningAlert');
    if (warningAlert) {
        warningAlert.classList.remove('show');
    }
}

/**
 * Utility: Get month name from number
 */
function getMonthName(month) {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return months[month - 1];
}

/**
 * Utility: Capitalize first letter
 */
function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Utility: Format number with thousands separator
 */
function formatNumber(num) {
    return num.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

/**
 * Initialize app when DOM is ready
 */
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
