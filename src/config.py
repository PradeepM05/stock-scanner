# Configuration File
# Now using 100% Yahoo Finance - no API key needed!

# Filters for Hidden Gems
MARKET_CAP_MIN = 300_000_000  # $300M
MARKET_CAP_MAX = 10_000_000_000  # $10B
MIN_AVG_VOLUME = 500_000
MAX_ANALYST_COVERAGE = 10  # Not easily available in free APIs, placeholder
MIN_INSTITUTIONAL_OWNERSHIP = 20  # Percentage
MAX_INSTITUTIONAL_OWNERSHIP = 60  # Percentage

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

# Valuation Thresholds
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

# Technical Score Parameters
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
ADX_PERIOD = 14

# Composite Scoring
VALUATION_WEIGHT = 0.6
TECHNICAL_WEIGHT = 0.4

# Market Filter
SPY_MA_PERIOD = 200

# Output
TOP_N_STOCKS = 20
OUTPUT_FILE = "stock_picks.csv"

# Stock Universe - Curated Small/Mid-Cap Stocks ($300M - $10B Market Cap)
# Diversified across sectors for hidden gems hunting
STOCK_UNIVERSE = [
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

# Note: This list focuses on small/mid-caps across diverse sectors
# Market caps range from ~$300M to $10B as of late 2024
# Review and update quarterly as market caps change