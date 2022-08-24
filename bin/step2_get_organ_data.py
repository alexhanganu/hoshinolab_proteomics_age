#!/bin/python
# -*- coding: utf-8 -*-
#Alexandru Hanganu, 20200311

''' Read organ based analysis from Lav Varshney
Args:


Return:


'''

from os import path 
from .vars import VARS


class GetOrganData:
    def __init__(self, project_vars, Table):
        self.tab           = Table()
        self.project_vars  = project_vars
        self._id           = project_vars['id_col']
        self.vars_4glm     = project_vars['variables_for_glm']
        self.materials_DIR = project_vars["materials_DIR"][1]
        self.vars          = VARS(self.materials_DIR,
                                  project_vars)
        self.param_names   = self.vars.param_names()

        self.run()

    def run(self):
        '''
            reading the info.xlsx file, extracting list of IDs and corresponding
            files with data
        '''
        src_df    = self.tab.get_df(self.vars.lav_f_src()['file_src'])
        self.grid_df = self.tab.change_index(src_df, self.vars.lav_f_src()['index'])
        self.grid_df.index.name = self.vars.lav_f_src()['index']
        self.rm_cols()
        print(self.grid_df)
        self.create_data_file()


    def rm_cols(self):
        """remove cols that are not necessary or created automatically
        """
        feat_2rm = ('Unnamed: 0',)
        for feat in feat_2rm:
            if feat in self.grid_df.columns:
                self.grid_df.drop(columns = [feat], inplace=True)

    def create_data_file(self):
        '''
            save final grid file to use for stats
        '''
        grid_name = self.vars.lav_f_src()['grid_name']
        path_name_f2save   = path.join(self.materials_DIR, f'{grid_name}.csv')
        print('creating file with groups {}'.format(path_name_f2save))
        self.tab.save_df(self.grid_df, path_name_f2save, sheet_name = {grid_name})
