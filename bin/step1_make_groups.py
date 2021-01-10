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
        cols_2read = self.vars.get_cols_2read()
        files_2rm_2ndrow = self.vars.files_2rm_2ndrow()
        param_names = self.vars.param_names()
        file_path_current = ''
        for _id in list(_ids_files.keys())[54:]:
            print(_id)
            file_2read = _ids_files[_id]['file_name']
            file_path  = _ids_files[_id]['file_path']
            file_cols_2read  = cols_2read[file_2read]
            if file_path != file_path_current:
                file_path_current = file_path
            df_id_data = self.tab.get_df(file_path_current, cols = file_cols_2read)
            df_id_data = self.tab.rm_rows_with_nan(df_id_data, file_cols_2read[0])
            if file_2read in files_2rm_2ndrow:
                df_id_data = self.adjust_for_2nd_row(df_id_data, param_names["param"])
            df_id_data.rename(columns = {df_id_data.columns.tolist()[-1]: _id}, inplace=True)
            df_id_data = self.tab.change_index(df_id_data, param_names["protein_id"])
            df_all_data[_id] = df_id_data
        frames = (df_all_data[i] for i in df_all_data)
        self.grid_df = self.tab.concat_dfs(frames, ax=1, sort=True)
        self.create_data_file()

    def adjust_for_2nd_row(self, df, param):
        '''
            two files have the parameters in the second row
            script changes row names
            returns df with structure: col1, col2
        '''
        df.columns = df.iloc[0]
        df.drop([0], inplace = True)
        return df

    def create_data_file(self):
        path_name_f2save   = path.join('/home/ssp/Desktop', self.project_vars["GLM_file_group"])
        print('creating file with groups {}'.format(path_name_f2save))
        self.tab.save_df(self.grid_df, path_name_f2save, sheet_name = 'grid')
