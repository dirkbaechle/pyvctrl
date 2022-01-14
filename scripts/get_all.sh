#!/bin/sh 
set -x

vclient -c getVitoBetriebsart
vclient -c getVitoBetriebParty
vclient -c getVitoTempPartySoll
vclient -c getVitoBetriebSpar
vclient -c getVitoTempRaumNorSoll
vclient -c getVitoTempRaumRedSoll
vclient -c getVitoTempAussen
vclient -c getVitoTempAussenTp
vclient -c getVitoTempAussenAged
vclient -c getVitoTempAussenMid
vclient -c getVitoTempKesselIst
vclient -c getVitoTempKesselSoll
vclient -c getVitoTempSpeicher
vclient -c getVitoStatusFlamme
vclient -c getVitoLaufzeitBrenner
vclient -c getVitoStartsBrenner
vclient -c getVitoKennlinieNeigung
vclient -c getVitoKennlinieNiveau
vclient -c getVitoBetriebsartHK
vclient -c getVitoTempVLSoll
vclient -c getVitoTempVL
vclient -c getVitoTempRL17A
vclient -c getVitoTempRLIst
vclient -c getVitoStatusPumpeHK
vclient -c getVitoTempRaumHK
vclient -c getVitoStatusPumpeZirku
vclient -c getVitoStatusStoerung
vclient -c getVitoAnlagenschema
vclient -c getVitoDevType
vclient -c getVitoCtrlId
vclient -c getVitoInventory
vclient -c getVitoInvCodePlug
vclient -c getVitoPanelSWIndex
