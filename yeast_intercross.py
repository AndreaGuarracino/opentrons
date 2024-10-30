"""
Code for Yeast-Intercross Protocol.

The protocol is defined at
"""
# Yeast-Intercross Protocol
# Copyright © 2024 Frederick Muriuki Muriithi <fredmanglis@protonmail.com>
#
# This is part of the yeast-intercross protocol defined at
# https://docs.google.com/document/d/1Wy9pgJrg8Q71WrU-aVVziWQFyscnlpQuDEA2xgcpQ2c/edit?usp=sharing
import random

from opentrons.protocol_api import Labware, ProtocolContext, HeaterShakerContext

## OpenTrons initialisation
metadata = {
    "protocolName": "Yeast Intercross Protocol",
    "description": """…""",
    "author": "Frederick M. Muriithi"
}

requirements = {"robotType": "OT-2", "apiLevel": "2.16"}

MOD_HS_LOCATION = 1
MOD_HS_SPACING_01 = 2
MOD_HS_SPACING_02 = 4
MOD_TEMP_LOCATION = 10
TIP_RACK01_LOCATION = 9
TIP_RACK02_LOCATION = 11
RES_LIQUIDS_LOCATION = 7
RES_CROSSING_LOCATION = 3
CHANGE_THIS=5 # Remove this, it was only useful for testing!

def incubate(
        protocol: ProtocolContext,
        heatershaker: HeaterShakerContext,
        reservoir: Labware,
        shaker_speed: int = 1200,
        celsius: float = 37.0,
        minutes: int = 6 * 60
):
    """Incubate things while heating and shaking them."""
    heatershaker.open_labware_latch()
    protocol.move_labware(labware=reservoir, new_location=heatershaker)
    heatershaker.close_labware_latch()
    heatershaker.set_target_temperature(celsius=celsius)
    heatershaker.set_and_wait_for_shake_speed(rpm=shaker_speed)
    protocol.delay(minutes=minutes)
    heatershaker.deactivate_heater()
    heatershaker.deactivate_shaker()

    heatershaker.open_labware_latch()


def randomise_volumes(well_count: int, mini: int, maxi: int) -> list[int]:
    """Return `well_count` random volumes between mini and maxi (inclusive)."""
    return [random.randint(mini, maxi) for _i in range(0, well_count)]

def run(protocol: ProtocolContext):
    """Run the protocol."""

    # Label liquids
    MATa_suspension = protocol.define_liquid(
        name="MATa",
        description="10ml YPD solution infused with MATa yeast",
        display_color="#F210F5")
    MATalpha_suspension = protocol.define_liquid(
        name="MATalpha",
        description="10ml YPD solution infused with MATalpha yeast",
        display_color="#103DF5")
    clear_ypd = protocol.define_liquid(
        name="YPD",
        description="10ml of YPD solution with no yeast.",
        display_color="#DCCB82")

    # Define labware
    crossing_reservoir = protocol.load_labware(
        load_name="nest_96_wellplate_200ul_flat",
        label="crossing-reservoir",
        location=RES_CROSSING_LOCATION)
    mates_reservoir = protocol.load_labware(load_name="nest_12_reservoir_15ml",
                                            label="mates-reservoir",
                                            location=RES_LIQUIDS_LOCATION)

    # Define tips and instruments
    tips_200ul = protocol.load_labware(
        load_name="opentrons_96_filtertiprack_200ul",
        label="200ul tips with filters: count=96",
        location=TIP_RACK01_LOCATION)
    # tips_1000ul = protocol.load_labware(
    #     load_name="opentrons_96_filtertiprack_1000ul",
    #     label="1000ul tips with filters: count=96",
    #     location=TIP_RACK02_LOCATION)
    right_pipette = protocol.load_instrument(
        instrument_name="p300_single_gen2",
        mount="right",
        tip_racks=[
            # tips_1000ul,
            tips_200ul])

    # Define modules
    heatershaker = protocol.load_module(module_name="heaterShakerModuleV1",
                                        location=MOD_HS_LOCATION)
    

    # Mates Amplification
    #==========================================
    protocol.comment("Amplifying the mates =========================")
    MATa_well, MATalpha_well, YPD_well = (mates_reservoir.wells()[0],
                                          mates_reservoir.wells()[1],
                                          mates_reservoir.wells()[2])
    MATa_well.load_liquid(liquid=MATa_suspension, volume=10000)
    MATalpha_well.load_liquid(liquid=MATalpha_suspension, volume=10000)
    YPD_well.load_liquid(liquid=clear_ypd, volume=10000)
    ## ----
    incubate(protocol, heatershaker, mates_reservoir, shaker_speed=200,
             celsius=37, minutes=CHANGE_THIS)
    protocol.move_labware(
        labware=mates_reservoir, new_location=RES_LIQUIDS_LOCATION)

    # Crossing Mates
    #==========================================
    protocol.comment("Crossing the mates =========================")
    right_pipette.transfer(volume=50,
                           source=YPD_well,
                           dest=crossing_reservoir.wells())
    right_pipette.transfer(volume=25,#randomise_volumes(96, 5, 20),
                           source=MATa_well,
                           dest=crossing_reservoir.wells())
    right_pipette.transfer(volume=25,#randomise_volumes(96, 5, 20),
                           source=MATalpha_well,
                           dest=crossing_reservoir.wells())
    # ----
    incubate(protocol, heatershaker, crossing_reservoir, shaker_speed=1200,
             celsius=37, minutes=CHANGE_THIS)
    protocol.move_labware(
        labware=crossing_reservoir, new_location=RES_CROSSING_LOCATION)
    # ---- post incubation

    # Pre-sporulation
    #==========================================
    protocol.comment(
        "Running the pre-sporulation stage =========================")

    # Sporulation
    #==========================================
    protocol.comment(
        "Running the sporulation stage =========================")

    # Spore Enrichment
    #==========================================
    protocol.comment(
        "Enriching the spores =========================")

    # Spores Amplification
    #==========================================
    protocol.comment(
        "Amplifying the spores =========================")
    
