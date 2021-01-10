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
        self.param_names   = self.vars.param_names()

        self.run()

    def run(self):
        '''
            reading the info.xlsx file, extracting list of IDs and corresponding
            files with data
        '''
        self.df_src     = self.tab.get_df(self.vars.f_src()['file_src'])
        self._ids_files = self.vars.get_ids_and_data_files(self.df_src, self._id)
        self.populate_grid()
        self.concatenate_dfs()
        self.grid_df = self.tab.rm_rows_with_nan(self.grid_df)
        self.grid_df = self.grid_df.transpose()
        self.create_data_file()


    def populate_grid(self):
        """Extract data for IDs from corresponding files, from defined columns
            transpose data so that ID becomes index, and data are transposed
            feature names are taken from each file, from a defined column
        """
        self.df_all_data = dict()
        self.col_2set_index = self.param_names["protein_id"]
        multi_ids = list()
        for _id in list(self._ids_files.keys()):
            file_2read = self._ids_files[_id]['file_name']
            if file_2read not in self.vars.files_multi_ids():
                self.read_id_per_file(file_2read, _id)
            else:
                if _id not in multi_ids:
                    multi_ids.append(_id)
        if multi_ids:
            self.read_multiples_ids_from_file(multi_ids)

    def read_multiples_ids_from_file(self, multi_ids):
        file_2read = self._ids_files[multi_ids[0]]['file_name']
        file_path  = self._ids_files[multi_ids[0]]['file_path']
        df = self.tab.get_df(file_path)
        # df.drop(self.vars.rows_2rm_per_file()[file_2read], inplace = True)
        cols_2rename = {df.columns.tolist()[0]: self.col_2set_index}
        df.rename(columns = cols_2rename, inplace=True)
        for _id in multi_ids:
            df_id = df[[self.col_2set_index, _id]]
            df_id = self.adjust_rm_rows(df_id, self.vars.rows_2rm_per_file()[file_2read])
            df_id = self.tab.rm_rows_with_nan(df_id, self.col_2set_index, reset_index = True)
            df_id = self.prepare_df_for_grid(df_id, _id)
            self.df_all_data[_id] = df_id


    def read_id_per_file(self, file_2read, _id):
        file_path  = self._ids_files[_id]['file_path']
        cols = list(self.param_names.values())
        if file_2read in self.vars.get_cols_2read():
            cols = self.vars.get_cols_2read()[file_2read]
        df = self.tab.get_df(file_path, cols = cols)
        if file_2read in self.vars.rows_2rm_per_file():
            df = self.adjust_rm_rows(df, self.vars.rows_2rm_per_file()[file_2read])
        df = self.tab.rm_rows_with_nan(df, self.col_2set_index, reset_index = True)
        df = self.prepare_df_for_grid(df, _id)
        self.df_all_data[_id] = df

    def prepare_df_for_grid(self, df, _id):
        df.rename(columns = {df.columns.tolist()[-1]: _id}, inplace=True)
        df = self.tab.change_index(df, self.col_2set_index)
        return df

    def adjust_rm_rows(self, df, rows):
        '''
            two files have the parameters in the second row
            script changes row names
            returns df with structure: col1, col2
        '''
        df.rename(columns = {df.columns.tolist()[0]: self.col_2set_index}, inplace=True)
        df.drop(rows, inplace = True)
        df.reset_index(drop = True, inplace = True)
        return df

    def concatenate_dfs(self):
        frames       = (self.df_all_data[i] for i in self.df_all_data)
        self.grid_df = self.tab.concat_dfs(frames, ax=1, sort=True)

    def create_data_file(self):
        '''
            save final grid file to use for stats
        '''
        path_name_f2save   = path.join(self.materials_DIR, self.project_vars["GLM_file_group"])
        print('creating file with groups {}'.format(path_name_f2save))
        self.tab.save_df(self.grid_df, path_name_f2save, sheet_name = 'grid')
