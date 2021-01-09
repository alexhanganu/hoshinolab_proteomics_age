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
                # f_src_60    = "Ayuko_Lyden_autism_project_all_60_samples_PD.xlsx"
        # f_src_dJon  = "MS151970QE_Bruno_Lyden_control_dad_Jon.xlsx"
        # f_src_d_ct  = "MS151649QE_Bruno_Lyden_control2_dad.xlsx"
        # f_src_m_hz  = "MS151970QE_Bruno_Lyden_control_mom_HZ.xlsx"
        # f_src_m_ct1 = "MS151649QE_Bruno_Lyden_control1_mom.xlsx"
        # f_src_p_ea  = "MS151970QE_Bruno_Lyden_PNC_EA.xlsx"
        # f_src_p_dg  = "MS151818QE_Bruno_Lyden_PNC_DG.xlsx"
        # f_src_p_fs  = "MS151818QE_Bruno_Lyden_PNC_FS.xlsx"
        # f_src_p_ss  = "MS151818QE_Bruno_Lyden_PNC_SS.xlsx"
        # f_src_p_jm  = "MS151970QE_Bruno_Lyden_PNC_JM.xlsx"
        # f_src_p_eg  = "MS151970QE_Bruno_Lyden_PNC_EG.xlsx"
        # f_src_autsm = "MS162577_Ayuko_Lyden_autism_all_data_PD.xlsx"
        # ready_miss   = self.get_missing_data()
        # self.project_vars["materials_DIR"] = 'C:/Users/Jessica/Desktop' #tmp, to be removed
        # if ready_miss:
        #     log.info('missing data populated, doublons defined')
        #     self.check_subjects()
        #     self.exclude_columns()
        #     self.create_groups()
        #     self.create_data_file()
        # else:
        #     log.info(f'ERR in steps of missing data of defining doublons, doublons')

        # self.populate_missing_data()
        # self.df.set_index(self._id, inplace = True)
        # self.create_data_file()


    def populate_missing_data(self):
        """Some values are missing. If number of missing values is lower then 5%,
            missing values are changed to group mean
            else: columns is excluded
        """
        _, cols_with_nans = self.tab.check_nan(self.grid_df, self.miss_val_file)
        df_groups = dict()
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
