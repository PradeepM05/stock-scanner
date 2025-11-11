# Configuration File
# Now using 100% Yahoo Finance - no API key needed!

# =============================================================================
# MARKET SELECTION - Set dynamically via command-line argument
# =============================================================================
# Options: "US", "INDIA", or "BOTH"
# Usage: python main.py --market US
#        python main.py --market INDIA
#        python main.py --market BOTH
# 
# Default is set below but can be overridden
MARKET = "INDIA"  # Default market (will be overridden by CLI argument)

# =============================================================================
# US STOCKS CONFIGURATION
# =============================================================================

# Filters for Hidden Gems (US)
US_MARKET_CAP_MIN = 300_000_000  # $300M
US_MARKET_CAP_MAX = 10_000_000_000  # $10B
US_MIN_AVG_VOLUME = 500_000

# US Stock Universe - Curated Small/Mid-Cap Stocks ($300M - $10B Market Cap)
# Diversified across sectors for hidden gems hunting
US_STOCK_UNIVERSE = [
    # Technology - Software & Services
    'APPN', 'BILL', 'DOCN', 'FROG', 'GTLB', 'MNDY', 'PATH', 'PD', 'S', 'TENB',
    'TOST', 'U', 'ASAN', 'BLKB', 'COUP', 'FRSH', 'NCNO', 'PCOR', 'SMAR', 'WK',
    
    # Technology - Cybersecurity
    'CYBR', 'FFIV', 'RPD', 'SAIL', 'VRNS', 'ALRM', 'QLYS', 'RBRK', 'PING', 'EVBG',
    
    # Technology - Semiconductors & Hardware
    'ALGM', 'CRUS', 'DIOD', 'LITE', 'MTSI', 'NVTS', 'PLAB', 'SMTC', 'WOLF', 'CEVA',
    
    # Healthcare - Biotech
    'ACAD', 'ALKS', 'ARVN', 'BEAM', 'BGNE', 'BLUE', 'CRSP', 'EDIT', 'FOLD', 'IONS',
    'KRYS', 'LEGN', 'NTLA', 'RARE', 'SAGE', 'SRPT', 'UTHR', 'VRTX', 'XENE', 'YMAB',
    
    # Healthcare - Medical Devices & Equipment
    'AXNX', 'DXCM', 'GMED', 'HOLX', 'ICUI', 'ISRG', 'LMAT', 'NVST', 'NVCR', 'PODD',
    'STAA', 'TMDX', 'VCYT', 'IRTC', 'ATRC', 'OMCL', 'OFIX', 'ATEC', 'NEOG', 'NARI',
    
    # Healthcare - Services & Facilities
    'ACHC', 'AMED', 'CRVL', 'ENSG', 'HCAT', 'PDCO', 'PINC', 'RDNT', 'SEM', 'THC',
    
    # Industrials - Aerospace & Defense
    'AVAV', 'HWM', 'KTOS', 'LDOS', 'NPK', 'SPR', 'TGI', 'TXT', 'WWD', 'ATRO',
    
    # Industrials - Manufacturing & Equipment
    'AIT', 'ATKR', 'BMI', 'CR', 'FLS', 'GGG', 'GNRC', 'ITT', 'PRIM', 'RBC',
    'ROP', 'TTEK', 'UFPI', 'WSO', 'AGCO', 'ALG', 'BECN', 'CMCO', 'EXPO', 'MLI',
    
    # Consumer - Retail & E-commerce
    'BOOT', 'BURL', 'FIVE', 'GES', 'LCII', 'OLLI', 'PRPL', 'RVLV', 'SCVL', 'UPBD',
    'W', 'WRBY', 'ANF', 'BBWI', 'BURL', 'DKS', 'FL', 'LAD', 'SIG', 'TSCO',
    
    # Consumer - Restaurants & Hospitality
    'BLMN', 'CAKE', 'CBRL', 'CHUY', 'DENN', 'DIN', 'PLAY', 'RRGB', 'RUTH', 'TXRH',
    'WEN', 'WING', 'BJRI', 'BROS', 'CAVA', 'CMG', 'DNUT', 'JACK', 'LOCO', 'SHAK',
    
    # Financials - Regional Banks
    'ABCB', 'BANR', 'CADE', 'CASH', 'CBSH', 'CVBF', 'EWBC', 'FBK', 'FFIN', 'FHN',
    'GBCI', 'HBAN', 'HOMB', 'IBOC', 'ONB', 'OZK', 'PPBI', 'SFNC', 'SNV', 'UBSI',
    
    # Financials - Fintech & Services
    'AFRM', 'COIN', 'FOUR', 'LC', 'LU', 'MKTX', 'SOFI', 'UPST', 'VIRT', 'NU',
    
    # Financials - Insurance & Asset Management
    'ACGL', 'AFG', 'AXS', 'BRO', 'ESGR', 'KNSL', 'PRI', 'RLI', 'RYAN', 'WRB',
    
    # Energy - Oil & Gas Services
    'AROC', 'CLB', 'FLNG', 'FTI', 'HP', 'LBRT', 'NBR', 'NE', 'PTEN', 'RIG',
    
    # Energy - Renewables & Alternative
    'ARRY', 'ENPH', 'FSLR', 'NOVA', 'RUN', 'SEDG', 'SHLS', 'PLUG', 'BE', 'CHPT',
    
    # Materials - Chemicals & Specialty Materials
    'ALB', 'ASIX', 'CE', 'FUL', 'HUN', 'MEOH', 'NEU', 'OLN', 'RPM', 'SXT',
    'TROX', 'TSE', 'WLK', 'AVNT', 'CGNT', 'HWKN', 'KRA', 'BCPC', 'ECL', 'ESI',
    
    # Real Estate - REITs (Specialized)
    'AMT', 'CCI', 'DLR', 'EQIX', 'PLD', 'PSA', 'SBAC', 'SPG', 'WELL', 'VTR'
]

# =============================================================================
# INDIAN STOCKS CONFIGURATION
# =============================================================================

# Filters for Hidden Gems (India) - Using INR
# Adjusted for Indian market realities - emerging companies with growth potential
INDIA_MARKET_CAP_MIN = 1_000_000_000   # ₹1,000 Cr (~$120M) - Real hidden gems
INDIA_MARKET_CAP_MAX = 100_000_000_000 # ₹1,00,000 Cr (~$12B) - Upper mid-cap
INDIA_MIN_AVG_VOLUME = 50_000  # 50K shares - Less liquid but still tradeable

# Indian Stock Universe - NSE Mid/Small Caps
# Add .NS suffix for NSE stocks or .BO for BSE
INDIA_STOCK_UNIVERSE = [
    # IT Services & Software
    'PERSISTENT.NS', 'COFORGE.NS', 'MPHASIS.NS', 'LTTS.NS', 'CYIENT.NS',
    'TATAELXSI.NS', 'SONATSOFTW.NS', 'HAPPSTMNDS.NS', 'INTELLECT.NS', 'ROUTE.NS',
    
    # Pharmaceuticals & Healthcare
    'ALKEM.NS', 'TORNTPHARM.NS', 'LALPATHLAB.NS', 'METROPOLIS.NS', 'THYROCARE.NS',
    'AUROPHARMA.NS', 'ABBOTINDIA.NS', 'GLAXO.NS', 'SANOFI.NS', 'PFIZER.NS',
    'IPCALAB.NS', 'LAURUSLABS.NS', 'GLAND.NS', 'NATCOPHARMA.NS', 'STAR.NS',
    
    # Auto Components
    'MOTHERSON.NS', 'BOSCHLTD.NS', 'EXIDEIND.NS', 'BALKRISIND.NS', 'MRF.NS',
    'APOLLOTYRE.NS', 'CEATLTD.NS', 'ENDURANCE.NS', 'SCHAEFFLER.NS', 'SKFINDIA.NS',
    
    # Chemicals & Materials
    'AARTI.NS', 'DEEPAKNTR.NS', 'SRF.NS', 'NAVINFLUOR.NS', 'ATUL.NS',
    'PIIND.NS', 'GNFC.NS', 'FLUOROCHEM.NS', 'TATACHEM.NS', 'BASF.NS',
    
    # Consumer & Retail
    'TRENT.NS', 'JUBLFOOD.NS', 'RELAXO.NS', 'PAGEIND.NS', 'BATAIND.NS',
    'VMART.NS', 'WESTLIFE.NS', 'SAPPHIRE.NS', 'RAYMOND.NS', 'TITAN.NS',
    
    # Engineering & Capital Goods
    'CUMMINSIND.NS', 'THERMAX.NS', 'ABB.NS', 'SIEMENS.NS', 'VOLTAS.NS',
    'HAVELLS.NS', 'CROMPTON.NS', 'POLYCAB.NS', 'KEI.NS', 'KALPATPOWR.NS',
    
    # Financial Services
    'CHOLAFIN.NS', 'SRTRANSFIN.NS', 'MUTHOOTFIN.NS', 'MANAPPURAM.NS', 'ICICIGI.NS',
    'SBICARD.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'HDFCLIFE.NS', 'SBILIFE.NS',
    
    # Cement & Construction
    'RAMCOCEM.NS', 'JKCEMENT.NS', 'HEIDELBERG.NS', 'STARCEMENT.NS', 'NUVOCO.NS',
    'NCC.NS', 'IRCON.NS', 'NBCC.NS', 'ASHOKLEY.NS', 'GRINDWELL.NS',
    
    # Metals & Mining
    'APL.NS', 'JINDALSTEL.NS', 'SAIL.NS', 'NMDC.NS', 'HINDZINC.NS',
    'VEDL.NS', 'NATIONALUM.NS', 'HINDALCO.NS', 'RATNAMANI.NS', 'WELCORP.NS',
    
    # Textiles & Apparel
    'AFFLE.NS', 'GOKEX.NS', 'VARDHACRLC.NS', 'SPANDANA.NS', 'KPRMILL.NS',
    'TRIDENT.NS', 'WELSPUNIND.NS', 'GRASIM.NS', 'RTNPOWER.NS', 'CENTURYPLY.NS',
]

# =============================================================================
# COMMON SETTINGS (US & INDIA)
# =============================================================================

# Valuation Score Thresholds (Total 100 points)
VALUATION_WEIGHTS = {
    'eps_growth_yoy': 25,
    'eps_growth_3y': 15,
    'roe': 20,
    'debt_equity': 15,
    'pe_vs_sector': 10,
    'peg_ratio': 10,
    'fcf_yield': 5
}

# Valuation Thresholds (US / Global)
EPS_GROWTH_EXCELLENT = 15  # %
EPS_GROWTH_GOOD = 10  # %
EPS_GROWTH_3Y_EXCELLENT = 12  # %
EPS_GROWTH_3Y_GOOD = 8  # %
ROE_EXCELLENT = 20  # %
ROE_GOOD = 15  # %
DEBT_EQUITY_EXCELLENT = 0.5
DEBT_EQUITY_GOOD = 1.0
PE_SECTOR_EXCELLENT = 0.8  # 80% of sector avg
PE_SECTOR_GOOD = 1.0  # 100% of sector avg
PEG_EXCELLENT = 1.0
PEG_GOOD = 1.5
FCF_YIELD_EXCELLENT = 5  # %
FCF_YIELD_GOOD = 2  # %

# =============================================================================
# INDIA-SPECIFIC THRESHOLDS (More Realistic for Emerging Market)
# =============================================================================
# These are used automatically when MARKET == "INDIA" or "BOTH"
# Rationale: Indian companies are in growth phase, use more leverage,
# and operate in higher interest rate environment

INDIA_EPS_GROWTH_EXCELLENT = 12  # % (vs 15% for US) - Growth phase companies
INDIA_EPS_GROWTH_GOOD = 8        # % (vs 10% for US)
INDIA_EPS_GROWTH_3Y_EXCELLENT = 10  # % (vs 12% for US)
INDIA_EPS_GROWTH_3Y_GOOD = 6     # % (vs 8% for US)
INDIA_ROE_EXCELLENT = 18         # % (vs 20% for US) - Capital is more expensive
INDIA_ROE_GOOD = 12              # % (vs 15% for US) - 12-15% is decent in India
INDIA_DEBT_EQUITY_EXCELLENT = 0.7  # (vs 0.5 for US) - Bank financing culture
INDIA_DEBT_EQUITY_GOOD = 1.5     # (vs 1.0 for US) - More leverage is normal
INDIA_PE_SECTOR_EXCELLENT = 0.8  # Same as US
INDIA_PE_SECTOR_GOOD = 1.0       # Same as US
INDIA_PEG_EXCELLENT = 1.2        # (vs 1.0 for US) - Higher growth premium
INDIA_PEG_GOOD = 1.8             # (vs 1.5 for US)
INDIA_FCF_YIELD_EXCELLENT = 4    # % (vs 5% for US)
INDIA_FCF_YIELD_GOOD = 1.5       # % (vs 2% for US)

# =============================================================================
# BONUS SCORING SYSTEM (Simple Additive - Optional Quality Signals)
# =============================================================================
# Philosophy: Stocks don't need all bonuses to be good
# Each bonus is 0 or +5 points when signal is strong
# Missing data = no penalty, just no bonus

# Bonus 1: Insider Buying
INSIDER_BUY_BONUS = 5           # Points if significant buying detected
INSIDER_BUY_THRESHOLD = 3       # Min transactions in last 3 months

# Bonus 2: Institutional Interest  
INSTITUTIONAL_BONUS = 5         # Points if smart money interested
INSTITUTIONAL_THRESHOLD = 40    # Min % ownership to qualify

# Bonus 3: Low Short Interest
SHORT_INTEREST_BONUS = 5        # Points if low shorts (market confidence)
SHORT_INTEREST_THRESHOLD = 5    # Max % to qualify

# Maximum possible bonus points
MAX_BONUS_POINTS = 15           # 3 bonuses × 5 points each

# Technical Score Parameters
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
ADX_PERIOD = 14

# =============================================================================
# SCORING & ACTION THRESHOLDS (Conservative)
# =============================================================================

# Composite Scoring Weights (60% Fundamental, 40% Technical)
VALUATION_WEIGHT = 0.6  # Fundamentals are primary driver
TECHNICAL_WEIGHT = 0.4  # Timing is secondary confirmation

# Action Thresholds (Conservative - High Conviction Only)
ACTION_THRESHOLDS = {
    'STRONG_BUY': {
        'valuation_min': 80,    # Exceptional fundamentals
        'technical_min': 70,    # Excellent timing
        'description': 'Ultra high conviction - Best opportunities',
        'needs_deep_analysis': True  # Flag for Phase 2 AI analysis
    },
    'BUY': {
        'valuation_min': 70,    # Strong fundamentals  
        'technical_min': 60,    # Good timing
        'description': 'High conviction - Quality stocks with good entry',
        'needs_deep_analysis': True  # Flag for Phase 2 AI analysis
    },
    'WATCH': {
        'valuation_min': 70,    # Strong fundamentals
        'technical_min': 40,    # Timing not yet optimal
        'technical_max': 60,
        'description': 'Good fundamentals, waiting for better technical setup',
        'needs_deep_analysis': False
    },
    'WAIT': {
        'valuation_min': 70,    # Strong fundamentals
        'technical_max': 40,    # Poor timing currently
        'description': 'Great company, wrong time - wait for technical improvement',
        'needs_deep_analysis': False
    },
    'SPECULATIVE': {
        'valuation_min': 50,    # Decent fundamentals
        'valuation_max': 70,
        'technical_min': 60,    # Strong momentum
        'description': 'Momentum play - higher risk',
        'needs_deep_analysis': False
    },
    'AVOID': {
        'description': 'Does not meet criteria',
        'needs_deep_analysis': False
    }
}

# Market Regime Adjustments (Conservative)
MARKET_REGIME = {
    'bearish_adjustment': 10,  # Require +10 points in bear market (e.g., 80 instead of 70)
    'block_buys_in_bear': False,  # Still allow buying, but be more selective
}

# Market Filter
SPY_MA_PERIOD = 200

# Output
TOP_N_STOCKS = 20
OUTPUT_FILE = "../output/stock_picks.csv"  # Save to output folder

# =============================================================================
# AUTO-SELECT MARKET SETTINGS BASED ON MARKET VARIABLE
# =============================================================================
if MARKET == "US":
    STOCK_UNIVERSE = US_STOCK_UNIVERSE
    MARKET_CAP_MIN = US_MARKET_CAP_MIN
    MARKET_CAP_MAX = US_MARKET_CAP_MAX
    MIN_AVG_VOLUME = US_MIN_AVG_VOLUME
    MARKET_INDEX = "SPY"  # S&P 500
    
elif MARKET == "INDIA":
    STOCK_UNIVERSE = INDIA_STOCK_UNIVERSE
    MARKET_CAP_MIN = INDIA_MARKET_CAP_MIN
    MARKET_CAP_MAX = INDIA_MARKET_CAP_MAX
    MIN_AVG_VOLUME = INDIA_MIN_AVG_VOLUME
    MARKET_INDEX = "^NSEI"  # Nifty 50
    OUTPUT_FILE = "../output/stock_picks_india.csv"
    
elif MARKET == "BOTH":
    STOCK_UNIVERSE = US_STOCK_UNIVERSE + INDIA_STOCK_UNIVERSE
    MARKET_CAP_MIN = min(US_MARKET_CAP_MIN, INDIA_MARKET_CAP_MIN)
    MARKET_CAP_MAX = max(US_MARKET_CAP_MAX, INDIA_MARKET_CAP_MAX)
    MIN_AVG_VOLUME = min(US_MIN_AVG_VOLUME, INDIA_MIN_AVG_VOLUME)
    MARKET_INDEX = "SPY"  # Use US market as primary indicator
    OUTPUT_FILE = "../output/stock_picks_combined.csv"

# Note: This list focuses on small/mid-caps across diverse sectors
# Market caps range from ~$300M to $10B as of late 2024
# Review and update quarterly as market caps change