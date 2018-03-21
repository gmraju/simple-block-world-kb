import read, logic


print "\033[0;32m\n=================== Loading in the data ===================\x1b[0m"	

facts, rules = read.read_tokenize("asserts.txt")

retracts, retract_rules = read.read_tokenize("retracts.txt")

asks, ask_rules = read.read_tokenize("asks.txt")
	
print "\033[0;32m\n=================== Setting up the Knowledge Base ===================\x1b[0m"	

kb = logic.kb()

print 
print kb
	
print "\033[0;32m\n=================== Testing KB_Assert ===================\x1b[0m"	

for rule in rules:
	logic.KB_assert(kb, rule)
	
for fact in facts:
	logic.KB_assert(kb, fact)
	
for fact in kb.facts:
	print fact

print "\n=================== Testing KB_ask ==================="	


for ask in asks:
	print "\nAsking : " + str(ask)
	matches = logic.KB_ask(kb, ask)
	if len(matches) == 0:
		print "No matches in KB"
	else:
		for match in  logic.KB_ask(kb, ask):
			print match,
		print

print "\n=================== Testing KB_ask and instantiate ==================="	


for ask in asks:
	print "\nAsking : " + str(ask)
	matches = logic.KB_ask(kb, ask)
	if len(matches) == 0:
		print "No matches in KB"
	else:
		print "Found:",
		for match in logic.KB_ask(kb, ask):
			print logic.instantiate(ask, match),
		print

print "\n=================== Testing retract ==================="	

print
print kb

logic.KB_retract(kb, ["color", "bigbox", "red"])

logic.KB_retract(kb, ["size", "bigbox", "big"])

print kb

print "\n=================== Asserting what we just retracted ==================="	

logic.KB_assert(kb, ["color", "bigbox", "red"])

logic.KB_assert(kb, ["size", "bigbox", "big"])

print "\n=================== Testing against Why ==================="	


for fact in kb.facts:
	logic.KB_why(kb,fact.statement)
	
print "\n=================== Testing against Ask PLus ==================="	

statement_list1 = [["color", "?y", "red"],["color", "?x", "green"]]
statement_list2 = [["color", "?y", "?x"],["inst", "?y", "box"],["size", "?y", "?z"]]

print "\nAsking about: " + str(statement_list1)

list_of_bindings = logic.KB_ask_plus(kb, statement_list1)

print "Found " + str(len(list_of_bindings)) + " sets of bindings"

for bind in list_of_bindings:
	print "\n\tBinding: " + str(bind)
	print "\tFacts:",
	for statement in statement_list1:
		print logic.instantiate(statement, bind),
	print

print "\nAsking about: " + str(statement_list2)

list_of_bindings = logic.KB_ask_plus(kb, statement_list2)

print "Found " + str(len(list_of_bindings)) + " sets of bindings"

for bind in list_of_bindings:
	print "\n\tBinding: " + str(bind)
	print "\tFacts:",
	for statement in statement_list2:
		print logic.instantiate(statement, bind),
	print