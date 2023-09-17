"""
Index.py - provides a simple html example
"""
from flask import Blueprint

from src.schemas.agent import Agent
from src.schemas.ships import ShipsManager
from src.schemas.waypoint import Waypoint, Shipyard
from src.web.app import app
from src.web.rf.renderer import render_html

routes = Blueprint("index", __name__, url_prefix="/")


@routes.route("/")
@render_html()
def base_page():
    agent = Agent.me_sync()
    ships = ShipsManager.all()
    return dict(agent=agent, ships=ships)


@routes.route("/agent")
@render_html()
def agent():
    agent = Agent.me_sync()
    return dict(agent=agent)


@routes.route("/ships")
@render_html()
def ships():
    ships = ShipsManager.all()
    return dict(ships=ships)


@routes.route('/waypoint/<waypoint_symbol>')
@render_html()
def waypoint(waypoint_symbol: str):
    waypoint = Waypoint.sync_get(symbol=waypoint_symbol)
    return dict(waypoint=waypoint)

@routes.route("/shipyard/<waypoint_symbol>")
@render_html()
def shipyard(waypoint_symbol: str):
    shipyard = Shipyard.sync_get(symbol=waypoint_symbol)
    return dict(shipyard=shipyard)

app.register_blueprint(routes)
