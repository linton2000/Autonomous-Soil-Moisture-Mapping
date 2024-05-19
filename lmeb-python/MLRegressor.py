import copy
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.regression import LinearRegression, DecisionTreeRegressor, RandomForestRegressor, GBTRegressor
from pyspark.ml.feature import VectorAssembler, Normalizer
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql import DataFrame
from Regressor import Regressor

class MLRegressor(Regressor):

    def __init__(self, featCols) -> None:
        assembler = VectorAssembler(inputCols=featCols, outputCol='feat_vec')
        normalizer = Normalizer(
            inputCol=assembler.getOutputCol(), outputCol='features')
        self.pipe = Pipeline(stages=[assembler, normalizer])

    def fit(self, df: DataFrame, metric=None, split=[0.8, 0.2], type='basic'):
        df = df.withColumnRenamed('Avg_SM_LC', 'label')
        self.train, self.test = df.randomSplit(split, 42)
        if type == 'basic':
            return MLRegressor._basic_fit(self)
        elif type == 'feat':
            return MLRegressor._feat_fit(self, metric)
        elif type == 'dt':
            return MLRegressor._dt_fit(self)
        else:
            raise Exception(f'Invalid fit type {type} in MLRegressor.fit()')
    
    def _dt_fit(self):
        pipeline = Pipeline(stages=[self.pipe, DecisionTreeRegressor()])
        pipe_mdl = pipeline.fit(self.train)
        return pipe_mdl.stages[-1].featureImportances.toArray(), pipe_mdl.stages[0].stages[0].getInputCols()

    def _feat_fit(self, metric):
        pipeline = Pipeline(stages=[self.pipe, GBTRegressor()])
        pipe_mdl = pipeline.fit(self.train)
        predictions = pipe_mdl.transform(self.test)
        return RegressionEvaluator(metricName=metric).evaluate(predictions)
    
    def _basic_fit(self, metrics={'rmse': 0, 'mae': 0, 'r2': 0}, verbose=False):
        eval_dict = {'Linear Regression': LinearRegression(),
                     'Decision Tree': DecisionTreeRegressor(),
                     'Random Forest': RandomForestRegressor(),
                     'Gradient Boosted Tree': GBTRegressor()}

        for key, model in eval_dict.items():
            pipeline = Pipeline(stages=[self.pipe, model])
            pipe_mdl = pipeline.fit(self.train)
            predictions = pipe_mdl.transform(self.test)
            for metric, _ in metrics.items():
                eval = RegressionEvaluator(
                    metricName=metric).evaluate(predictions)
                metrics[metric] = round(eval, 4)
                if verbose: 
                    print(key, metric, eval)
            eval_dict[key] = copy.deepcopy(metrics)

        return eval_dict
