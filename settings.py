from envbind import ParameterSource, StringEnv


class MongoSettings(ParameterSource):
    uri: str = StringEnv(envar="MONGODB_URI")
    database: str = StringEnv(
        envar="MONGODB_DB",
        optional=True,
        default="meal_planner",
    )
