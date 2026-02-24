class DigikalaAnalyzerBaseException(Exception):
    """Base exception for the Digikala Comment Analyzer project."""
    pass

class MissingConfigurationError(DigikalaAnalyzerBaseException):
    """Raised when environment variables are missing."""
    pass

class CrawlerError(DigikalaAnalyzerBaseException):
    """Raised when the crawler fails to fetch data from the target API."""
    pass

class LLMAnalysisError(DigikalaAnalyzerBaseException):
    """Raised when the AI model fails to process the comment or return valid JSON."""
    pass

class DatabaseError(DigikalaAnalyzerBaseException):
    """Raised when a SQLite database operation fails."""
    pass