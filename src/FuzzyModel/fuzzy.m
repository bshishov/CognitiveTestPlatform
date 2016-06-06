fistemperament = readfis('temperament');
fismemory = readfis('memory');
fismemory_stress = readfis('memory_stress');
fismemory_overall = readfis('memory_overall');
fisoperation = readfis('operation');
fisplasticity = readfis('plasticity');

results = readtable('../valid_results_predicted.csv');


neurotism = results{:, {'TemperamentNeurotismScore'}};
extraversy = results{:, {'TemperamentExtravertScore'}};
memoryAverageResponseTime = results{:, {'MemoryAverageResponseTime'}} / 1000;
memoryRemembered = results{:, {'MemoryRemembered'}};
memoryStressAverageResponseTime = results{:, {'MemoryStressAverageResponseTime'}} / 1000;
memoryStressCorrectCount = results{:, {'MemoryStressCorrectCount'}};
operationAverageResponseTime = results{:, {'OperationAverageResponseTime'}} / 1000;
operationFails = results{:, {'OperationFails'}};
plasticityTime = results{:, {'PlasticityTime'}} / 1000;
plasticityFails = results{:, {'PlasticityFails'}};

results.Temperament = evalfis([neurotism extraversy], fistemperament);
memory = evalfis([memoryAverageResponseTime memoryRemembered], fismemory);
memory_stress = evalfis([memoryStressAverageResponseTime memoryStressCorrectCount], fismemory_stress);
results.Memory = evalfis([memory memory_stress], fismemory_overall); 
results.Operation = evalfis([operationAverageResponseTime operationFails], fisoperation); 
results.Plasticity = evalfis([plasticityTime plasticityFails], fisplasticity);     

writetable(results, 'fuzzy_results.csv')

figure
gensurf(fistemperament);
print('figures/Temperament.png','-dpng')

figure
gensurf(fismemory);
print('figures/MemoryBasic.png','-dpng')

figure
gensurf(fismemory_stress);
print('figures/MemoryStress.png','-dpng')

figure
gensurf(fismemory_overall);
print('figures/Memory.png','-dpng')

figure
view(-220, 30)
gensurf(fisoperation);
print('figures/Operation.png','-dpng')


figure
gensurf(fisplasticity);
view(-125, 30)
print('figures/Plasticity.png','-dpng')