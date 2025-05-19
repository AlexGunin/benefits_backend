from typing import List

from fastapi import APIRouter, Depends

from app.dependencies import deps, is_admin, get_current_user_id
from app.schemas.benefit import BenefitCreate, BenefitRead, BenefitUpdate

router = APIRouter(
    prefix="/benefits",
    tags=["Benefits"],

)

@router.post("", response_model=BenefitRead, dependencies=[Depends(is_admin)])
async def create_benefit(benefit: BenefitCreate, benefits_service: deps.services.benefits):
    return await benefits_service.add(benefit)

@router.get("", response_model=List[BenefitRead], dependencies=[Depends(get_current_user_id)])
async def get_benefits(benefits_service: deps.services.benefits):
    return await benefits_service.get_all()

@router.patch("/{benefit_id}", dependencies=[Depends(is_admin)])
async def patch_benefits(benefit_id: int, benefit_data: BenefitUpdate, benefits_service: deps.services.benefits):
    return await benefits_service.patch(benefit_id, BenefitUpdate.model_validate(benefit_data))

@router.delete("/{benefit_id}", status_code=204, dependencies=[Depends(is_admin)])
async def delete_benefits(benefit_id: int, benefits_service: deps.services.benefits):
    return await benefits_service.delete(benefit_id)
