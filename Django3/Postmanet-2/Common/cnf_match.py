import ryw,logging
import datetime # needed for eval-ing upload_datetime, which is a string! Randy is so stupid!

## Converts string or list of strings to lowercase
def to_lower(v):
	if isinstance(v, list):
		r = []
		for value in v:
			r.append(value.lower())
		return r
	else:
		return v.lower()

## Compares v with r. If r is a list, v is compared with each element of r
## 'nocase' option recognized
def test_equals(r, v, options):

	if 'nocase' in options:
		r = to_lower(r)
		v = to_lower(v)

	if isinstance(r, list):
		return v in r
	else:
		return v == r

def test_contains(r, v, options):

	if 'nocase' in options:
		r = to_lower(r)
		v = to_lower(v)

	if isinstance(r, list):
		for a in r:
			if a.find(v) >= 0:
				return True
		return False
	else:
		return r.find(v) >= 0

def test_startswith(r, v, options):

	if 'nocase' in options:
		r = to_lower(r)
		v = to_lower(v)

	if isinstance(r, list):
		for a in r:
			if a.startswith(v):
				return True
		return False
	else:
		return r.startswith(v)

def test_endswith(r, v, options):

	if 'nocase' in options:
		r = to_lower(r)
		v = to_lower(v)

	if isinstance(r, list):
		for a in r:
			if a.endswith(v):
				return True
		return False
	else:
		return r.endswith(v)

def matches_literal(meta, literal):

	## TODO: What to do on exceptions? Return False?

	## TODO: Are keys always lowercase, should we check?

	#
	#RYW
	# hack: the "path" attribute is causing problems.
	# it's frozen. it's not really used. and it causes stuff like:
	# a cloned object from a lecture to retain a "lecture" path
	# and so a search for lecture keeps turning up lesson plans and
	# stuff.
	#
	meta2 = meta.copy()
	if meta2 and meta2.has_key('path'):
		del meta2['path']

	try:
		key, operation_and_options, value = literal

		## print 'literal', literal

		if isinstance(operation_and_options, list):
			operation = operation_and_options[0]
			options   = operation_and_options[1:]
		else:
			operation = operation_and_options
			options = []
		operation = operation.lower()

                if operation.endswith(' eval_value'):
                    to_eval_value = True
                    operation = operation[:-(len(' eval_value'))]
                else:
                    to_eval_value = False

                if key == 'all_keys_concatenated':
                    real_value = ' '.join([str(v) for v in meta2.values()])
                else:
		    if meta2.has_key(key):
		        real_value = meta2[key]
		    else:
		        real_value = ''

		if operation == 'equals':
			return test_equals(real_value, value, options)

		if operation == 'contains':
			return test_contains(real_value, value, options)

		if operation == 'startswith':
			return test_startswith(real_value, value, options)

		if operation == 'endswith':
			return test_endswith(real_value, value, options)

		## Otherwise, just do an eval()
		if to_eval_value:
                    real_value = eval(real_value)
		expression = 'real_value %s value' % operation
		return eval(expression)
	except Exception, e:
		ryw.give_bad_news(
			'Exception in cnf_match.matches_literal',
			logging.error)
                #print '<P>Exception in cnf_match.matches_literal', str(e)
		return False



def matches_disjunction(meta, query):
    ## query is a list of literals
    ## at least one of them must match

    ryw.db_print2('matches_disjunction: query is: ' + repr(query), 53)
    
    for literal in query:
        ryw.db_print2('matches_disjunction: literal is: ' + repr(literal), 53)
	#
	# a "literal" is like:
	# ('all_keys_concatenated', ['contains', 'nocase'], 'lecture')
	#
        if matches_literal(meta, literal):
	    return True

    return False



def matches_cnf(meta, query):
	## meta is the meta-data dictionary
	## query is the cnf query
	## query is a list of conjuncts

	for conjunct in query:
		if not matches_disjunction(meta, conjunct):
			return False

	return True

def selftest():
	print 'Running selftest'
	meta = {}
	meta['a'] = 'hello'
	meta['b'] = 'world'
	meta['c'] = 1
	meta['d'] = 2
	meta['e'] = 3
	meta['f'] = 4
	meta['g'] = 'bello'
	meta['h'] = ['atta', 'pasta', 'astalavista']

	query1 = [\
			[('a', '==', 'gola'), ('b', '==', 'world')],\
			[('d', '>', 4), ('e', '<', 4)],\
		 ]
	assert matches_cnf(meta, query1) == True

	query2 = [\
			[('a', '==', 'gola'), ('b', '==', 'gola')],\
			[('d', '>', 4), ('e', '>', 4)],\
		 ]
	assert matches_cnf(meta, query2) == False

	query3 = [[('a', 'contains', 'hell')]]
	assert matches_cnf(meta, query3) == True

	query4 = [[('a', 'contains', 'Hell')]]
	assert matches_cnf(meta, query4) == False

	## The list form of operation. Can specify options like 'nocase'
	query5 = [[('a', ['contains', 'nocase'], 'Hell')]]
	assert matches_cnf(meta, query5) == True

	query6 = [[('h', ['startswith', 'nocase'], 'AsTa')]]
	assert matches_cnf(meta, query6) == True

	query7 = [[('h', ['startswith'], 'AsTa')]]
	assert matches_cnf(meta, query7) == False


	print 'Selftest successful'

if __name__ == '__main__':

	selftest()
