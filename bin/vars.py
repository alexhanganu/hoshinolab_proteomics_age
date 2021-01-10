#!/bin/python

from os import path

class VARS():
    def __init__(self, materials_DIR):
        self.materials_DIR = materials_DIR

    def f_src(self):
        f_src_subs  = path.join(self.materials_DIR, "source", "data for Alex and Lav", "info.xlsx")
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
                file_path = path.join(self.materials_DIR, "source", "data for Alex and Lav", f"{cur_file_name}.xlsx")
            _ids_files[df.at[ix, _id]] = {
                'file_name' : cur_file_name,
                'file_path' : file_path,
                }
        return _ids_files

    def param_names(self):
        return {"protein_id" : "Accession", "param" : "Area"}

    def rows_2rm_per_file(self):
        return {"Ayuko_Lyden_autism_project_all_60_samples_PD": [0], "MS162577_Ayuko_Lyden_autism_all_data_PD": [0]}

    def files_multi_ids(self):
        return ["Ayuko_Lyden_autism_project_all_60_samples_PD",]

    def get_cols_2read(self):
        return {"MS162577_Ayuko_Lyden_autism_all_data_PD" : ["Unnamed: 0", "control_AH_1"],}

