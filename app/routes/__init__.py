def register_routes(app):
    from app.routes.players import players_bp
    from app.routes.games import games_bp


    # Registrar o blueprint
    app.register_blueprint(players_bp)
    app.register_blueprint(games_bp)
