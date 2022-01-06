#!/bin/sh 
set -x

vclient -c getVitoBetriebsart
vclient -c getVitoBetriebParty
vclient -c getVitoTempPartySoll
vclient -c getVitoBetriebSpar
vclient -c getVitoTempRaumNorSoll
vclient -c getVitoTempRaumRedSoll
vclient -c getVitoTempAussen
vclient -c getVitoTempKesselIst
vclient -c getVitoTempKesselSoll
vclient -c getVitoStatusFlamme
vclient -c getVitoLaufzeitBrenner
vclient -c getVitoStartsBrenner
vclient -c getVitolaKennlinieNeigung
vclient -c getVitolaKennlinieNiveau
vclient -c getVitoBetriebsartHK
vclient -c getVitoTempVLSoll
vclient -c getVitoTempRLIst
vclient -c getVitoStatusPumpeHK
vclient -c getVitoTempRaumHK
vclient -c getVitoStatusPumpeZirku
vclient -c getVitoAnlagenschema
