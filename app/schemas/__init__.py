from .dimensions import (
    # SR Dimension Type of Approval Status
    SrDimTypeOfApprovalStat,
    SrDimTypeOfApprovalStatCreate,
    SrDimTypeOfApprovalStatComplete,
    # Custom Dropdown Dimension
    DimCustomDropdown,
    DimCustomDropdownCreate,
    DimCustomDropdownComplete,
    # Color Coding Dimension
    DimColorCoding,
    DimColorCodingCreate,
    # Customer Dimension
    DimCustomer,
    DimCustomerCreate,
    DimCustomerComplete,
    # Discount Dimension
    DimDiscount,
    DimDiscountCreate,
    # Material Dimension
    DimMara,
    DimMaraCreate,
    DimMaraComplete,
)

from .fct_visits import (
    FctVisits,
    FctVisitsCreate,
    FctVisitsComplete,
    FctVisitsResponse,
    FctVisitsListResponse,
)

from .sr_fct_header import (
    SrFctHeader,
    SrFctHeaderCreate,
    SrFctHeaderComplete,
    SrFctHeaderResponse,
    SrFctHeaderDetailResponse,
    SrFctHeaderListResponse,
)

from .sr_fct_items import (
    SrFctItems,
    SrFctItemsCreate,
    SrFctItemsComplete,
    SrFctItemsResponse,
    SrFctItemsDetailResponse,
    SrFctItemsListResponse,
)

from .sr_fct_attachment import (
    SrFctAttachment,
    SrFctAttachmentCreate,
    SrFctAttachmentComplete,
    SrFctAttachmentResponse,
    SrFctAttachmentDetailResponse,
    SrFctAttachmentListResponse,
)

from .sr_fct_logsremarksheader import (
    SrFctLogsRemarksHeader,
    SrFctLogsRemarksHeaderCreate,
    SrFctLogsRemarksHeaderComplete,
    SrFctLogsRemarksHeaderResponse,
    SrFctLogsRemarksHeaderDetailResponse,
    SrFctLogsRemarksHeaderListResponse,
)

from .sr_fct_logsremarksitems import (
    SrFctLogsRemarksItems,
    SrFctLogsRemarksItemsCreate,
    SrFctLogsRemarksItemsComplete,
    SrFctLogsRemarksItemsResponse,
    SrFctLogsRemarksItemsDetailResponse,
    SrFctLogsRemarksItemsListResponse,
)

from .common import (
    BaseSchema,
    PaginationParams,
    PaginatedResponse,
    DateRangeFilter,
    SrHeaderFilter,
    VisitsFilter,
    ResponseStatus,
    ErrorResponse,
    SuccessResponse,
    BulkCreateResult,
    BulkUpdateResult,
    BulkDeleteResult,
    EmailValidationMixin,
    DECIMALValidationMixin,
    AuditSchemaMixin,
    MobileAuditSchemaMixin,
)

__version__ = "1.0.0"
__author__ = "Your Team"

__all__ = [
    # Dimension schemas
    "SrDimTypeOfApprovalStat",
    "SrDimTypeOfApprovalStatCreate",
    "SrDimTypeOfApprovalStatComplete",
    "DimCustomDropdown",
    "DimCustomDropdownCreate",
    "DimCustomDropdownComplete",
    "DimColorCoding",
    "DimColorCodingCreate",
    "DimCustomer",
    "DimCustomerCreate",
    "DimCustomerComplete",
    "DimDiscount",
    "DimDiscountCreate",
    "DimMara",
    "DimMaraCreate",
    "DimMaraComplete",
    # Fct table schemas
    "FctVisits",
    "FctVisitsCreate",
    "FctVisitsComplete",
    "FctVisitsResponse",
    "FctVisitsListResponse",
    "SrFctHeader",
    "SrFctHeaderCreate",
    "SrFctHeaderComplete",
    "SrFctHeaderResponse",
    "SrFctHeaderDetailResponse",
    "SrFctHeaderListResponse",
    "SrFctItems",
    "SrFctItemsCreate",
    "SrFctItemsComplete",
    "SrFctItemsResponse",
    "SrFctItemsDetailResponse",
    "SrFctItemsListResponse",
    "SrFctAttachment",
    "SrFctAttachmentCreate",
    "SrFctAttachmentComplete",
    "SrFctAttachmentResponse",
    "SrFctAttachmentDetailResponse",
    "SrFctAttachmentListResponse",
    "SrFctLogsRemarksHeader",
    "SrFctLogsRemarksHeaderCreate",
    "SrFctLogsRemarksHeaderComplete",
    "SrFctLogsRemarksHeaderResponse",
    "SrFctLogsRemarksHeaderDetailResponse",
    "SrFctLogsRemarksHeaderListResponse",
    "SrFctLogsRemarksItems",
    "SrFctLogsRemarksItemsCreate",
    "SrFctLogsRemarksItemsComplete",
    "SrFctLogsRemarksItemsResponse",
    "SrFctLogsRemarksItemsDetailResponse",
    "SrFctLogsRemarksItemsListResponse",
    # Common utilities
    "BaseSchema",
    "PaginationParams",
    "PaginatedResponse",
    "DateRangeFilter",
    "SrHeaderFilter",
    "VisitsFilter",
    "ResponseStatus",
    "ErrorResponse",
    "SuccessResponse",
    "BulkCreateResult",
    "BulkUpdateResult",
    "BulkDeleteResult",
    "EmailValidationMixin",
    "DECIMALValidationMixin",
    "AuditSchemaMixin",
    "MobileAuditSchemaMixin",
]


DIMENSION_SCHEMAS = [
    "SrDimTypeOfApprovalStat",
    "DimCustomDropdown",
    "DimColorCoding",
    "DimCustomer",
    "DimDiscount",
    "DimMara",
]

FACT_SCHEMAS = [
    "FctVisits",
    "SrFctHeader",
    "SrFctItems",
    "SrFctAttachment",
    "SrFctLogsRemarksHeader",
    "SrFctLogsRemarksItems",
]

SR_SCHEMAS = [
    "SrFctHeader",
    "SrFctItems",
    "SrFctAttachment",
    "SrFctLogsRemarksHeader",
    "SrFctLogsRemarksItems",
    "SrDimTypeOfApprovalStat",
]
