from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db.engine import get_session
from app.db.models.benefit import BenefitModel
from app.repositories.base.abstract import AbstractRepository
from app.repositories.benefits import BenefitRepository
from app.schemas.benefit import BenefitCreate, BenefitUpdate
from app.services.base import BaseService


class BenefitsService(BaseService[BenefitModel, BenefitCreate, BenefitUpdate]):
    def __init__(self, benefits_repository: AbstractRepository[BenefitModel, BenefitCreate, BenefitUpdate]):
        super().__init__(repository=benefits_repository)


def get_benefits_service(session: AsyncSession = Depends(get_session)):
    return BenefitsService(BenefitRepository(session))