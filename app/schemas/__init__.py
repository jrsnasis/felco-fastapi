# app/schemas/__init__.py
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
    SrFctHeaderCreate,
    SrFctHeaderResponse,
    SrFctHeaderListResponse,
    SrFctHeaderUpdate,
)

from .sr_fct_items import (
    SrFctItemsCreate,
    SrFctItemsResponse,
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

from .sr_sync import (
    SrSyncResponse,
)

__version__ = "1.0.0"
__author__ = "FELCO LOVE"

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
    "SrFctHeaderUpdate",
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
    "SrSyncResponse"
]


DIMENSION_SCHEMAS = [
    "SrDimTypeOfApprovalStat",
    "DimCustomDropdown",
    "DimColorCoding",
    "DimCustomer",
    "DimDiscount",
    "DimMara",
]

FCT_SCHEMAS = [
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

for _model in [
    SrFctAttachment,
    SrFctLogsRemarksHeader,
    SrFctLogsRemarksItems,
    DimCustomDropdown,
    DimCustomer,
]:
    try:
        _model.model_rebuild()
    except Exception as e:
        print(f"Skipping rebuild for {_model}: {e}")
