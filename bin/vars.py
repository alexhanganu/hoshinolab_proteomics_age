#!/bin/python


class VARS():
    def __init__(self, project_vars):
        self.project_vars       = project_vars


    def f_and_sheets(self):
        f_src_subs  = "info.xlsx"
        cols = ['ID', 'File name', 'sample name', 'age']
        # f_src_60    = "Ayuko_Lyden_autism_project_all_60_samples_PD.xlsx"
        # f_src_dJon  = "MS151970QE_Bruno_Lyden_control_dad_Jon.xlsx"
        # f_src_d_ct  = "MS151649QE_Bruno_Lyden_control2_dad.xlsx"
        # f_src_m_hz  = "MS151970QE_Bruno_Lyden_control_mom_HZ.xlsx"
        # f_src_m_ct1 = "MS151649QE_Bruno_Lyden_control1_mom.xlsx"
        # f_src_p_ea  = "MS151970QE_Bruno_Lyden_PNC_EA.xlsx"
        # f_src_p_dg  = "MS151818QE_Bruno_Lyden_PNC_DG.xlsx"
        # f_src_p_fs  = "MS151818QE_Bruno_Lyden_PNC_FS.xlsx"
        # f_src_p_ss  = "MS151818QE_Bruno_Lyden_PNC_SS.xlsx"
        # f_src_p_jm  = "MS151970QE_Bruno_Lyden_PNC_JM.xlsx"
        # f_src_p_eg  = "MS151970QE_Bruno_Lyden_PNC_EG.xlsx"
        # f_src_autsm = "MS162577_Ayuko_Lyden_autism_all_data_PD.xlsx"
        return {'file_src': f_src_subs,
                          'cols': cols}
