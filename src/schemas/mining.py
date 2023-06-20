from typing import Dict, List, Optional, Self

import attrs

from src.db import get_db
from src.db.models.surveys import SurveyModel
from src.support.datetime import DateTime


@attrs.define
class Survey:
    """
    A survey result
    """

    signature: str
    symbol: str
    deposits: List[Dict]
    expiration: DateTime
    size: str

    def drop(self) -> None:
        """
        Remove from the database
        """
        with get_db() as db:
            survey_model: SurveyModel = (
                db.query(SurveyModel)
                .filter(SurveyModel.signature == self.signature)
                .one()
            )
            db.delete(survey_model)
            db.commit()

    def payload(self) -> Dict:
        """
        Like attrs.asdict but formats the datetime value properly
        """
        as_dict = attrs.asdict(self)
        as_dict["expiration"] = as_dict["expiration"]["raw"]
        return as_dict

    @classmethod
    def build(cls, data: Dict) -> Self:
        date_time = DateTime.build(datetime_string=data.pop("expiration"))

        return cls(**data, expiration=date_time)

    @classmethod
    def filter(cls, symbol: str, size: Optional[str] = None) -> List[Self]:
        """
        Return a list of Surveys that match the symbol and size
        """
        with get_db() as db:
            survey_models: List[SurveyModel] = db.query(SurveyModel).filter(
                SurveyModel.symbol == symbol
            )
            if size:
                survey_models.filter(SurveyModel.size == size)

        return [
            cls(
                signature=s.signature,
                symbol=s.symbol,
                deposits=s.deposits,
                expiration=DateTime.build(datetime_string=s.expiration),
                size=s.size,
            )
            for s in survey_models
        ]

    @classmethod
    def from_db(cls, signature: str) -> Self:
        """
        Get a persisted instance of this from the database.
        """
        with get_db() as db:
            survey_model: SurveyModel = (
                db.query(SurveyModel).filter(SurveyModel.signature == signature).one()
            )

        return cls(
            signature=survey_model.signature,
            symbol=survey_model.symbol,
            deposits=survey_model.deposits,
            expiration=DateTime.build(datetime_string=survey_model.expiration),
            size=survey_model.size,
        )

    def save(self):
        """
        Persist in the database
        """
        survey_model: SurveyModel = SurveyModel(
            signature=self.signature,
            symbol=self.symbol,
            deposits=self.deposits,
            expiration=self.expiration.raw,
            size=self.size,
        )

        with get_db() as db:
            db.add(survey_model)
            db.commit()


@attrs.define
class Extraction:
    """
    The result of a mining operation
    """

    shipSymbol: str
    yield_: Dict
