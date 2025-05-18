"""
Timeout settings for ScubaDiveIn project.
These settings control various timeout values for different operations.
"""

# Tool call timeouts (in seconds)
TOOL_CALL_TIMEOUT = 60  # Increased default timeout for tool calls
LIST_DIR_TIMEOUT = 45   # Increased timeout for directory listing
SEARCH_TIMEOUT = 45     # Increased timeout for search operations
FILE_READ_TIMEOUT = 45  # Increased timeout for file reading operations

# Database timeouts
DB_CONNECT_TIMEOUT = 45
DB_READ_TIMEOUT = 30
DB_WRITE_TIMEOUT = 35

# API timeouts
API_REQUEST_TIMEOUT = 45
RAZORPAY_API_TIMEOUT = 45

# Cache timeouts
CACHE_TIMEOUT = 300  # 5 minutes
SESSION_COOKIE_AGE = 7200  # 2 hours 