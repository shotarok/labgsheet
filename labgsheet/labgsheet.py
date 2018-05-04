# -*- coding: utf-8 -*-

import uuid


class Experiment(object):
    HEADER_ROW = 1
    EXP_ID_COL = 1

    def __init__(self, ws, experiment_id=None):
        self._ws = ws
        self._prepare_experiment_header()
        self.experiment_id = experiment_id or self._uuid()
        self.row = self._find_or_create_row(self.experiment_id)

    def _uuid(self):
        return uuid.uuid4().hex

    def _prepare_experiment_header(self):
        # make sure that 'experiment_id' header exists
        self._ws.update_cell(self.HEADER_ROW, self.EXP_ID_COL, 'experiment_id')

    def log_parameter(self, name, val):
        self._update_by_name(name, val)

    def log_multi_params(self, param_dict):
        for name, val in param_dict.items():
            self._update_by_name(name, val)

    def log_metric(self, name, val):
        self._update_by_name(name, val)

    def log_multi_metrics(self, metric_dict):
        for name, val in metric_dict.items():
            self._update_by_name(name, val)

    def _update_by_name(self, name, val):
        col = self._find_or_create_header(name)
        self._ws.update_cell(self.row, col, val)

    def _find_or_create_row(self, experiment_id):
        experiment_ids = self._get_experiment_ids()
        if experiment_id in experiment_ids:
            return experiment_ids.index(experiment_id) + 1

        # Add a new experiment row when experiment_id does not exist
        new_exp_row = len(experiment_ids) + 1
        self._ws.update_cell(
            new_exp_row, self.EXP_ID_COL, self.experiment_id
        )
        return new_exp_row

    def _get_headers(self):
        return self._ws.row_values(self.HEADER_ROW)

    def _get_experiment_ids(self):
        return self._ws.col_values(self.EXP_ID_COL)

    def _find_or_create_header(self, name):
        headers = self._get_headers()
        if name in headers:
            return headers.index(name) + 1

        # Add a new header cell when name is not in headers
        new_h_col = len(headers) + 1
        self._ws.update_cell(self.HEADER_ROW, new_h_col, name)
        return new_h_col
