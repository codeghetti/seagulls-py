from seagulls.rpg_demo import RpgDemoCliPluginEntryPoint


class TestRpgDemoCliPluginEntryPoint:
    def test_nothing(self) -> None:
        assert RpgDemoCliPluginEntryPoint is not None
