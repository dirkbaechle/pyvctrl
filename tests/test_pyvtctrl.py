import unittest
import pyvctrl

class TestPyvctrl(unittest.TestCase):

    def test_get_list(self):
        cmd = pyvctrl.listOfGetCommands(['getVitoFlammenStatus'])
        self.assertEqual(2, len(cmd))
        self.assertEqual(cmd[0], '-c')
        self.assertEqual(cmd[1], 'getVitoFlammenStatus')

    def test_get_list_multiple(self):
        cmd = pyvctrl.listOfGetCommands(['getNiveau', 'getNeigung'])
        self.assertEqual(2, len(cmd))
        self.assertEqual(cmd[0], '-c')
        self.assertEqual(cmd[1], 'getNiveau,getNeigung')

    def test_set_list(self):
        cmd = pyvctrl.listOfSetCommands({'setNiveau': '30.0'})
        self.assertEqual(2, len(cmd))
        self.assertEqual(cmd[0], '-c')
        self.assertEqual(cmd[1], '"setNiveau 30.0"')

    def test_set_list_multiple(self):
        cmd = pyvctrl.listOfSetCommands({'setNiveau': '30.0', 'setNeigung': '2.0'})
        self.assertEqual(2, len(cmd))
        self.assertEqual(cmd[0], '-c')
        self.assertEqual(cmd[1], '"setNiveau 30.0,setNeigung 2.0"')

    def test_parse_output(self):
        msg = """getVitoBetriebsart:
Dauernd Normalbetrieb
getVitoBetriebParty:
aus
getVitoTempPartySoll:
20.000000 °C
getVitoBetriebSpar:
aus
getVitoTempRaumNorSoll:
23.000000 °C
getVitoTempRaumRedSoll:
3.000000 °C
getVitoTempAussen:
7.800000 °C
getVitoTempKesselIst:
63.500000 °C
getVitoTempKesselSoll:
74.300003 °C
getVitoStatusFlamme:
aus
getVitoLaufzeitBrenner:
13926.977539 Stunden
getVitoStartsBrenner:
252701.000000 
getVitoKennlinieNeigung:
2.000000 
getVitoBetriebsartHK:
?
getVitoTempVLSoll:
0.000000 °C
getVitoTempRLIst:
55.099998 °C
getVitoStatusPumpeHK:
aus
getVitoTempRaumHK:
20.000000 °C
getVitoStatusPumpeZirku:
aus
getVitoAnlagenschema:
3.000000 
"""
        out = pyvctrl.parseVclientOutput(msg)
        self.assertEqual(out['getVitoBetriebsart'], 'Dauernd Normalbetrieb')
        self.assertEqual(out['getVitoBetriebParty'], 'aus')
        self.assertEqual(out['getVitoTempPartySoll'], '20.0')
        self.assertEqual(out['getVitoBetriebSpar'], 'aus')
        self.assertEqual(out['getVitoTempRaumNorSoll'], '23.0')
        self.assertEqual(out['getVitoTempRaumRedSoll'], '3.0')
        self.assertEqual(out['getVitoTempAussen'], '7.80')
        self.assertEqual(out['getVitoTempKesselIst'], '63.50')
        self.assertEqual(out['getVitoTempKesselSoll'], '74.300003')
        self.assertEqual(out['getVitoStatusFlamme'], 'aus')
        self.assertEqual(out['getVitoLaufzeitBrenner'], '13926.977539')
        self.assertEqual(out['getVitoStartsBrenner'], '252701.0')
        self.assertEqual(out['getVitoKennlinieNeigung'], '2.0')
        self.assertEqual(out['getVitoBetriebsartHK'], '?')
        self.assertEqual(out['getVitoTempVLSoll'], '0.0')
        self.assertEqual(out['getVitoTempRLIst'], '55.099998')
        self.assertEqual(out['getVitoStatusPumpeHK'], 'aus')
        self.assertEqual(out['getVitoTempRaumHK'], '20.0')
        self.assertEqual(out['getVitoStatusPumpeZirku'], 'aus')
        self.assertEqual(out['getVitoAnlagenschema'], '3.0')

    def test_parse_output_known(self):
        allowed = ['getVitoBetriebSpar',
                   'getVitoTempKesselIst']
        msg = """getVitoBetriebsart:
Dauernd Normalbetrieb
getVitoBetriebParty:
aus
getVitoTempPartySoll:
20.000000 °C
getVitoBetriebSpar:
aus
getVitoTempRaumNorSoll:
23.000000 °C
getVitoTempRaumRedSoll:
3.000000 °C
getVitoTempAussen:
7.800000 °C
getVitoTempKesselIst:
63.500000 °C
"""
        out = pyvctrl.parseVclientOutput(msg, allowed)
        self.assertEqual(len(out), 2)
        self.assertEqual(out['getVitoBetriebSpar'], 'aus')
        self.assertEqual(out['getVitoTempKesselIst'], '63.50')

    def test_parse_output_double_key(self):
        allowed = ['getVitoBetriebSpar',
                   'getVitoTempRaumNorSoll',
                   'getVitoTempKesselIst']
        msg = """getVitoBetriebsart:
Dauernd Normalbetrieb
getVitoBetriebParty:
aus
getVitoTempPartySoll:
20.000000 °C
getVitoBetriebSpar:
getVitoTempRaumNorSoll:
23.000000 °C
getVitoTempRaumRedSoll:
3.000000 °C
getVitoTempAussen:
7.800000 °C
getVitoTempKesselIst:
63.500000 °C
"""
        out = pyvctrl.parseVclientOutput(msg, allowed)
        self.assertEqual(len(out), 2)
        self.assertEqual(out['getVitoTempRaumNorSoll'], '23.0')
        self.assertEqual(out['getVitoTempKesselIst'], '63.50')


    def test_parse_output_double_key_auto(self):
        allowed = ['getVitoBetriebSpar',
                   'getVitoTempKesselIst']
        msg = """getVitoBetriebsart:
Dauernd Normalbetrieb
getVitoBetriebParty:
aus
getVitoTempPartySoll:
20.000000 °C
getVitoBetriebSpar:
getVitoTempRaumNorSoll:
23.000000 °C
getVitoTempRaumRedSoll:
3.000000 °C
getVitoTempAussen:
7.800000 °C
getVitoTempKesselIst:
63.500000 °C
"""
        out = pyvctrl.parseVclientOutput(msg, allowed)
        self.assertEqual(len(out), 1)
        self.assertEqual(out['getVitoTempKesselIst'], '63.50')

    def test_parse_output_unknown_key(self):
        allowed = ['getVitoBetriebSpar',
                   'getVitoTempKesselIst']
        msg = """getVitoBetriebsart:
Dauernd Normalbetrieb
getVitoBetriebParty:
aus
getVitoTempPartySoll:
20.000000 °C
getVitoBetriebXSpar:
aus
getVitoTempRaumNorSoll:
23.000000 °C
getVitoTempRaumRedSoll:
3.000000 °C
getVitoTempAussen:
7.800000 °C
getVitoTempKesselIst:
63.500000 °C
"""
        out = pyvctrl.parseVclientOutput(msg, allowed)
        self.assertEqual(len(out), 1)
        self.assertEqual(out['getVitoTempKesselIst'], '63.50')

    def test_parse_output_leading_junk(self):
        allowed = ['getVitoBetriebSpar',
                   'getVitoTempKesselIst']
        msg = """Dies
ist
ein
Test
getVitoBetriebSpar:
aus
getVitoTempKesselIst:
63.500000 °C"""
        out = pyvctrl.parseVclientOutput(msg, allowed)
        self.assertEqual(len(out), 2)
        self.assertEqual(out['getVitoBetriebSpar'], 'aus')
        self.assertEqual(out['getVitoTempKesselIst'], '63.50')

    def test_parse_output_middle_junk(self):
        allowed = ['getVitoBetriebSpar',
                   'getVitoTempKesselIst']
        msg = """getVitoBetriebsart:
Dauernd Normalbetrieb
getVitoBetriebParty:
aus
getVitoTempPartySoll:
20.000000 °C
getVitoBetriebSpar:
aus
Dies
ist
ein
Test
getVitoTempKesselIst:
63.500000 °C"""
        out = pyvctrl.parseVclientOutput(msg, allowed)
        self.assertEqual(len(out), 2)
        self.assertEqual(out['getVitoBetriebSpar'], 'aus')
        self.assertEqual(out['getVitoTempKesselIst'], '63.50')

    def test_float_reduce(self):
        out = pyvctrl.reduceFloatValue('0.0003000')
        self.assertEqual(out, '0.00030')
        out = pyvctrl.reduceFloatValue('0.300000')
        self.assertEqual(out, '0.30')
        out = pyvctrl.reduceFloatValue('0.')
        self.assertEqual(out, '0.')
        out = pyvctrl.reduceFloatValue('0.3')
        self.assertEqual(out, '0.3')
        out = pyvctrl.reduceFloatValue('0.30')
        self.assertEqual(out, '0.30')

        out = pyvctrl.reduceFloatValue('0,0003000')
        self.assertEqual(out, '0,00030')
        out = pyvctrl.reduceFloatValue('0,300000')
        self.assertEqual(out, '0,30')
        out = pyvctrl.reduceFloatValue('0,')
        self.assertEqual(out, '0,')
        out = pyvctrl.reduceFloatValue('0,3')
        self.assertEqual(out, '0,3')
        out = pyvctrl.reduceFloatValue('0,30')
        self.assertEqual(out, '0,30')

        out = pyvctrl.reduceFloatValue('0.0003000 als test')
        self.assertEqual(out, '0.0003000 als test')
        out = pyvctrl.reduceFloatValue('0.300000 Celsius')
        self.assertEqual(out, '0.30')
