from apyori import apriori, TransactionManager
import pandas as pd 


class Apriori():
    
    def __init__(self, df, group_column, item_column, min_confidence=0.5, min_lift=1.1, min_support=0.1):
        self.df = df
        self.group_column = group_column
        self.item_column = item_column
        self.min_confidence = min_confidence
        self.min_lift = min_lift
        self.min_support = min_support
        
        self.transactions = list(self.df.groupby(self.group_column)[self.item_column].apply(lambda values: [value for value in values]).values)
        self.all_rules = list(apriori(self.transactions, 
                                        min_confidence=self.min_confidence, 
                                        min_lift=self.min_lift, 
                                        min_support=self.min_support))

    def rules(self, numero_max_antecedente=10, numero_max_consequente=10, eliminar_antecedente=None,
              eliminar_consequente=None, incluir_antecedente=None, incluir_consequente=None, show_freq=False):
        items_base = [tuple(rule.items_base) for rules in self.all_rules for rule in rules.ordered_statistics ]
        items_add = [tuple(rule.items_add) for rules in self.all_rules for rule in rules.ordered_statistics ]
        confidences = [rule.confidence for rules in self.all_rules for rule in rules.ordered_statistics]
        lifts = [rule.lift for rules in self.all_rules for rule in rules.ordered_statistics]
        results = pd.DataFrame({'Se': items_base, 'Então': items_add, 'Confiança': confidences, 'Lift': lifts})
        filtro = (results['Se'].map(lambda value: len(value)) <= numero_max_antecedente) & \
            (results['Então'].map(lambda value: len(value)) <= numero_max_consequente) 
        results = results.loc[filtro]
        if eliminar_antecedente:
            for item in eliminar_antecedente:
                results = results.loc[~results.Se.astype('str').str.contains(item, regex=False)]
        if eliminar_consequente:
            for item in eliminar_consequente:
                results = results.loc[~results['Então'].astype('str').str.contains(item, regex=False)]
        if incluir_antecedente:
            for item in incluir_antecedente:
                results = results.loc[results.Se.astype('str').str.contains(item, regex=False)]
        if incluir_consequente:
            for item in incluir_consequente:
                results = results.loc[results['Então'].astype('str').str.contains(item, regex=False)]
        if show_freq:
            def func(row, itemlist):
                return row.loc[row[self.item_column].isin(itemlist), self.item_column].count()
            def freq_se(row, df):
                return df.groupby(self.group_column).apply(lambda row1: func(row1, row['Se'].values[0])).sum()
            def freq_entao(row, df):
                return df.groupby(self.group_column).apply(lambda row1: func(row1, row['Então'].values[0])).sum()
            
            freq_se = results.groupby('Se').apply(lambda row: freq_se(row, self.df)).reset_index(name='Freq_Se')
            freq_entao = results.groupby('Então').apply(lambda row: freq_entao(row, self.df)).reset_index(name='Freq_Então')
            results = pd.merge(results, freq_se, left_on='Se', right_on='Se')
            results = pd.merge(results, freq_entao, left_on='Então', right_on='Então')
            
        return results
    

        
    
    
        

        
if __name__ == '__main__':
    df = pd.read_csv('Distribuidora.csv')
    model = Apriori(df, 'NOTA', 'NOME_PROD')
    rules = model.rules(show_freq=True)
    
    print(rules)
    
    # def func(row, itemlist):
    #     return row.loc[row['NOME_PROD'].isin(itemlist), 'NOME_PROD'].count()
    
    # def freq(row, df):
    #     # print(row['Se'].values[0])
    #     return df.groupby('NOTA').apply(lambda row1: func(row1, row['Se'].values[0])).sum()
    
    # # rules.groupby('Se').apply(lambda row: freq(row))
    
    # # itemset = rules['Se'].iloc[0]
    # print(rules.groupby('Se').apply(lambda row: freq(row, df)))