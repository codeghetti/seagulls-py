from seagulls.cat_demos.engine.v2.components._entities import GameSceneId
from seagulls.cat_demos.engine.v2.sessions._app import seagulls_app
# print(f"hello {sys.argv}")
# cat_container = CatDemosDiContainer()
# cat_container.app().run(cat_container.standalone_providers()())

app = seagulls_app()
app.load_scene(GameSceneId("home"))
