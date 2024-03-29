# !/usr/bin/env python
# coding: utf-8
# last update: 20200109

project = "ayuko_lav"

STEP0_make_groups = False
STEP0_organ       = False
STEP1_stats       = True

from os import path, system
from bin import nimb_link
NIMB_HOME = nimb_link.link_with_nimb()
from setup.get_vars import Get_Vars, SetProject
from stats.db_processing import Table
from stats.preprocessing import Preprocess
from distribution import utilities as utils
all_vars = Get_Vars()
project_vars = all_vars.projects[project]
#nimb_stats = SetProject(all_vars.location_vars['local']['NIMB_PATHS']['NIMB_tmp'], all_vars.stats_vars, project).stats

if STEP0_make_groups:
    from bin.step1_make_groups import MakeGroupFile
    MakeGroupFile(project_vars, utils, Table, Preprocess)

if STEP0_organ:
	from bin.step2_get_organ_data import GetOrganData
	GetOrganData(project_vars, Table)

if STEP1_stats:
	from bin.step3_stats import Stats
	Stats(project_vars, utils, Table, Preprocess)
