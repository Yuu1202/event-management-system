from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.application.commands.refund_commands import (
    ApproveRefundCommand, MarkRefundPaidOutCommand,
    RejectRefundCommand, RequestRefundCommand
)
from app.presentation.dependencies.dependencies import (
    get_approve_refund_handler, get_mark_refund_paidout_handler,
    get_reject_refund_handler, get_request_refund_handler
)

router = APIRouter(prefix="/refunds", tags=["Refunds"])


class RequestRefundRequest(BaseModel):
    booking_id: str
    customer_id: str


class RejectRefundRequest(BaseModel):
    organizer_id: str
    reason: str


class MarkPaidOutRequest(BaseModel):
    payment_reference: str


@router.post("", status_code=201)
def request_refund(
    body: RequestRefundRequest,
    handler=Depends(get_request_refund_handler)
):
    try:
        refund_id = handler.handle(RequestRefundCommand(
            booking_id=body.booking_id,
            customer_id=body.customer_id,
        ))
        return {"refund_id": refund_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{refund_id}/approve", status_code=200)
def approve_refund(
    refund_id: str,
    organizer_id: str,
    handler=Depends(get_approve_refund_handler)
):
    try:
        handler.handle(ApproveRefundCommand(refund_id=refund_id, organizer_id=organizer_id))
        return {"message": "Refund approved successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{refund_id}/reject", status_code=200)
def reject_refund(
    refund_id: str,
    body: RejectRefundRequest,
    handler=Depends(get_reject_refund_handler)
):
    try:
        handler.handle(RejectRefundCommand(
            refund_id=refund_id,
            organizer_id=body.organizer_id,
            reason=body.reason,
        ))
        return {"message": "Refund rejected successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{refund_id}/payout", status_code=200)
def mark_refund_paidout(
    refund_id: str,
    body: MarkPaidOutRequest,
    handler=Depends(get_mark_refund_paidout_handler)
):
    try:
        handler.handle(MarkRefundPaidOutCommand(
            refund_id=refund_id,
            payment_reference=body.payment_reference,
        ))
        return {"message": "Refund marked as paid out successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))