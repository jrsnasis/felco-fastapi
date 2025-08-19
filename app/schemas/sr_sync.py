# app/schemas/sr_sync.py
from pydantic import BaseModel
from typing import List

from app.schemas.sr_fct_header import SrFctHeaderResponse
from app.schemas.sr_fct_items import SrFctItemsResponse
from app.schemas.sr_fct_attachment import SrFctAttachmentResponse
from app.schemas.sr_fct_logsremarksheader import SrFctLogsRemarksHeaderResponse
from app.schemas.sr_fct_logsremarksitems import SrFctLogsRemarksItemsResponse


class SrSyncResponse(BaseModel):
    """Combined response schema for all SR data"""

    headers: List[SrFctHeaderResponse] = []
    items: List[SrFctItemsResponse] = []
    attachments: List[SrFctAttachmentResponse] = []
    header_logs: List[SrFctLogsRemarksHeaderResponse] = []
    items_logs: List[SrFctLogsRemarksItemsResponse] = []

    class Config:
        from_attributes = True
