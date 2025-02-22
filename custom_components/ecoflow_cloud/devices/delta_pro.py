from . import const, BaseDevice
from ..entities import BaseSensorEntity, BaseNumberEntity, BaseSwitchEntity, BaseSelectEntity
from ..mqtt.ecoflow_mqtt import EcoflowMQTTClient
from ..number import ChargingPowerEntity, MaxBatteryLevelEntity, MinBatteryLevelEntity, MinGenStartLevelEntity, \
    MaxGenStopLevelEntity
from ..select import DictSelectEntity, TimeoutDictSelectEntity
from ..sensor import LevelSensorEntity, WattsSensorEntity, RemainSensorEntity, TempSensorEntity, \
    CyclesSensorEntity, InWattsSensorEntity, OutWattsSensorEntity, VoltSensorEntity
from ..switch import BeeperEntity, EnabledEntity


class DeltaPro(BaseDevice):
    def sensors(self, client: EcoflowMQTTClient) -> list[BaseSensorEntity]:
        return [
            LevelSensorEntity(client, "pd.soc", const.MAIN_BATTERY_LEVEL),
            WattsSensorEntity(client, "pd.wattsInSum", const.TOTAL_IN_POWER),
            WattsSensorEntity(client, "pd.wattsOutSum", const.TOTAL_OUT_POWER),

            InWattsSensorEntity(client, "inv.inputWatts", const.AC_IN_POWER),
            InWattsSensorEntity(client, "mppt.inWatts", const.SOLAR_IN_POWER),

            OutWattsSensorEntity(client, "inv.outputWatts", const.AC_OUT_POWER),
            OutWattsSensorEntity(client, "mppt.outWatts", const.DC_OUT_POWER),
            # OutWattsSensorEntity(client, "pd.carWatts", const.DC_OUT_POWER),

            OutWattsSensorEntity(client, "mppt.carOutWatts", const.DC_CAR_OUT_POWER),
            OutWattsSensorEntity(client, "mppt.dcdc12vWatts", const.DC_ANDERSON_OUT_POWER),

            OutWattsSensorEntity(client, "pd.typec1Watts", const.TYPEC_1_OUT_POWER),
            OutWattsSensorEntity(client, "pd.typec2Watts", const.TYPEC_2_OUT_POWER),

            OutWattsSensorEntity(client, "pd.usb1Watts", const.USB_1_OUT_POWER),
            OutWattsSensorEntity(client, "pd.usb2Watts", const.USB_2_OUT_POWER),

            OutWattsSensorEntity(client, "pd.qcUsb1Watts", const.USB_QC_1_OUT_POWER),
            OutWattsSensorEntity(client, "pd.qcUsb2Watts", const.USB_QC_2_OUT_POWER),

            RemainSensorEntity(client, "ems.chgRemainTime", const.CHARGE_REMAINING_TIME),
            RemainSensorEntity(client, "ems.dsgRemainTime", const.DISCHARGE_REMAINING_TIME),
            CyclesSensorEntity(client, "bmsMaster.cycles", const.CYCLES),

            TempSensorEntity(client, "bmsMaster.temp", const.BATTERY_TEMP),
            TempSensorEntity(client, "bmsMaster.minCellTemp", const.MIN_CELL_TEMP, False),
            TempSensorEntity(client, "bmsMaster.maxCellTemp", const.MAX_CELL_TEMP, False),

            VoltSensorEntity(client, "bmsMaster.vol", const.BATTERY_VOLT, False),
            VoltSensorEntity(client, "bmsMaster.minCellVol", const.MIN_CELL_VOLT, False),
            VoltSensorEntity(client, "bmsMaster.maxCellVol", const.MAX_CELL_VOLT, False),

            # Optional Slave Battery
            LevelSensorEntity(client, "bmsSlave2.soc", const.SLAVE_BATTERY_LEVEL, False, True),
            TempSensorEntity(client, "bmsSlave2.temp", const.SLAVE_BATTERY_TEMP, False, True),
            WattsSensorEntity(client, "bmsSlave2.inputWatts", const.SLAVE_IN_POWER, False, True),
            WattsSensorEntity(client, "bmsSlave2.outputWatts", const.SLAVE_OUT_POWER, False, True)
        ]

    def numbers(self, client: EcoflowMQTTClient) -> list[BaseNumberEntity]:
        return [
            MaxBatteryLevelEntity(client, "ems.maxChargeSoc", const.MAX_CHARGE_LEVEL, 50, 100,
                                  lambda value: {"moduleType": 0, "operateType": "TCP",
                                                 "params": {"id": 49, "maxChgSoc": value}}),
            MinBatteryLevelEntity(client, "ems.minDsgSoc", const.MIN_DISCHARGE_LEVEL, 0, 30,
                                  lambda value: {"moduleType": 0, "operateType": "TCP",
                                                 "params": {"id": 51, "minDsgSoc": value}}),

            MinGenStartLevelEntity(client, "ems.minOpenOilEbSoc", const.GEN_AUTO_START_LEVEL, 0, 30,
                                   lambda value: {"moduleType": 0, "operateType": "TCP",
                                                  "params": {"openOilSoc": value, "id": 52}}),

            MaxGenStopLevelEntity(client, "ems.maxCloseOilEbSoc", const.GEN_AUTO_STOP_LEVEL, 50, 100,
                                  lambda value: {"moduleType": 0, "operateType": "TCP",
                                                 "params": {"closeOilSoc": value, "id": 53}}),

            ChargingPowerEntity(client, "inv.cfgSlowChgWatts", const.AC_CHARGING_POWER, 200, 2900,
                                lambda value: {"moduleType": 0, "operateType": "TCP",
                                               "params": {"slowChgPower": value, "id": 69}}),

        ]

    def switches(self, client: EcoflowMQTTClient) -> list[BaseSwitchEntity]:
        return [
            BeeperEntity(client, "mppt.beepState", const.BEEPER,
                         lambda value: {"moduleType": 0, "operateType": "TCP", "params": {"id": 38, "enabled": value}}),
            EnabledEntity(client, "mppt.carState", const.DC_ENABLED,
                          lambda value: {"moduleType": 0, "operateType": "TCP",
                                         "params": {"id": 81, "enabled": value}}),
            EnabledEntity(client, "inv.cfgAcEnabled", const.AC_ENABLED,
                          lambda value: {"moduleType": 0, "operateType": "TCP",
                                         "params": {"id": 66, "enabled": value}}),

            EnabledEntity(client, "inv.cfgAcXboost", const.XBOOST_ENABLED,
                          lambda value: {"moduleType": 0, "operateType": "TCP", "params": {"id": 66, "xboost": value}}),

            EnabledEntity(client, "inv.acPassByAutoEn", const.AC_ALWAYS_ENABLED,
                          lambda value: {"moduleType": 0, "operateType": "TCP", "params": {"id": 84, "enabled": value}})
        ]

    def selects(self, client: EcoflowMQTTClient) -> list[BaseSelectEntity]:
        return [
            DictSelectEntity(client, "mppt.cfgDcChgCurrent", const.DC_CHARGE_CURRENT, const.DC_CHARGE_CURRENT_OPTIONS,
                             lambda value: {"moduleType": 0, "operateType": "TCP",
                                            "params": {"currMa": value, "id": 71}}),

            TimeoutDictSelectEntity(client, "pd.lcdOffSec", const.SCREEN_TIMEOUT, const.SCREEN_TIMEOUT_OPTIONS,
                                    lambda value: {"moduleType": 0, "operateType": "TCP",
                                                   "params": {"lcdTime": value, "id": 39}}),

            TimeoutDictSelectEntity(client, "pd.standByMode", const.UNIT_TIMEOUT, const.UNIT_TIMEOUT_OPTIONS_LIMITED,
                                    lambda value: {"moduleType": 0, "operateType": "TCP",
                                                   "params": {"standByMode": value, "id": 33}}),

            TimeoutDictSelectEntity(client, "inv.cfgStandbyMin", const.AC_TIMEOUT, const.AC_TIMEOUT_OPTIONS,
                                    lambda value: {"moduleType": 0, "operateType": "TCP",
                                                   "params": {"standByMins": value, "id": 153}}),

        ]
