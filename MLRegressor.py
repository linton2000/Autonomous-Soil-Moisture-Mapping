from pyspark.ml.regression import LinearRegression, DecisionTreeRegressor, RandomForestRegressor
from pyspark.ml.feature import VectorAssembler
from ParamHandler import ParamHandler
from Regressor import Regressor


class MLRegressor(Regressor):
    featCols = ['TBH_40', 'TBV_40', 'TBH_45', 'TBV_45', 'TBH_50', 'TBV_50', 'TBH_55', 'TBV_55', 'TBH_60',
                'TBV_60', 'TBH_65', 'TBV_65', 'TBH_70', 'TBV_70', 'Avg_STS_LC', 'Avg_STD_LC', 'LAI_hants']

    def __init__(self, params: ParamHandler) -> None:
        self.params = params
        assembler = VectorAssembler(inputCols=MLRegressor.featCols, outputCol='features')
        self.df = assembler.transform(params.df_handler.data_df).select('features', 'Avg_SM_LC')

    def fit(self, type='Linear', split=[0.8, 0.2], print_summary=False, ):
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
        summary = model.evaluate(test)
        if print_summary: MLRegressor._print_summary(summary, type)
        return summary
    
    def _print_summary(summary, type):
        print(f'Summary for {type} regression')
        print("   numInstances: %d" % summary.numInstances)
        print("   degreesOfFreedom: %d" % summary.degreesOfFreedom)
        print("   explainedVariance: %f" % summary.explainedVariance)
        print("   meanAbsoluteError: %f" % summary.meanAbsoluteError)
        print("   meanSquaredError: %f" % summary.meanSquaredError)
        print("   rootMeanSquaredError: %f" % summary.rootMeanSquaredError)
        print("   r2: %f" % summary.r2)
        print("   r2adj: %f" % summary.r2adj)