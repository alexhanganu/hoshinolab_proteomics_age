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
        self.vars_4glm     = project_vars['variables_for_glm']
        self.materials_DIR = project_vars["materials_DIR"][1]
        self.vars          = VARS(self.materials_DIR, project_vars)
        self.param_names   = self.vars.param_names()

        self.run()

    def run(self):
        '''
            reading the info.xlsx file, extracting list of IDs and corresponding
            files with data
        '''
        self.df_src    = self.tab.get_df(self.vars.f_src()['file_src'])
        self._src_data = self.vars.get_data_from_src_file(self.df_src)
        self.populate_grid()
        self.concatenate_dfs()
        # self.grid_df = self.tab.rm_rows_with_nan(self.grid_df) #!!!!!!!!!!!! UNCOMMENT
        # self.grid_df = self.grid_df.transpose()
        self.grid_df.index.name = self._id
        self.create_data_file()


    def populate_grid(self):
        """Extract data for IDs from corresponding files, from defined columns
            transpose data so that ID becomes index, and data are transposed
            feature names are taken from each file, from a defined column
        """
        self.df_all_data = dict()
        self.col_2set_index = self.param_names["protein_id"]
        multi_ids = {i: list() for i in self.vars.files_multi_ids()}
        for _id in list(self._src_data.keys()):
            file_2read = self._src_data[_id]['file_name']
            if file_2read in multi_ids:
                    multi_ids[file_2read].append(_id)
            else:
                self.read_id_per_file(file_2read, _id)
        self.read_multiples_ids_from_file(multi_ids)

    def read_multiples_ids_from_file(self, multi_ids):
        ''' iterate through files that contain multiple ids
            extract each id
        '''
        for file in list(multi_ids.keys()):
            file_2read = self._src_data[multi_ids[file][0]]['file_name']
            file_path = self._src_data[multi_ids[file][0]]['file_path']
            print(file_2read, file_path)

            df = self.tab.get_df(file_path)
            if file_2read in self.vars.rows_2rm_per_file():
                df.drop(self.vars.rows_2rm_per_file()[file_2read], inplace = True)
            cols_2rename = {df.columns.tolist()[0]: self.col_2set_index}
            df.rename(columns = cols_2rename, inplace=True)
            for _id in multi_ids[file]:
                df_id = df[[self.col_2set_index, _id]]
                # df_id = self.adjust_rm_rows(df_id, self.vars.rows_2rm_per_file()[file_2read])
                df_id = self.tab.rm_rows_with_nan(df_id, self.col_2set_index, reset_index = True)
                df_id = self.add_variables_4glm(df_id, _id)
                df_id = self.prepare_df_for_grid(df_id, _id)
                self.df_all_data[_id] = df_id
            # print(self.df_all_data)#[_id])


    def read_id_per_file(self, file_2read, _id):
        file_path  = self._src_data[_id]['file_path']
        cols = list(self.param_names.values())
        if file_2read in self.vars.get_cols_2read():
            cols = self.vars.get_cols_2read()[file_2read]
        df = self.tab.get_df(file_path, cols = cols)
        if file_2read in self.vars.rows_2rm_per_file():
            df = self.adjust_rm_rows(df, self.vars.rows_2rm_per_file()[file_2read])
        df = self.tab.rm_rows_with_nan(df, self.col_2set_index, reset_index = True)
        df = self.add_variables_4glm(df, _id)
        df = self.prepare_df_for_grid(df, _id)
        self.df_all_data[_id] = df

    def add_variables_4glm(self, df, _id):
        param_2populate = self.param_names['param']
        for var in self.vars_4glm:
            var_value = self._src_data[_id][var] 
            df.at[-1, self.col_2set_index] = var
            if param_2populate in df.columns:
                df.at[-1, param_2populate]         = var_value
            else:
                df.at[-1, df.columns.tolist()[-1]] = var_value
        return df

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
        frames       = (self.df_all_data[_id] for _id in self.df_all_data)
        self.grid_df = self.tab.concat_dfs(frames, ax=1, sort=True)

    def create_data_file(self):
        '''
            save final grid file to use for stats
        '''
        path_name_f2save   = path.join(self.materials_DIR, self.project_vars["GLM_file_group"])
        print('creating file with groups {}'.format(path_name_f2save))
        self.tab.save_df(self.grid_df, path_name_f2save, sheet_name = 'grid')
