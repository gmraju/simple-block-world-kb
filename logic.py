
from copy import deepcopy
from read import *

####
####The KB consists of fact_list and rule_list. These contain fact objects and rule objects respectively.
####
class kb:
	def __init__(self):
		self.facts = []
		self.rules = []

	def __str__(self):
		return 'Number of facts: '+str(len(self.facts))+', Number of rules: '+str(len(self.rules))


class fact:
	"""
	Fact class:
		-statement refers to the statement
		-contains 2 separate list holding facts and rules inferred from this fact respectively
		-default statement for 'asserted' is True
	"""
	def __init__(self, fact, **kvargs):
		if('asserted' in kvargs):
			self. asserted = kvargs['asserted'] 
		else:
			self.asserted = True
		self. supported_by = []
		self.inferences_facts = []
		self.inferences_rules = []
		self.statement = fact

	def __str__(self):
		return str(self.statement)




class rule:
	"""
	Rule class:
		-statement refers to the actual rule tuple
		-contains 2 separate list holding facts and rules inferred from this rule respectively
		-default statement for 'asserted' is True
	"""
	def __init__(self, rule, **kvargs):
		if('asserted' in kvargs):
			self.asserted = kvargs['asserted']
		else:
			self.asserted = True
		self.supported_by = []
		self.inferences_rules = []
		self.inferences_facts = []
		self.statement = rule

	def __str__(self):
		return str(self.statement)





def assert_to_KB(entry, fact_list, rule_list):
	"""
	Function to assert a new rule/fact into the KB.
	Finds inferences from newly asserted rule/fact.
	"""
	if(type(entry) == tuple):
		new_entry = rule(entry, asserted=True)
		rule_list.append(new_entry)
		print 'Rule Asserted: '+str(entry)
	else:
		new_entry = fact(entry, asserted=True)
		fact_list.append(new_entry)
		print 'Fact Asserted: '+str(entry)

	find_inferences(new_entry, fact_list, rule_list)
	print
	return fact_list, rule_list




def find_inferences(new_entry, fact_list, rule_list):
	"""
	Compares the input rule/fact against all other facts/rules to infer new facts and rules.
		-new_entry can be an input fact or rule
	"""
	#Check if new_entry is a rule or fact.
	#If rule, store lhs and rhs separately a
	if(type(new_entry.statement) == tuple):
		check_list = fact_list
		lhs = new_entry.statement[0]
		rhs = new_entry.statement[1]
	else:
		check_list = rule_list
		factt = new_entry.statement

	#Traverse through all elements in check_list, comparing each element to new_entry
	for item in check_list:
		if(type(new_entry.statement) == tuple):
			factt = item.statement

		else:
			lhs = item.statement[0]
			rhs = item.statement[1]			

		#If fact = lhs of rule, create a new fact with statement of rhs
		if(factt == lhs[0] and len(lhs) == 1):
			inferred_fact = fact(rhs)
			print '\tInferred Fact: '+str(inferred_fact.statement)
			#adding inferred fact to to rule and fact
			check_repeats_and_append(inferred_fact, new_entry.inferences_facts)
			check_repeats_and_append(inferred_fact, item.inferences_facts)
			#adding supports for new fact
			inferred_fact.supported_by.append(item)
			inferred_fact.supported_by.append(new_entry)
			#add new fact to fact_list
			check_repeats_and_append(inferred_fact, fact_list)

			#Find inferences that can be made from new fact
			fact_list, rule_list = find_inferences(inferred_fact, fact_list, rule_list)
			break
		#Otherwise 
		else:
			#Find bindings for fact and lhs of rule
			binding = match_logic(factt, lhs[0])
			#If bindings are found, instantiate new rule
			if(binding):
				if(type(new_entry.statement) == tuple):
					temp = deepcopy(list(new_entry.statement))
				else:
					temp = deepcopy(list(item.statement))
		
				temp = instantiate_rule(binding, temp)

				#removing the first element in lhs and creating a new rule containing remaining elements and rhs
				if(len(temp[0]) > 1):
					temp[0] = temp[0][1:] 
				inferred_rule = rule(tuple(temp))
				print '\tInferred Rule: '+str(inferred_rule.statement)
				#adding supported-by to new rule
				inferred_rule.supported_by.append(new_entry)
				inferred_rule.supported_by.append(item)
				#inserting supported/infernces to the rule and fact and rule list
				check_repeats_and_append(inferred_rule, new_entry.inferences_rules)
				check_repeats_and_append(inferred_rule, item.inferences_rules)
				check_repeats_and_append(inferred_rule, rule_list)

				#Find inferences that can be made from new rule
				fact_list, rule_list = find_inferences(inferred_rule, fact_list, rule_list)
	return fact_list, rule_list



def instantiate_fact(binding, temp):
	"""
	Function to instantiate a new fact from input bindings and statement.
	(Replaces the variables in input statement with corresponding constant from bindings)
	"""
	temporary = deepcopy(temp)
	for pos in range(len(temp)):
		if(temporary[pos] in binding.keys()):
			temporary[pos] = binding[temporary[pos]]
	return temporary



def instantiate_rule(binding, temp):
	"""
	Uses bindings list to replace variables with corresponding constants.
	"""
	#replacing variables on lhs
	for ele in range(len(temp[0])):
		for pos in range(len(temp[0][ele])):
			if(temp[0][ele][pos] in binding.keys()):
				temp[0][ele][pos] = binding[temp[0][ele][pos]]
	#Replacing variables in rhs
	for pos in range(len(temp[1])):
		if(temp[1][pos] in binding.keys()):
			temp[1][pos] = binding[temp[1][pos]]
	return temp



def match_logic(statement1, statement2):
	"""
	Checks if two input statements are equivalent.
	If so, returns the binding lists.
	"""
	binding = {}
	if(len(statement1) == len(statement2)):
		#for each ele check if it is a variable- if so add a binding mapping the argument to variable,
		#otherwise fact and lhs of rule don't match.
		for pos in range(len(statement1)):
			var = statement2[pos]
			if(var[0] == '?'):
				binding[var] = statement1[pos]
			elif(var != statement1[pos]):
				binding = {}
				break
	return binding

				

def check_repeats_and_append(entry, some_list):
	"""
	Helper Function-
	Checks if new entry already exists in KB. If not, adds new entry to KB 
	"""
	add_flag = True
	for item in some_list:
		if(entry.statement == item.statement):
			add_flag = False
			break
	if(add_flag):
		some_list.append(entry)



def ask(statement, fact_list):
	"""
	Finds all facts in KB that hold true for input statement and return the list of bindings that hold true.
	"""
	st_bindings = []

	for fact_obj in fact_list:
		fact = fact_obj.statement
		binding = match_logic(fact,statement)

		if(binding):
			st_bindings.append(binding)
		else:
			if(find_object_in_list(statement, fact_list)):
				st_bindings = str(statement)+' is a fact in KB'
				break
	return st_bindings



def ask_plus(statement_list, fact_list):
	#print 'in new'
	sts_bindings = []
	all_in_kb = True
 	bindings = []
 	st = []
	for curr_st in statement_list: 
		bindings = ask(curr_st, fact_list)

		if(isinstance(bindings, str)):
			continue
		elif(not bindings):
			all_in_kb = False
			sts_bindings = []
			break
		else:
			all_in_kb = False
			st = curr_st
			break

	if((not all_in_kb) and bindings): 
		for bind_pos in range(len(bindings)):
			temp = deepcopy(statement_list)
			for pos in range(len(statement_list)):
				temp[pos] = instantiate_fact(bindings[bind_pos], temp[pos])
			if(len(temp)>1):
				temp = temp[1:]
				new_binds = ask_plus(temp, fact_list)
				if(isinstance(new_binds,str)):
					sts_bindings = check_dictionaries_and_extend(sts_bindings, [bindings[bind_pos]])
				elif(new_binds):
					for pos in range(len(new_binds)):
						new_binds[pos].update(bindings[bind_pos])
						sts_bindings = check_dictionaries_and_extend(sts_bindings, new_binds)
			else:
				if(find_object_in_list(temp[0], fact_list)):
					sts_bindings = check_dictionaries_and_extend(sts_bindings, [bindings[bind_pos]])

	if(all_in_kb):
		sts_bindings = 'inkb'
	return sts_bindings


def check_dictionaries_and_extend(binding_list, new_bindings):
	sts_bindings = deepcopy(binding_list)
	for each in new_bindings:
		new_binding = each.items()
		repeat = False
		for bind in binding_list:
			old_binding = bind.items()
			for tup in new_binding:
				if(tup in old_binding):
					old_binding.remove(tup)
			if(not old_binding):
				repeat = True
				break
		if(not repeat):
			sts_bindings.append(each)
	return sts_bindings



def why(statement, fact_list):
	"""
	Why function prints out the support tree for the current fact. ie: it prints out the
	supports for the input argument and the supports for those supports and so on till we reach the asserted root
	statements from which current fact was derived.
	"""
	top_level_stmts = []
	bindings = ask([statement], fact_list)
	if(not bindings):
		st =[]
		is_fact = True
		for var in statement:
			if(var[0] == '?'):
				is_fact = False
				break
		#if statement is a fact check if it is in KB
		if(is_fact):
			st = find_object_in_list(statement, fact_list)
			if(st):
				justification_tree(st,0)
				print
				top_level_stmts.append(st)
			else:
				print 'fact is not in KB'
		#otherwise statement is not in KB
		else:
			print 'statement is not true in KB'
	#if statement is in KB, get bindings and create the facts
	else:
		bindings = bindings[0]
		for binding in bindings:
			copy_statement = deepcopy(statement)
			copy_statement = instantiate_fact(binding, copy_statement)
			st = find_object_in_list(copy_statement, fact_list)
			justification_tree(st,0)
			print
			top_level_stmts.append(st)
	return top_level_stmts

def justification_tree(statement,depth):
	"""
	Helper function for why.
	Recursively calls itself till statement with no supports is reached.
	Also displays all statements traversed.
	"""
	if(not statement.supported_by):
		pretty_print(depth, str(statement.statement)+'--------- asserted')
	else:
		pretty_print(depth, str(statement.statement))
		pretty_print(depth+1, 'Supported By:')
		for each in statement.supported_by:
			justification_tree(each,depth+1) 





def find_object_in_list(statement, some_list):
	"""
	Helper function to find the corresponding rule/fact object given a rule/fact statement
	"""
	st = []
	for item in some_list:
		if(statement == item.statement):
			st = item
			break	
	return st




def retract(ent, fact_list, rule_list):
	"""
	Function to remove a fact/rule from the KB and remove all facts/rules inferred from it.
	"""
	if(type(ent) == tuple):
		check_list = rule_list
	else:
		check_list = fact_list

	st = find_object_in_list(ent, check_list)
	if(st):
		check_list.remove(st)
		print 'Removed: '+str(st.statement)

		fact_list, rule_list = remove_statements(st, fact_list, rule_list, 1)
	print
	return fact_list, rule_list


def remove_statements(statement, fact_list, rule_list, depth):
	"""
	Helper function for 'retract'.
	Recursively traverses the elements of inferences_rules and inferences_facts.  
	"""
	if(statement.inferences_facts or statement.inferences_rules):
		pretty_print(depth, 'Removing Inferences:')
	#Removes a rule from statement.inferred_rules and recursively performs removal on its inferences and so on.
	while(statement.inferences_rules):
		to_remove = statement.inferences_rules.pop()
		#Checks if the rule has already been removed from the KB. If not, removes it.
		if(to_remove in rule_list):
			rule_list.remove(to_remove)
			pretty_print(depth, 'Rule Removed: '+str(to_remove.statement))
		remove_statements(to_remove,fact_list,rule_list, depth+1)

	#Same as above 'while', but for inferred_facts
	while(statement.inferences_facts):
		to_remove = statement.inferences_facts.pop()
		if(to_remove in fact_list):
			fact_list.remove(to_remove)
			pretty_print(depth, 'Fact Removed: '+str(to_remove.statement)) 
		remove_statements(to_remove, fact_list,rule_list, depth+1)

	return fact_list, rule_list



def display_kb(fact_list, rule_list):
	"""
	Function to display contents of KB. 
	"""
	print 'fact:'
	for x in fact_list:
		print x.statement
	print ' '
	print 'rule:'
	for x in rule_list:
		print x.statement
	print ''
	print ''




def pretty_print(depth, print_line):
	"""
	Function for indented printing based on recursion depth
	"""
	for n in range(depth):
		print '\t',
	print print_line










###
#Wrapper Functions
###
def factq(element):
    return type(element[0]) is str

def KB_assert(kb, entry):
	kb.fact_list, kb.rule_list = assert_to_KB(entry, kb.facts, kb.rules)

def KB_ask(kb, query):
	return ask(query, kb.facts)

def instantiate(st, binding):
	return instantiate_fact(binding, st)

def KB_retract(kb, entry):
	kb.facts, kb.rules = retract(entry, kb.facts, kb.rules)

def KB_why(kb, st):
	why(st, kb.facts)

def KB_ask_plus(kb, st_list):
	return ask_plus(st_list, kb.facts)






