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
        self.vars         = VARS(project_vars)
        f_src             = self.vars.f_src()
        src_file          = f_src['file_src']
        self.col_files    = f_src['col_files']

        self.run()

    def run(self):
        src_file_path    = path.join(project_vars['materials_DIR'][1], src_file)
        self.df           = self.tab.get_df(src_file_path)
        _ids_files = {}
        for ix in self.df.index:
            _ids_files[self.df.at[ix, self._id]] = {
                'file': self.df.at[ix, self.col_files],
                self.group_param : self.df.at[ix, self.group_param]
                }
        print(_ids_files)

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

    def check_subjects(self):
        self.ls_indices_to_drop = list()
        for ix in self.df.index.tolist():
            _id_scan = self.df.at[ix, self._id]
            self.populate_missing_values(_id_scan, ix)
            self.exclude_on_criterion(_id_scan, ix)
            self.exclude_subject(_id_scan, ix)
        log.info('excluding {} subjects based on exclusion ,alternate and values'.format(len(self.ls_indices_to_drop)))
        self.df.drop(self.ls_indices_to_drop, inplace=True)

    def populate_missing_values(self, _id_scan, ix):
        if _id_scan in self.vals_retrieved:
            for col in self.vals_retrieved[_id_scan]:
                value = self.vals_retrieved[_id_scan][col]
                if isinstance(value, str):
                    value = np.nan
                self.df.at[ix, col] = value

    def exclude_on_criterion(self, _id_scan, ix):
        ex_criteria = {'MOCA' : {'dir':'<=', 'type': 'int', 'value': 25},}
                # 'Age'  : {'dir':'>=', 'type': 'float', 'value': 90.0}}
        self.excluded_on_criterion = {}
        for criterion in ex_criteria:
            type_crit = ex_criteria[criterion]['type']
            dir = ex_criteria[criterion]['dir']
            value = self.df.at[ix, criterion]
            if type_crit == 'float' and not np.isnan(value):
                if float(value) <= float(ex_criteria[criterion]['value']):
                    print('    excluding {}, {}, {}'.format(_id_scan, criterion, value))
                    self.excluded_on_criterion[_id_scan] = {criterion:value}
            elif type_crit == 'int' and not np.isnan(value):
                if int(value) <= int(ex_criteria[criterion]['value']):
                    print('    excluding {}, {}, {}'.format(_id_scan, criterion, value))
                    self.excluded_on_criterion[_id_scan] = {criterion:value}
            elif np.isnan(value) and self.exclude_nan:
                    print('    excluding {}, {}, {}'.format(_id_scan, criterion, value))
                    self.excluded_on_criterion[_id_scan] = {criterion:value}

    def exclude_subject(self, _id_scan, ix):
        if _id_scan in self.vars.doublons_excluded() \
            or _id_scan in self.vars.doublons_with_alternates() \
            or _id_scan in self.vars.doublons_alternate_on_age() \
            or _id_scan in self.excluded_on_criterion:
            self.ls_indices_to_drop.append(ix)

    def exclude_columns(self):
        cols_to_exclude = ['Code_Study', 'Code Labo', 'Code_Participant','SCANNER','NB de cannaux','Année_SCAN','séance longitudinal', 'Doublon']
        self.df.drop(columns = cols_to_exclude, inplace=True)

    def create_groups(self):
        groups      = self.vars.groups()
        thresh      = self.vars.group_thresh()
        group_col   = self.project_vars["group_col"]
        group_param = self.project_vars["group_param"]

        conditions = list()
        values     = list()
        for group in groups:
            if groups[group] == '>=':
                values.append(group)
                conditions.append((self.df[group_param] >= thresh))
            if groups[group] == '<':
                values.append(group)
                conditions.append((self.df[group_param] < thresh))
        self.df[group_col] = np.select(conditions, values)

    def create_data_file(self):
        data_file = path.join(self.project_vars["materials_DIR"], self.project_vars["GLM_file_group"])
        log.info('creating file with groups {}'.format(data_file))
        self.df.set_index(self._id, inplace = True)
        self.df.to_excel(data_file)

    def get_missing_data(self):
        self.f_missing_values = get_path(path.dirname(__file__), self.vars.f_missing_values)
        if not path.exists(self.f_missing_values):
            from .step0_prep2_chk_data import GetMissingData
            ready = GetMissingData(self.project_vars, self.df).ready
        else:
            ready = True
        if ready:
            self.vals_retrieved = load_json(self.f_missing_values)
        return ready
