from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.regression import LinearRegression, DecisionTreeRegressor, RandomForestRegressor, GBTRegressor
from pyspark.ml.feature import VectorAssembler, Normalizer
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql import DataFrame
from ParamHandler import ParamHandler
from Regressor import Regressor


class MLRegressor(Regressor):
    featCols = ['TBH_40', 'TBV_40', 'TBH_45', 'TBV_45', 'TBH_50', 'TBV_50', 'TBH_55', 'TBV_55', 'TBH_60',
                'TBV_60', 'TBH_65', 'TBV_65', 'TBH_70', 'TBV_70', 'LAI_hants', 'Avg_STS_LC', 'Avg_STD_LC']

    def __init__(self, featCols=None, numRecs=None) -> None:
        if featCols == None:
            featCols = MLRegressor.featCols
        assembler = VectorAssembler(inputCols=featCols, outputCol='feat_vec')
        normalizer = Normalizer(
            inputCol=assembler.getOutputCol(), outputCol='features')
        self.pipe = Pipeline(stages=[assembler, normalizer])

    def fit(self, df: DataFrame, trainRecs=1000, metrics={'rmse': 0, 'mae': 0, 'r2': 0}):
        df = df.withColumnRenamed('Avg_SM_LC', 'label')
        train, test = df.randomSplit()
        eval_dict = {'Linear Regression': LinearRegression(),
                     'Decision Tree': DecisionTreeRegressor(),
                     'Random Forest': RandomForestRegressor(),
                     'Gradient Boosted Tree': GBTRegressor()}

        for key, (_, model) in eval_dict.items():
            pipeline = Pipeline(stages=[self.pipe, model])
            pipe_mdl = pipeline.fit(train)
            predictions = pipe_mdl.transform(test)
            for metric, _ in metrics.items():
                eval = RegressionEvaluator(
                    metricName=metric).evaluate(predictions)
                metrics[metric] = eval
            eval_dict[key] = metrics

        return eval_dict