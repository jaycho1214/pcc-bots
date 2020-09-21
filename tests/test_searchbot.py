import pytest
import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.absolute()))

from lib.searchbot import searchbot

class TestSearchbot:
    @pytest.fixture
    def testcase(self, file_name=str(Path(__file__).parent) + "/data/testcase_fall20.json"):
        try:
            with open(file_name) as f:
                test_case = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(file_name + " file not found!")
        return test_case

    @pytest.fixture
    def bot(self):
        return searchbot(year=2020, term="Fall")

    # initialize
    def test_initialize(self, bot):
        assert bot.form_data is not None, 'Form data is not initialized'
        assert bot.html is not None, 'Html is not fetched'

        macro = searchbot(init=False)
        assert macro.form_data is None, 'Should be not initialized'
        assert macro.html is None, 'Should be not initialized'

    # setData
    @pytest.mark.xfail
    def test_setdata_filename(self):
        macro = searchbot(init=False)
        macro.setData(year=2020, term="Wrong Semester")

    def test_setdata_name(self):
        macro = searchbot(init=False)
        macro.setData(year=2025, term="sPrInG")
        assert macro.form_data[0][1] == '202530', 'Wrong Form Data'

        macro.setData(year=2008, term="wInTeR  ")
        assert macro.form_data[0][1] == '200810', 'Wrong Form Data'

        macro.setData(year=2010, term="  fAlL  ")
        assert macro.form_data[0][1] == '201070', 'Wrong Form Data'

        macro.setData(year=2001, term="      sumMeR")
        assert macro.form_data[0][1] == '200150', 'Wrong Form Data'

    @pytest.mark.xfail(reason="No File Exists")
    def test_setdata_file(self):
        macro = searchbot(init=False)
        macro.setData(year=2020, term="Spring", file_name="abcdefghijk.json")

    def test_setdata_json(self, file_name="testjson.json"):
        macro = searchbot(init=False)
        macro.setData(9999, 'Winter', "/tests/data/" + file_name)
        test_form_data = [
            ['TERM', '999910'],
            ['TERM_DESC', 'Winter 9999'],
            ['sel_subj', 'dummy'],
            ['sel_subj', '%'],
            ['sel_day', 'dummy'],
            ['sel_schd', 'dummy'],
            ['sel_schd', '%'],
            ['sel_camp', 'dummy'],
            ['sel_camp', '%'],
            ['sel_ism', 'dummy'],
            ['sel_ism', '%'],
            ['sel_sess', 'dummy'],
            ['sel_sess', '%'],
            ['sel_instr', 'dummy'],
            ['sel_instr', '%'],
            ['sel_ptrm', 'dummy'],
            ['sel_ptrm', '%'],
            ['sel_attrib', 'dummy'],
            ['sel_attrib', '%'],
            ['sel_crse', ''],
            ['sel_crn', ''],
            ['sel_title', ''],
            ['begin_hh', '5'],
            ['begin_mi', '0'],
            ['begin_ap', 'a'],
            ['end_hh', '11'],
            ['end_mi', '0'],
            ['end_ap', 'p'],
            ['aa', 'N'],
            ['bb', 'N'],
            ['ee', 'N'],
            ]
        assert macro.form_data == test_form_data, 'Json improperly imported'

    # getTable
    def test_getTable(self, bot, testcase):
        crns = testcase['test_getTable']

        for crn in crns:
            bot.getTable(crn)
            assert bot.tr is not None, 'Data should not be empty'

    @pytest.mark.skip(reason="Not supported Yet!")
    def test_getTable_none(self, bot, testcase):
        crns_fail = testcase['test_getTable_none']

        for crn in crns_fail:
            pytest.raises(Exception, bot.getTable, crn)

    # getProf and getSeats
    def test_getData(self, bot, testcase):
        testcase = testcase['test_getData']
        for row in testcase:
            bot.getTable(row[0])
            assert bot.getProf() == row[1]
            assert bot.getSeats() == str(row[2])

    # getClass
    def test_getClass(self, bot, testcase):
        testcase = testcase['test_getClass']
        for row in testcase:
            bot.getTable(row[0])
            assert bot.getClass() == row[1]
