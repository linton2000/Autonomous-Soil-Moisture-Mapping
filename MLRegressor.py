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

    def fit(self, df: DataFrame, split=[0.8, 0.2], metrics={'rmse': 0, 'mae': 0, 'r2': 0}, verbose=False):
        df = df.withColumnRenamed('Avg_SM_LC', 'label')
        train, test = df.randomSplit(split, 42)
        eval_dict = {'Linear Regression': LinearRegression(),
                     'Decision Tree': DecisionTreeRegressor(),
                     'Random Forest': RandomForestRegressor(),
                     'Gradient Boosted Tree': GBTRegressor()}

        for key, model in eval_dict.items():
            pipeline = Pipeline(stages=[self.pipe, model])
            pipe_mdl = pipeline.fit(train)
            predictions = pipe_mdl.transform(test)
            for metric, _ in metrics.items():
                eval = RegressionEvaluator(
                    metricName=metric).evaluate(predictions)
                metrics[metric] = round(eval, 4)
                if verbose: 
                    print(key, metric, eval)
            eval_dict[key] = copy.deepcopy(metrics)

        return eval_dict
