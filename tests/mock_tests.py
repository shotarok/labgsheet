"""A test suite that doesn't query the Google API.

Avoiding direct network access is benefitial in that it markedly speeds up
testing, avoids error-prone credential setup, and enables validation even if
internet access is unavailable.

"""

from unittest.mock import Mock
from unittest.mock import call
import unittest

from labgsheet import Experiment


class MockExperimentTest(unittest.TestCase):

    def setUp(self):
        self.ws_mock = Mock()

    def test_init(self):
        self.ws_mock.col_values = Mock(return_value=['experiment_id'])
        exp = Experiment(self.ws_mock)
        got = self.ws_mock.method_calls
        expected = [
            call.update_cell(1, 1, 'experiment_id'),
            call.col_values(1),
            call.update_cell(2, 1, exp.experiment_id)
        ]
        self.assertEqual(got, expected)
        self.assertEqual(exp.row, 2)

    def test_init_with_experiment_id(self):
        experiment_ids = ['experiment_id', 'exp1', 'exp2', 'exp3']
        self.ws_mock.col_values = Mock(return_value=experiment_ids)
        exp = Experiment(self.ws_mock, experiment_id='exp2')
        got = self.ws_mock.method_calls
        expected = [
            call.update_cell(1, 1, 'experiment_id'),
            call.col_values(1)
        ]
        self.assertEqual(got, expected)
        self.assertEqual(exp.row, 3)

    def test_logging_new_params_and_metrics(self):
        self.ws_mock.col_values = Mock(return_value=['experiment_id'])
        headers = [
            'experiment_id', 'param1', 'metric1', 'param2',
            'param3', 'metric2', 'metric3'
        ]
        self.ws_mock.row_values = Mock(side_effect=[
            headers[0:i] for i in range(1, len(headers))
        ])
        exp = Experiment(self.ws_mock)
        exp.log_parameter('param1', 1)
        exp.log_metric('metric1', 10)
        exp.log_multi_params({'param2': 2, 'param3': 3})
        exp.log_multi_metrics({'metric2': 20, 'metric3': 30})

        got = self.ws_mock.method_calls
        expected = [
            call.update_cell(Experiment.HEADER_ROW, 2, 'param1'),
            call.update_cell(exp.row, 2, 1),
            call.update_cell(Experiment.HEADER_ROW, 3, 'metric1'),
            call.update_cell(exp.row, 3, 10),
            call.update_cell(Experiment.HEADER_ROW, 4, 'param2'),
            call.update_cell(exp.row, 4, 2),
            call.update_cell(Experiment.HEADER_ROW, 5, 'param3'),
            call.update_cell(exp.row, 5, 3),
            call.update_cell(Experiment.HEADER_ROW, 6, 'metric2'),
            call.update_cell(exp.row, 6, 20),
            call.update_cell(Experiment.HEADER_ROW, 7, 'metric3'),
            call.update_cell(exp.row, 7, 30),
        ]
        self.assertTrue(all([c in got for c in expected]))

    def test_logging_existed_params_and_metrics(self):
        self.ws_mock.col_values = Mock(return_value=['experiment_id'])
        headers = [
            'experiment_id', 'metric1', 'metric2', 'metric3',
            'param1', 'param2', 'param3'
        ]
        self.ws_mock.row_values = Mock(return_value=headers)
        exp = Experiment(self.ws_mock)
        exp.log_parameter('param1', 1)
        exp.log_metric('metric1', 10)
        exp.log_multi_params({'param2': 2, 'param3': 3})
        exp.log_multi_metrics({'metric2': 20, 'metric3': 30})

        got = self.ws_mock.method_calls
        expected = [
            call.update_cell(exp.row, headers.index('param1') + 1, 1),
            call.update_cell(exp.row, headers.index('metric1') + 1, 10),
            call.update_cell(exp.row, headers.index('param2') + 1, 2),
            call.update_cell(exp.row, headers.index('param3') + 1, 3),
            call.update_cell(exp.row, headers.index('metric2') + 1, 20),
            call.update_cell(exp.row, headers.index('metric3') + 1, 30),
        ]
        self.assertTrue(all([c in got for c in expected]))
