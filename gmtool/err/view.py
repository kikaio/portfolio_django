from django.shortcuts import render, reverse, redirect

ERR_ROOT = 'gmtool/err'

def render_err(req, tmeplate_name:str='', context:dict = {}):
	return render(req, f'{ERR_ROOT}/{tmeplate_name}', context)


def bad_req(req):
	return render_err(req, 'bad_req.html')
pass

def not_found(req):
	return render_err(req, 'not_found.html')
pass

