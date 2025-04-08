from ... import options
from ...test import SVTestBase


class TestArcadeMachinesLogic(SVTestBase):
    options = {
        options.ArcadeMachineLocations.internal_name: options.ArcadeMachineLocations.option_full_shuffling,
    }

    def test_prairie_king(self):
        self.assertFalse(self.world.logic.region.can_reach("JotPK World 1")(self.multiworld.state))
        self.assertFalse(self.world.logic.region.can_reach("JotPK World 2")(self.multiworld.state))
        self.assertFalse(self.world.logic.region.can_reach("JotPK World 3")(self.multiworld.state))
        self.assert_cannot_reach_location("Journey of the Prairie King Victory")

        boots = self.create_item("JotPK: Progressive Boots")
        gun = self.create_item("JotPK: Progressive Gun")
        ammo = self.create_item("JotPK: Progressive Ammo")
        life = self.create_item("JotPK: Extra Life")
        drop = self.create_item("JotPK: Increased Drop Rate")

        self.multiworld.state.collect(boots)
        self.multiworld.state.collect(gun)
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 1")(self.multiworld.state))
        self.assertFalse(self.world.logic.region.can_reach("JotPK World 2")(self.multiworld.state))
        self.assertFalse(self.world.logic.region.can_reach("JotPK World 3")(self.multiworld.state))
        self.assert_cannot_reach_location("Journey of the Prairie King Victory")
        self.remove(boots)
        self.remove(gun)

        self.multiworld.state.collect(boots)
        self.multiworld.state.collect(boots)
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 1")(self.multiworld.state))
        self.assertFalse(self.world.logic.region.can_reach("JotPK World 2")(self.multiworld.state))
        self.assertFalse(self.world.logic.region.can_reach("JotPK World 3")(self.multiworld.state))
        self.assert_cannot_reach_location("Journey of the Prairie King Victory")
        self.remove(boots)
        self.remove(boots)

        self.multiworld.state.collect(boots)
        self.multiworld.state.collect(gun)
        self.multiworld.state.collect(ammo)
        self.multiworld.state.collect(life)
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 1")(self.multiworld.state))
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 2")(self.multiworld.state))
        self.assertFalse(self.world.logic.region.can_reach("JotPK World 3")(self.multiworld.state))
        self.assert_cannot_reach_location("Journey of the Prairie King Victory")
        self.remove(boots)
        self.remove(gun)
        self.remove(ammo)
        self.remove(life)

        self.multiworld.state.collect(boots)
        self.multiworld.state.collect(gun)
        self.multiworld.state.collect(gun)
        self.multiworld.state.collect(ammo)
        self.multiworld.state.collect(ammo)
        self.multiworld.state.collect(life)
        self.multiworld.state.collect(drop)
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 1")(self.multiworld.state))
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 2")(self.multiworld.state))
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 3")(self.multiworld.state))
        self.assert_cannot_reach_location("Journey of the Prairie King Victory")
        self.remove(boots)
        self.remove(gun)
        self.remove(gun)
        self.remove(ammo)
        self.remove(ammo)
        self.remove(life)
        self.remove(drop)

        self.multiworld.state.collect(boots)
        self.multiworld.state.collect(boots)
        self.multiworld.state.collect(gun)
        self.multiworld.state.collect(gun)
        self.multiworld.state.collect(gun)
        self.multiworld.state.collect(gun)
        self.multiworld.state.collect(ammo)
        self.multiworld.state.collect(ammo)
        self.multiworld.state.collect(ammo)
        self.multiworld.state.collect(life)
        self.multiworld.state.collect(drop)
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 1")(self.multiworld.state))
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 2")(self.multiworld.state))
        self.assertTrue(self.world.logic.region.can_reach("JotPK World 3")(self.multiworld.state))
        self.assert_can_reach_location("Journey of the Prairie King Victory")
        self.remove(boots)
        self.remove(boots)
        self.remove(gun)
        self.remove(gun)
        self.remove(gun)
        self.remove(gun)
        self.remove(ammo)
        self.remove(ammo)
        self.remove(ammo)
        self.remove(life)
        self.remove(drop)
