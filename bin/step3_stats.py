#!/bin/python
# -*- coding: utf-8 -*-
#Alexandru Hanganu, 20200311

''' Do stats
Args:


Return:


'''

from os import path 
from .vars import VARS


class Stats:
    def __init__(self, project_vars, utils, Table, Preprocess):
        self.tab           = Table()
        self.project_vars  = project_vars
        self._id           = project_vars['id_col']
        self.vars_4glm     = project_vars['variables_for_glm']
        self.materials_DIR = project_vars["materials_DIR"][1]
        self.vars          = VARS(self.materials_DIR, project_vars)
        self.param_names   = self.vars.param_names()

        self.run()

    def run(self):
        '''
            reading the  files with data
        '''
        grid_src_df           = self.tab.get_df(self.vars.f_src()['grid_file'])
        grid_lav_df       = self.tab.get_df(self.vars.lav_f_src()['grid_file'])

        _ids_src = grid_src_df[self.vars.f_src()['index']]
        _ids_lav_src = grid_lav_df[self.vars.lav_f_src()['index']]
        print([i for i in _ids_src if i in _ids_lav_src])
        # compare if proteins are similar in both df: sample name and protein id


