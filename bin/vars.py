#!/bin/python

from os import path

class VARS():
    def __init__(self, materials_DIR):
        self.materials_DIR       = materials_DIR

    def f_src(self):
        f_src_subs  = "info.xlsx"
        col_files = 'File name'
        return {'file_src': f_src_subs,
                'col_files': col_files}

    def get_ids_and_data_files(self, df, _id):
        _ids_files = {}
        for ix in df.index:
            _ids_files[df.at[ix, _id]] = {
                'file': path.join(self.materials_DIR, df.at[ix, self.f_src()['col_files']]),
                }
        return _ids_files

    def get_cols_2read(self):
        return {
            "Ayuko_Lyden_autism_project_all_60_samples_PD.xlsx" : "",
            "MS151970QE_Bruno_Lyden_control_dad_Jon.xlsx"       : "",
            "MS151649QE_Bruno_Lyden_control2_dad.xlsx"          : "",
            "MS151970QE_Bruno_Lyden_control_mom_HZ.xlsx"        : "",
            "MS151649QE_Bruno_Lyden_control1_mom.xlsx"          : "",
            "MS151970QE_Bruno_Lyden_PNC_EA.xlsx"                : "",
            "MS151818QE_Bruno_Lyden_PNC_DG.xlsx"                : "",
            "MS151818QE_Bruno_Lyden_PNC_FS.xlsx"                : "",
            "MS151818QE_Bruno_Lyden_PNC_SS.xlsx"                : "",
            "MS151970QE_Bruno_Lyden_PNC_JM.xlsx"                : "",
            "MS151970QE_Bruno_Lyden_PNC_EG.xlsx"                : "",
            "MS162577_Ayuko_Lyden_autism_all_data_PD.xlsx"      : "",
            }

