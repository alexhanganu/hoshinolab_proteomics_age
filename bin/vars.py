#!/bin/python


class VARS():
    def __init__(self, project_vars):
        self.project_vars       = project_vars


    def f_src(self):
        f_src_subs  = "info.xlsx"
        col_files = 'File name'
        return {'file_src': f_src_subs,
                'col_files': col_files}
