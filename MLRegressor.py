from pyspark.ml.regression import LinearRegression, DecisionTreeRegressor, RandomForestRegressor
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator
from ParamHandler import ParamHandler
from Regressor import Regressor


class MLRegressor(Regressor):
    featCols = ['TBH_40', 'TBV_40', 'TBH_45', 'TBV_45', 'TBH_50', 'TBV_50', 'TBH_55', 'TBV_55', 'TBH_60',
                'TBV_60', 'TBH_65', 'TBV_65', 'TBH_70', 'TBV_70', 'LAI_hants', 'Avg_STS_LC', 'Avg_STD_LC']

    def __init__(self, params: ParamHandler, without_temp=False, numRecs=None) -> None:
        self.params = params
        featCols = MLRegressor.featCols
        if without_temp: featCols = featCols[:-2]
        assembler = VectorAssembler(inputCols=featCols, outputCol='features')
        self.df = assembler.transform(params.df_handler.data_df).select('features', 'Avg_SM_LC')
        if numRecs != None:
            self.df = self.df.sample(numRecs/self.df.count())

    def fit(self, type='Linear', split=[0.8, 0.2], should_print=False):
        train, test = self.df.randomSplit(split)
        algo = None
        if type == 'Linear':
            algo = LinearRegression(featuresCol='features', labelCol='Avg_SM_LC')
        elif type == 'Decision Tree':
            algo = DecisionTreeRegressor(featuresCol='features', labelCol='Avg_SM_LC')
        elif type == 'Random Forest':
            algo = RandomForestRegressor(featuresCol='features', labelCol='Avg_SM_LC')
        else:
            raise Exception(f'Invalid model type arg {type} in MLRegressor.fit()')
    
        model = algo.fit(train)
        predictions = model.transform(test)
        evaluator = RegressionEvaluator(labelCol="Avg_SM_LC", predictionCol="prediction", metricName="rmse")
        rmse = evaluator.evaluate(predictions)
        if should_print: print("Root Mean Squared Error (RMSE) on test data = %g" % rmse)
        return rmse