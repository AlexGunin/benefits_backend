from app.repositories.base.sql_alchemy import SQLAlchemyRepository

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.benefit import BenefitModel
from app.schemas.benefit import BenefitCreate, BenefitUpdate


class BenefitRepository(SQLAlchemyRepository[BenefitModel, BenefitCreate, BenefitUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, BenefitModel)