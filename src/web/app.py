from os.path import abspath, dirname, join

from src.web.rf.app import RFApp

app = RFApp(
    __name__,
    static_folder=abspath(join(dirname(__file__), "static")),
    template_folder=abspath(join(dirname(__file__), "template")),
)

from src.web import views  # noqa
