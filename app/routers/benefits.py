from typing import List

from fastapi import APIRouter

from app.dependencies import deps
from app.schemas.benefit import BenefitCreate, BenefitRead, BenefitUpdate

router = APIRouter(
    prefix="/benefits",
    tags=["Benefits"]
)

@router.post("", response_model=BenefitRead)
async def create_benefit(benefit: BenefitCreate, benefits_service: deps.services.benefits):
    return await benefits_service.add(benefit)

@router.get("", response_model=List[BenefitRead])
async def get_benefits(benefits_service: deps.services.benefits):
    return await benefits_service.get_all()

@router.patch("/{benefit_id}")
async def patch_benefits(benefit_id: int, benefit_data: BenefitUpdate, benefits_service: deps.services.benefits):
    return await benefits_service.patch(benefit_id, BenefitUpdate.model_validate(benefit_data))

@router.delete("/{benefit_id}", status_code=204)
async def delete_benefits(benefit_id: int, benefits_service: deps.services.benefits):
    return await benefits_service.delete(benefit_id)
