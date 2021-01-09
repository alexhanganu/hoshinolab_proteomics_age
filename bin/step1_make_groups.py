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
        self.tab          = Table()
        self.preproc      = Preprocess()
        self.project_vars = project_vars
        self._id          = project_vars['id_col']
        self.group_param  = project_vars['group_param']
        self.materials_DIR = project_vars["materials_DIR"][1]
        self.vars         = VARS(project_vars)
        self.src_file     = self.vars.f_src()['file_src']

        self.run()

    def run(self):
        '''
            reading the info.xlsx file, extracting list of IDs and corresponding
            files with data
        '''
        src_file_path = path.join(self.project_vars['materials_DIR'][1], self.src_file)
        self.df       = self.tab.get_df(src_file_path)
        _ids_files = self.vars.get_ids_and_data_files(self.df, self._id)
        for key in _ids_files:
            print(key, _ids_files[key])
        # self.populate_grid_with_col_data_transposed()
        # self.df.set_index(self._id, inplace = True)
        # self.create_data_file()


    def populate_grid_with_col_data_transposed(self):
        """Extract data for IDs from corresponding files, from defined columns
            transpose data so that ID becomes index, and data are transposed
            feature names are taken from each file, from a defined column
        """
        for group in self.groups:
            df_group = self.tab.get_df_per_parameter(self.grid_df, self.project_vars['group_col'], group)
            df_group = self.preproc.populate_missing_vals_2mean(df_group, cols_with_nans)
            df_groups[group] = df_group
        frames = (df_groups[i] for i in df_groups)
        df_meaned_vals = pd.concat(frames, axis=0, sort=True)
        for col in cols_with_nans:
            self.grid_df[col] = df_meaned_vals[col]

    def create_data_file(self):
        file_path_name = path.join(self.materials_DIR, self.project_vars["GLM_file_group"])
        print('creating file with groups {}'.format(file_path_name))
        self.tab.save_df(self.grid_df, file_path_name, sheet_name = 'grid')
