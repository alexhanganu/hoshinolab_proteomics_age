#!/bin/python

from os import path, environ, sep
from .nimb_link import get_Nimb_Home, get_home_dir
import pandas as pd
import time
date = str(time.strftime('%Y%m%d', time.localtime()))
import logging

log = logging.getLogger(__name__)
logging.basicConfig(format='%(message)s')
log.setLevel(logging.INFO)

# from datetime import date
# dt = date.today().strftime('%Y%m%d')
# dt=str(datetime.now().year)+str(datetime.now().month)+str(datetime.now().day)

class VARS():
    def __init__(self, project_vars):
        self.home               = get_home_dir()
        self.project_vars       = project_vars
        self.tmp_MR_data_file   = 'tmp/step0_prep1_path_2MR_files.json'
        self.tmp_FSnotprocessed = 'tmp/step0_prep1_fs_scans_notprocessed.json'
        self.f_missing_values   = 'tmp/step0_prep2_values_missing.json'


    def f_and_sheets(self):
    	f_src_subs  = "info.xlsx"
        f_src_60    = "Ayuko_Lyden_autism_project_all_60_samples_PD.xlsx"
        f_src_dJon  = "MS151970QE_Bruno_Lyden_control_dad_Jon.xlsx"
        f_src_d_ct  = "MS151649QE_Bruno_Lyden_control2_dad.xlsx"
        f_src_m_hz  = "MS151970QE_Bruno_Lyden_control_mom_HZ.xlsx"
        f_src_m_ct1 = "MS151649QE_Bruno_Lyden_control1_mom.xlsx"
        f_src_p_ea  = "MS151970QE_Bruno_Lyden_PNC_EA.xlsx"
        f_src_p_dg  = "MS151818QE_Bruno_Lyden_PNC_DG.xlsx"
        f_src_p_fs  = "MS151818QE_Bruno_Lyden_PNC_FS.xlsx"
        f_src_p_ss  = "MS151818QE_Bruno_Lyden_PNC_SS.xlsx"
        f_src_p_jm  = "MS151970QE_Bruno_Lyden_PNC_JM.xlsx"
        f_src_p_eg  = "MS151970QE_Bruno_Lyden_PNC_EG.xlsx"
        f_src_autsm = "MS162577_Ayuko_Lyden_autism_all_data_PD.xlsx"
        return {'subjects':{'file': f_src_subs,
                          'cols': "area"}
