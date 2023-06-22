# Import all the models, so that Base has them before being
# imported by Alembic
from src.db.base_class import Base  # noqa
from .models.surveys import SurveyModel  # noqa
from .models.charts import ChartModel  # noqa
from .models.waypoints import WaypointModel  # noqa
