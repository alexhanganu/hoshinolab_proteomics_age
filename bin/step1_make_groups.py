#!/bin/python
# -*- coding: utf-8 -*-
#Alexandru Hanganu, 20200109

''' Read the source file with data
    extracts the corresponding variables
    checks that ids are present
    checks all variables
    excludes subjects from analysis, based on rules
Args:
    project variables (nimb style)
Return:
    True or False if all steps are correct and finished
'''

from os import path 
from .vars import VARS


class MakeGroupFile:
    def __init__(self, project_vars, utils, Table, Preprocess):
        self.tab           = Table()
        self.preproc       = Preprocess()
        self.project_vars  = project_vars
        self._id           = project_vars['id_col']
        self.group_param   = project_vars['group_param']
        self.materials_DIR = project_vars["materials_DIR"][1]
        self.vars          = VARS(self.materials_DIR)
        self.src_file      = self.vars.f_src()['file_src']

        self.run()

    def run(self):
        '''
            reading the info.xlsx file, extracting list of IDs and corresponding
            files with data
        '''
        src_file_path = path.join(self.materials_DIR, self.src_file)
        self.df       = self.tab.get_df(src_file_path)
        _ids_files = self.vars.get_ids_and_data_files(self.df, self._id)
        self.populate_grid_with_col_data_transposed(_ids_files)
        # self.df.set_index(self._id, inplace = True)
        # self.create_data_file()


    def populate_grid_with_col_data_transposed(self, _ids_files):
        """Extract data for IDs from corresponding files, from defined columns
            transpose data so that ID becomes index, and data are transposed
            feature names are taken from each file, from a defined column
        """
        df_all_data = dict()
        for _id in _ids_files:
            file_2read = _ids_files[_id]['file']
            col_2read  = _ids_files[_id]['col2read']
            df_id_data = self.tab.get_df(file_2read, col_2read)
        #     df_id_data = self.preproc.populate_missing_vals_2mean(df_id_data, cols_with_nans)
        #     df_all_data[_id] = df_id_data
        # frames = (df_all_data[i] for i in df_all_data)
        # df_meaned_vals = pd.concat(frames, axis=0, sort=True)
        # for col in cols_with_nans:
        #     self.grid_df[col] = df_meaned_vals[col]

    def create_data_file(self):
        file_path_name = path.join(self.materials_DIR, self.project_vars["GLM_file_group"])
        print('creating file with groups {}'.format(file_path_name))
        self.tab.save_df(self.grid_df, file_path_name, sheet_name = 'grid')
