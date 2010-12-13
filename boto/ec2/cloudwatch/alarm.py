# Copyright (c) 2010 Reza Lotun http://reza.lotun.name
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
import json


class MetricAlarm(object):
    _cmp_map = {
                    '>='    :   'GreaterThanOrEqualToThreshold',
                    '>'     :   'GreaterThanThreshold',
                    '<'     :   'LessThanThreshold',
                    '<='    :   'LessThanOrEqualToThreshold',
               }
    _rev_cmp_map = dict((v, k) for (k, v) in _cmp_map.iteritems())

    def __init__(self, connection=None, name=None, metric=None,
                 namespace=None, statistic=None, comparison=None, threshold=None,
                 period=None, evaluation_periods=None):
        """
        Creates a new Alarm.

        :type name: str
        :param name: Name of alarm.

        :type metric: str
        :param metric: Name of alarm's associated metric.

        :type namespace: str
        :param namespace: The namespace for the alarm's metric.

        :type statistic: str
        :param statistic: The statistic to apply to the alarm's associated metric. Can
                          be one of 'SampleCount', 'Average', 'Sum', 'Minimum', 'Maximum'

        :type comparison: str
        :param comparison: Comparison used to compare statistic with threshold. Can be
                           one of '>=', '>', '<', '<='

        :type threshold: float
        :param threshold: The value against which the specified statistic is compared.

        :type period: int
        :param period: The period in seconds over which teh specified statistic is applied.

        :type evaluation_periods: int
        :param evaluation_period: The number of periods over which data is compared to
                                  the specified threshold
        """
        self.name = name
        self.connection = connection
        self.metric = metric
        self.namespace = namespace
        self.statistic = statistic
        self.threshold = float(threshold)
        self.comparison = self._cmp_map[comparison]
        self.period = int(period)
        self.evaluation_periods = int(evaluation_periods)
        self.actions_enabled = None
        self.alarm_actions = []
        self.alarm_arn = None
        self.last_updated = None
        self.description = ''
        self.dimensions = []
        self.insufficient_data_actions = []
        self.ok_actions = []
        self.state_reason = None
        self.state_value = None
        self.unit = None

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'ActionsEnabled':
            self.actions_enabled = value
        elif name == 'AlarmArn':
            self.alarm_arn = value
        elif name == 'AlarmConfigurationUpdatedTimestamp':
            self.last_updated = value
        elif name == 'AlarmDescription':
            self.description = value
        elif name == 'AlarmName':
            self.name = value
        elif name == 'ComparisonOperator':
            setattr(self, 'comparison', self._rev_cmp_map[value])
        elif name == 'EvaluationPeriods':
            self.evaluation_periods = int(value)
        elif name == 'MetricName':
            self.metric = value
        elif name == 'NameSpace':
            self.namespace = value
        elif name == 'Period':
            self.period = int(value)
        elif name == 'StateReason':
            self.state_reason = value
        elif name == 'StateValue':
            self.state_value = None
        elif name == 'Statistic':
            self.statistic = value
        elif name == 'Threshold':
            self.threshold = float(value)
        elif name == 'Unit':
            self.unit = value
        else:
            setattr(self, name, value)


class AlarmHistoryItem(object):
    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'AlarmName':
            self.name = value
        elif name == 'HistoryData':
            self.data = json.loads(value)
        elif name == 'HistoryItemType':
            self.tem_type = value
        elif name == 'HistorySummary':
            self.summary = value
        elif name == 'Timestamp':
            self.timestamp = value

