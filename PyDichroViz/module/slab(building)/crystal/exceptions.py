"""
Custom exceptions for crystal data module
"""

class CrystalDataError(Exception):
    """Base exception for crystal data related errors"""
    pass

class InvalidCrystalType(CrystalDataError):
    """Raised when invalid crystal type or plane is requested"""
    pass

class DataValidationError(CrystalDataError):
    """Raised when crystal data fails validation"""
    pass

class DataNotFoundError(CrystalDataError):
    """Raised when requested crystal data is not found"""
    pass