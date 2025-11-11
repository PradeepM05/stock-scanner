# Enhanced Configuration File
# Pre-filtered stock discovery via Finviz/Screener.in - 100% FREE!

# =============================================================================
# MARKET SELECTION
# =============================================================================
MARKET = "INDIA"  # Options: "US", "INDIA", or "BOTH"

# =============================================================================
# API CONFIGURATION FOR DYNAMIC STOCK DISCOVERY
# =============================================================================

# US Market Data Sources (Multiple options for redundancy)
US_DATA_SOURCES = {
    'primary': 'yfinance_screener',      # Free, no key needed
    'secondary': 'finviz',                # Free web scraping
    'tertiary': 'financial_modeling_prep' # Requires free API key
}

# India Market Data Sources
INDIA_DATA_SOURCES = {
    'primary': 'nse_india',               # NSE India official API
    'secondary': 'bse_api',               # BSE API
    'tertiary': 'screener_in'             # Screener.in web scraping
}

# API Keys (Optional - most work without keys)
API_KEYS = {
    'financial_modeling_prep': None,  # Get free key from financialmodelingprep.com
    'alpha_vantage': None,             # Get free key from alphavantage.co
    'polygon': None                     # Get free key from polygon.io
}

# =============================================================================
# SCREENING CRITERIA - These will be sent to APIs
# =============================================================================

# US Market Filters
US_FILTERS = {
    # Market Cap
    'market_cap_min': 300_000_000,      # $300M
    'market_cap_max': 10_000_000_000,   # $10B
    
    # Liquidity
    'volume_min': 500_000,               # Minimum daily volume
    
    # Fundamentals
    'pe_ratio_max': 30,                  # Not overvalued
    'roe_min': 12,                       # % Return on Equity
    'debt_to_equity_max': 2.0,           # Manageable debt
    'revenue_growth_min': 10,            # % YoY growth
    'earnings_growth_min': 8,            # % YoY growth
    
    # Price Action
    'price_above_200ma': False,          # Optional: True to filter only uptrends
    'price_above_50ma': False,
    
    # Additional Quality Filters
    'operating_margin_min': 5,           # % Operating margin
    'current_ratio_min': 1.2,            # Liquidity ratio
    
    # Sector Diversification (Optional - leave empty for all sectors)
    'sectors_include': [],               # e.g., ['Technology', 'Healthcare', 'Industrials']
    'sectors_exclude': ['Real Estate'],  # Sectors to avoid
    
    # Country filters for US
    'countries': ['US']
}

# Indian Market Filters (Adjusted for Indian market dynamics)
INDIA_FILTERS = {
    # Market Cap (in INR)
    'market_cap_min': 1_000_000_000,     # ₹1,000 Cr (~$120M)
    'market_cap_max': 100_000_000_000,   # ₹1,00,000 Cr (~$12B)
    
    # Liquidity
    'volume_min': 50_000,                 # Minimum daily volume
    
    # Fundamentals
    'pe_ratio_max': 35,                   # Higher P/E acceptable in growth phase
    'roe_min': 12,                        # % Return on Equity
    'debt_to_equity_max': 1.5,            # More leverage acceptable
    'revenue_growth_min': 10,             # % YoY growth
    'earnings_growth_min': 8,             # % YoY growth
    
    # Price Action
    'price_above_200ma': False,
    'price_above_50ma': False,
    
    # Additional Filters
    'operating_margin_min': 5,
    'current_ratio_min': 1.0,             # Lower threshold for India
    
    # Sector Diversification
    'sectors_include': [],
    'sectors_exclude': [],
    
    # Specific to India
    'exchanges': ['NSE', 'BSE'],          # Both exchanges
    'indices_to_scan': [                  # Pull stocks from these indices
        'NIFTY500',
        'NIFTY_MIDCAP_100',
        'NIFTY_SMALLCAP_100',
        'NIFTY_MIDSMALLCAP_400'
    ]
}

# =============================================================================
# ADVANCED SCREENING OPTIONS
# =============================================================================

# Dynamic Universe Building
UNIVERSE_BUILDER = {
    'refresh_frequency': 'daily',         # How often to refresh stock universe
    'cache_results': True,                # Cache screened results
    'cache_duration_hours': 24,           # Cache validity
    'max_stocks_per_scan': 500,           # Limit for performance
    
    # Multi-stage filtering
    'use_progressive_filtering': True,    # Apply filters in stages
    'stage_1_filters': ['market_cap', 'volume', 'pe_ratio'],  # Quick filters first
    'stage_2_filters': ['roe', 'debt_to_equity', 'growth'],   # Detailed filters
    'stage_3_filters': ['technical', 'momentum'],              # Final filters
}

# Scoring Weights for API Results
API_RANKING_WEIGHTS = {
    'data_freshness': 0.10,               # Prefer recently updated data
    'data_completeness': 0.15,            # Prefer stocks with complete data
    'fundamental_score': 0.45,            # Your valuation score
    'technical_score': 0.30,              # Your technical score
}

# =============================================================================
# BACKUP/FALLBACK STRATEGY
# =============================================================================

# If API fails, use these exchanges as fallback
FALLBACK_EXCHANGES = {
    'US': ['NYSE', 'NASDAQ'],
    'INDIA': ['NSE']
}

# Maximum retries and timeout
API_RETRY_CONFIG = {
    'max_retries': 3,
    'timeout_seconds': 30,
    'backoff_multiplier': 2,              # Exponential backoff
}

# =============================================================================
# VALUATION & TECHNICAL SCORING (Keep your existing logic)
# =============================================================================

VALUATION_WEIGHTS = {
    'eps_growth_yoy': 25,
    'eps_growth_3y': 15,
    'roe': 20,
    'debt_equity': 15,
    'pe_vs_sector': 10,
    'peg_ratio': 10,
    'fcf_yield': 5
}

# US Thresholds
EPS_GROWTH_EXCELLENT = 15
EPS_GROWTH_GOOD = 10
EPS_GROWTH_3Y_EXCELLENT = 12
EPS_GROWTH_3Y_GOOD = 8
ROE_EXCELLENT = 20
ROE_GOOD = 15
DEBT_EQUITY_EXCELLENT = 0.5
DEBT_EQUITY_GOOD = 1.0
PE_SECTOR_EXCELLENT = 0.8       # P/E 80% of sector average or less
PE_SECTOR_GOOD = 1.0            # P/E at sector average or less
PEG_EXCELLENT = 1.0             # PEG ratio 1.0 or less
PEG_GOOD = 1.5                  # PEG ratio 1.5 or less
FCF_YIELD_EXCELLENT = 0.08      # 8% FCF yield or higher
FCF_YIELD_GOOD = 0.05           # 5% FCF yield or higher

# India Thresholds
INDIA_EPS_GROWTH_EXCELLENT = 12
INDIA_EPS_GROWTH_GOOD = 8
INDIA_EPS_GROWTH_3Y_EXCELLENT = 12
INDIA_EPS_GROWTH_3Y_GOOD = 8
INDIA_ROE_EXCELLENT = 18
INDIA_ROE_GOOD = 12
INDIA_DEBT_EQUITY_EXCELLENT = 0.7
INDIA_DEBT_EQUITY_GOOD = 1.5
INDIA_PE_SECTOR_EXCELLENT = 0.8
INDIA_PE_SECTOR_GOOD = 1.0
INDIA_PEG_EXCELLENT = 1.0
INDIA_PEG_GOOD = 1.5
INDIA_FCF_YIELD_EXCELLENT = 0.08
INDIA_FCF_YIELD_GOOD = 0.05

# Bonus Points Thresholds
SHORT_INTEREST_THRESHOLD = 10    # % of float
SHORT_INTEREST_BONUS = 5         # bonus points
INSTITUTIONAL_THRESHOLD = 50     # % held
INSTITUTIONAL_BONUS = 5          # bonus points
INSIDER_BUY_THRESHOLD = 2        # number of buy transactions
INSIDER_BUY_BONUS = 5            # bonus points

# Scoring Weights for Composite Score
VALUATION_WEIGHT = 0.60          # 60% weight on fundamentals
TECHNICAL_WEIGHT = 0.40          # 40% weight on technicals

# Market Regime Adjustments
MARKET_REGIME = {
    'block_buys_in_bear': False,       # If True, don't recommend BUY/STRONG_BUY in bearish market
    'bearish_adjustment': -10          # Point adjustment when market is bearish
}

# Technical Indicator Parameters
RSI_PERIOD = 14                  # RSI calculation period
MACD_FAST = 12                  # MACD fast EMA period
MACD_SLOW = 26                  # MACD slow EMA period
MACD_SIGNAL = 9                 # MACD signal line period
ADX_PERIOD = 14                 # ADX calculation period

# Action Thresholds (Keep your existing)
ACTION_THRESHOLDS = {
    'STRONG_BUY': {
        'valuation_min': 80,
        'technical_min': 70,
        'description': 'Ultra high conviction - Best opportunities',
        'needs_deep_analysis': True
    },
    'BUY': {
        'valuation_min': 70,
        'technical_min': 60,
        'description': 'High conviction - Quality stocks with good entry',
        'needs_deep_analysis': True
    },
    'WATCH': {
        'valuation_min': 70,
        'technical_min': 40,
        'technical_max': 60,
        'description': 'Good fundamentals, waiting for better technical setup',
        'needs_deep_analysis': False
    },
    'WAIT': {
        'valuation_min': 70,
        'technical_max': 40,
        'description': 'Great company, wrong time',
        'needs_deep_analysis': False
    }
}

# Output
TOP_N_STOCKS = 20
OUTPUT_FILE = "../output/stock_picks.csv"
MARKET_INDEX = "SPY"  # Will be set based on market

# =============================================================================
# HARDCODED STOCK UNIVERSES (Fallback for main.py)
# =============================================================================

# US Stock Universe - Popular small/mid-cap stocks across sectors
US_STOCK_UNIVERSE = [
    # Technology
    'APPN', 'DOCN', 'FROG', 'GTLB', 'PATH', 'PCOR', 'QLYS', 'CYBR', 'FFIV', 'CRUS', 'LITE', 'MTSI', 'SMTC', 'CEVA',
    # Healthcare
    'ACAD', 'ALKS', 'BEAM', 'CRSP', 'FOLD', 'IONS', 'KRYS', 'NTLA', 'RARE', 'SRPT', 'UTHR', 'XENE', 'YMAB',
    # Biotech/Medical Devices
    'DXCM', 'GMED', 'HOLX', 'ICUI', 'LMAT', 'NVST', 'NVCR', 'PODD', 'STAA', 'TMDX', 'VCYT',
    # Industrials
    'ATRO', 'AIT', 'ATKR', 'BMI', 'CR', 'FLS', 'GGG', 'GNRC', 'ITT', 'PRIM', 'RBC', 'ROP', 'TTEK', 'UFPI', 'WSO',
    # Consumer Discretionary
    'AGCO', 'CMCO', 'EXPO', 'MLI', 'BOOT', 'BURL', 'FIVE', 'GES', 'LCII', 'OLLI', 'RVLV', 'SCVL', 'UPBD', 'W',
    # Consumer Staples & Restaurants
    'ANF', 'BBWI', 'DKS', 'LAD', 'SIG', 'TSCO', 'BLMN', 'CAKE', 'CBRL', 'DENN', 'DIN', 'PLAY', 'TXRH', 'WEN', 'WING',
    # Financial Services
    'ABCB', 'BANR', 'CADE', 'CASH', 'CBSH', 'CVBF', 'EWBC', 'FBK', 'FFIN', 'FHN', 'GBCI', 'HBAN', 'HOMB', 'IBOC', 'ONB', 'OZK',
    'SFNC', 'SNV', 'UBSI', 'AFRM', 'FOUR', 'LC', 'LU', 'MKTX', 'SOFI', 'UPST', 'VIRT', 'NU',
    # Insurance
    'ACGL', 'AFG', 'AXS', 'BRO', 'KNSL', 'PRI', 'RLI', 'RYAN', 'WRB',
    # Energy & Utilities
    'AROC', 'CLB', 'FLNG', 'FTI', 'HP', 'LBRT', 'NBR', 'NE', 'PTEN', 'RIG',
    # Clean Energy
    'ARRY', 'ENPH', 'FSLR', 'RUN', 'SEDG', 'SHLS', 'PLUG', 'BE',
    # Materials & Chemicals
    'ALB', 'ASIX', 'CE', 'FUL', 'HUN', 'MEOH', 'OLN', 'RPM', 'SXT', 'TROX', 'WLK',
    # Diversified
    'AVNT', 'CGNT', 'HWKN', 'BCPC', 'ECL', 'ESI',
    # Real Estate & REIT
    'CCI', 'DLR', 'PSA', 'SBAC', 'SPG', 'VTR'
]

# India Stock Universe - Popular NSE-listed stocks
INDIA_STOCK_UNIVERSE = [
    # IT/Tech
    'PERSISTENT.NS', 'COFORGE.NS', 'MPHASIS.NS', 'LTTS.NS', 'CYIENT.NS', 'TATAELXSI.NS', 'SONATSOFTW.NS',
    'HAPPSTMNDS.NS', 'INTELLECT.NS', 'ROUTE.NS',
    # Pharma
    'ALKEM.NS', 'TORNTPHARM.NS', 'LALPATHLAB.NS', 'METROPOLIS.NS', 'THYROCARE.NS', 'AUROPHARMA.NS',
    'ABBOTINDIA.NS', 'GLAXO.NS', 'SANOFI.NS', 'PFIZER.NS', 'IPCALAB.NS', 'LAURUSLABS.NS', 'GLAND.NS',
    # Consumer & Retail
    'TRENT.NS', 'JUBLFOOD.NS', 'RELAXO.NS', 'PAGEIND.NS', 'VMART.NS', 'WESTLIFE.NS', 'SAPPHIRE.NS', 'RAYMOND.NS',
    # Auto & Auto Components
    'MOTHERSON.NS', 'BOSCHLTD.NS', 'EXIDEIND.NS', 'BALKRISIND.NS', 'MRF.NS', 'APOLLOTYRE.NS', 'CEATLTD.NS',
    'ENDURANCE.NS', 'SCHAEFFLER.NS', 'SKFINDIA.NS',
    # Chemicals & Specialty Chemicals
    'DEEPAKNTR.NS', 'SRF.NS', 'NAVINFLUOR.NS', 'ATUL.NS', 'PIIND.NS', 'GNFC.NS', 'FLUOROCHEM.NS',
    'TATACHEM.NS', 'BASF.NS',
    # Construction & Engineering
    'NCC.NS', 'IRCON.NS', 'NBCC.NS', 'ASHOKLEY.NS', 'GRINDWELL.NS',
    # Steel & Metals
    'JINDALSTEL.NS', 'SAIL.NS', 'NMDC.NS', 'HINDZINC.NS', 'VEDL.NS', 'NATIONALUM.NS', 'HINDALCO.NS',
    'RATNAMANI.NS', 'WELCORP.NS',
    # Digital & Others
    'AFFLE.NS', 'GOKEX.NS', 'SPANDANA.NS', 'KPRMILL.NS', 'TRIDENT.NS',
    # Textiles
    'CENTURYPLY.NS',
    # Cement
    'HEIDELBERG.NS', 'STARCEMENT.NS', 'NUVOCO.NS', 'RAMCOCEM.NS', 'JKCEMENT.NS',
    # Electrical & Power Equipment
    'VOLTAS.NS', 'HAVELLS.NS', 'CROMPTON.NS', 'POLYCAB.NS', 'KEI.NS',
    # Financial Services
    'CHOLAFIN.NS', 'MUTHOOTFIN.NS', 'MANAPPURAM.NS', 'ICICIGI.NS', 'SBICARD.NS',
    'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'HDFCLIFE.NS', 'SBILIFE.NS'
]

# US Market Cap Defaults
US_MARKET_CAP_MIN = 300_000_000      # $300M
US_MARKET_CAP_MAX = 10_000_000_000   # $10B
US_MIN_AVG_VOLUME = 500_000

# India Market Cap Defaults
INDIA_MARKET_CAP_MIN = 1_000_000_000     # ₹1,000 Cr
INDIA_MARKET_CAP_MAX = 100_000_000_000   # ₹1,00,000 Cr
INDIA_MIN_AVG_VOLUME = 50_000

# =============================================================================
# AUTO-APPLY MARKET-SPECIFIC SETTINGS
# =============================================================================

def get_market_config(market='US'):
    """Return market-specific configuration"""
    if market == 'US':
        return {
            'filters': US_FILTERS,
            'data_sources': US_DATA_SOURCES,
            'market_index': 'SPY',
            'output_file': '../output/stock_picks_us.csv'
        }
    elif market == 'INDIA':
        return {
            'filters': INDIA_FILTERS,
            'data_sources': INDIA_DATA_SOURCES,
            'market_index': '^NSEI',
            'output_file': '../output/stock_picks_india.csv'
        }
    elif market == 'BOTH':
        return {
            'filters': {**US_FILTERS, **INDIA_FILTERS},
            'data_sources': {**US_DATA_SOURCES, **INDIA_DATA_SOURCES},
            'market_index': 'SPY',
            'output_file': '../output/stock_picks_combined.csv'
        }
    
    raise ValueError(f"Unknown market: {market}")