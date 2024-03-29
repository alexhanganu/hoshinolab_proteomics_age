#!/bin/python

from os import path

class VARS():
    def __init__(self, materials_DIR, project_vars):
        self.materials_DIR  = materials_DIR
        self.vars_4glm      = project_vars['variables_for_glm']
        self._id            = project_vars['id_col']
        self.path_2src_data = path.join(self.materials_DIR,
                                        "sourcedata",
                                        "data for Alex and Lav")

    def f_src(self):
        f_src_subs  = path.join(self.path_2src_data,
                                "info.xlsx")
        grid_name   = 'grid'
        grid_f      = path.join(self.materials_DIR,
                                f"{grid_name}.csv")
        col_files = 'File name'
        return {'file_src' : f_src_subs,
                'col_files': col_files,
                'grid_name': grid_name,
                'grid_file': grid_f,
                'index'    : 'sample name'}

    def get_data_from_src_file(self, df):
        _src_data = {}
        cur_file_name = ''
        for ix in df.index:
            index_val = df.at[ix, self._id]
            file_name = df.at[ix, self.f_src()['col_files']].replace('.xlsx','')
            if file_name != cur_file_name:
                cur_file_name = file_name
                file_path = path.join(self.path_2src_data,
                                      f"{cur_file_name}.xlsx")
            _src_data[index_val] = {
                                        'file_name' : cur_file_name,
                                        'file_path' : file_path,
                                        }
            for var in self.vars_4glm:
                var_value = df.at[ix, var]
                _src_data[index_val][var] = var_value
        return _src_data

    def param_names(self):
        return {"protein_id" : "Accession", "param" : "Area"}

    def rows_2rm_per_file(self):
        return {"Ayuko_Lyden_autism_project_all_60_samples_PD": [0],
                "MS162577_Ayuko_Lyden_autism_all_data_PD": [0],
                "MS183640_Alberto_Lyden_complete_analysis": [0],
                "MS216945QEHF_Ayuko_Hoshino": [0]}

    def files_multi_ids(self):
        return ["MS216945QEHF_Ayuko_Hoshino",
        		"MS183640_Alberto_Lyden_complete_analysis",
                "Ayuko_Lyden_autism_project_all_60_samples_PD",
                ]

    def get_cols_2read(self):
        return {"MS162577_Ayuko_Lyden_autism_all_data_PD" :
                        ["Unnamed: 0", "control_AH_1"],}

    def lav_f_src(self):
        lav_f_src  = path.join(self.materials_DIR,
                               "sourcedata",
                               "lav",
                               "organ_source_distribution_Ayuko_Lyden_autism_project_all_60_samples_PD_per_protein.csv")
        grid_name   = 'lav_organ_source_grid'
        grid_f      = path.join(self.materials_DIR, f"{grid_name}.csv")

        return {'file_src': lav_f_src,
                'index': 'protein id',
                'grid_name': grid_name,
                'grid_file': grid_f,
                'index'    : 'protein id'}
