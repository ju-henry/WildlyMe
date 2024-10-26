from optim_functions import global_optim
import json

res = global_optim()

# write best combination
result = f"questions: {res['questions']}"
with open('optim.txt', 'a') as file:
    file.write(result)
        
