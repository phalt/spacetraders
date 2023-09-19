"""
Index.py - provides a simple html example
"""
from flask import Blueprint

from src.schemas.agent import Agent
from src.schemas.ships import ShipsManager, Ship
from src.schemas.waypoint import Waypoint, Shipyard
from src.schemas.markets import Market
from src.schemas.systems import System, JumpGate
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


@routes.route("/ship/<symbol>")
@render_html()
def ship(symbol: str):
    ship = Ship.sync_get(symbol=symbol)
    return dict(ship=ship)


@routes.route('/waypoint/<waypoint_symbol>')
@render_html()
def waypoint(waypoint_symbol: str):
    waypoint = Waypoint.sync_get(symbol=waypoint_symbol)
    if waypoint.type == "JUMP_GATE":
        jumpgate = JumpGate.sync_get(symbol=waypoint_symbol)
    else:
        jumpgate = None
    return dict(waypoint=waypoint, jumpgate=jumpgate)

@routes.route('/system/<system_symbol>')
@render_html()
def system(system_symbol: str):
    system = System.sync_get(symbol=system_symbol)
    return dict(system=system)

@routes.route("/shipyard/<waypoint_symbol>")
@render_html()
def shipyard(waypoint_symbol: str):
    shipyard = Shipyard.sync_get(symbol=waypoint_symbol)
    return dict(shipyard=shipyard)

@routes.route("/marketplace/<waypoint_symbol>")
@render_html()
def marketplace(waypoint_symbol: str):
    marketplace = Market.sync_get(symbol=waypoint_symbol)
    return dict(marketplace=marketplace)

app.register_blueprint(routes)
