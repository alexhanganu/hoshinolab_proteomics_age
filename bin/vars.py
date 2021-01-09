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
        cur_file_name = ''
        for ix in df.index:
            file_name = df.at[ix, self.f_src()['col_files']].strip('.xlsx')
            if file_name != cur_file_name:
                cur_file_name = file_name
                file_path = path.join(self.materials_DIR, f'{cur_file_name}.xlsx')                
            _ids_files[df.at[ix, _id]] = {
                'file_name' : cur_file_name,
                'file_path' : file_path,
                }
        return _ids_files

    def param_names(self):
        return {"protein_id" : "Accession", "param" : "Area"}

    def files_2rm_2ndrow(self):
        return ["Ayuko_Lyden_autism_project_all_60_samples_PD", "MS162577_Ayuko_Lyden_autism_all_data_PD"]

    def get_cols_2read(self):
        cols_1st_line = list(self.param_names().values())
        return {
            "Ayuko_Lyden_autism_project_all_60_samples_PD" : ["Accession", "Area"],
            "MS162577_Ayuko_Lyden_autism_all_data_PD"      : ["Unnamed: 0", "control_AH_1"],
            "MS151970QE_Bruno_Lyden_control_dad_Jon"       : cols_1st_line,
            "MS151649QE_Bruno_Lyden_control2_dad"          : cols_1st_line,
            "MS151970QE_Bruno_Lyden_control_mom_HZ"        : cols_1st_line,
            "MS151649QE_Bruno_Lyden_control1_mom"          : cols_1st_line,
            "MS151970QE_Bruno_Lyden_PNC_EA"                : cols_1st_line,
            "MS151818QE_Bruno_Lyden_PNC_DG"                : cols_1st_line,
            "MS151818QE_Bruno_Lyden_PNC_FS"                : cols_1st_line,
            "MS151818QE_Bruno_Lyden_PNC_SS"                : cols_1st_line,
            "MS151970QE_Bruno_Lyden_PNC_JM"                : cols_1st_line,
            "MS151970QE_Bruno_Lyden_PNC_EG"                : cols_1st_line,
            }

