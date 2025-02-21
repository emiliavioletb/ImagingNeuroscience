
from common.functions import *
from common.stats_test import *
from statsmodels.stats.diagnostic import linear_reset

allData_reg = pd.read_csv('/Users/emilia/Documents/Conferences/fNIRS 2024/regression_data.csv')
allData_reg = allData_reg.dropna(subset=['globEfficiency', 'Age', 'mmse_total'])

predictors = allData_reg[['avgClustering', 'globEfficiency', 'Age']]
predicted = allData_reg[['mmse_total']]

X = sm.add_constant(predictors)
model = sm.OLS(predicted, X).fit()
print(model.summary())

####### TESTING MODEL ASSUMPTIONS ######
# Linearity
reset_test = linear_reset(model, power=2, test_type='fitted')
print(f'Ramsey RESET Test p-value: {reset_test.pvalue}')
fitted_values = model.fittedvalues
residuals = model.resid

# Homoscedasticity - p val should be above 0.05
test_stat, p_value, _, _ = sms.het_breuschpagan(residuals, model.model.exog)
print(f'Breusch-Pagan p-value: {p_value}')

# Test normality of residuals - p val should be above 0.05
shapiro_test = stats.shapiro(residuals)
print('Shapiro-Wilk test:', shapiro_test)

# Test for colinearity - should be below 10
vif = pd.DataFrame()
vif["Variable"] = X.columns
vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif)

# Independence of errors - should be close to 2
dw_test = durbin_watson(residuals)
print('Durbin-Watson test:', dw_test)

# Significant outliers
plot_leverage_resid2(model)
plt.show()

# Plotting linear regression
sns.lmplot(x='gT', y='MMSE', data=allData_reg, ci=None)
plt.title('Linear Regression')
plt.show()