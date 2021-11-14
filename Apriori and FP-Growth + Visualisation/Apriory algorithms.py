from apriori_python import apriori
from efficient_apriori import apriori as efficient_apriori
from fpgrowth_py import fpgrowth
import pprint
import time
from PyARMViz import PyARMViz


pp = pprint.PrettyPrinter(indent=4, compact=False)
transactions = []
with open('pharmacy_busket.csv', 'r') as dataset:
    lines = dataset.readlines()
    for line in lines:
        line = line.strip('\n')
        transactions.append(line.split(','))
freqItemSet, rules = apriori(transactions, minSup=0.2, minConf=0.6)
for item in rules:
    pp.pprint(item)

print("------------------\n----Efficient-----\n------------------")
freqItemSet, rules = efficient_apriori(transactions, min_support=0.2, min_confidence=0.6)
for item in rules:
    pp.pprint(item)

# PyARMViz.generate_parallel_category_plot(rules)
# PyARMViz.generate_parallel_coordinate_plot(rules)
# PyARMViz.generate_rule_graph_plotly(rules)
# PyARMViz.generate_rule_start_end_plot(rules)

print("------------------\n----FPGrowth-----\n------------------")
freqItemSet, rules = fpgrowth(transactions, minSupRatio=0.2, minConf=0.6)
for item in rules:
    pp.pprint(item)



print("\nТестируем время работы алгоритмов")
transactions = transactions*10000
#  ---
start_time = time.time()
apriori(transactions, minSup=0.2, minConf=0.6)
print("Apriori: --- %s seconds ---" % (time.time() - start_time))
#  ---
start_time = time.time()
efficient_apriori(transactions, min_support=0.2, min_confidence=0.6)
print("Efficient apriori: --- %s seconds ---" % (time.time() - start_time))
#  ---
start_time = time.time()
fpgrowth(transactions, minSupRatio=0.2, minConf=0.6)
print("FPGrowth: --- %s seconds ---" % (time.time() - start_time))
