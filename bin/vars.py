#!/bin/python


class VARS():
    def __init__(self, project_vars):
        self.project_vars       = project_vars


    def f_src(self):
        f_src_subs  = "info.xlsx"
        col_files = 'File name'
        return {'file_src': f_src_subs,
                'col_files': col_files}

    def get_ids_and_data_files(self, df, _id):
        _ids_files = {}
        for ix in df.index:
            _ids_files[df.at[ix, _id]] = {
                'file': df.at[ix, self.f_src()['col_files']],
                }
        return _ids_files
