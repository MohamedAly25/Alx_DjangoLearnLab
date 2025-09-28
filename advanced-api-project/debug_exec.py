import pathlib, sys, inspect
p = pathlib.Path(__file__).resolve().parent / 'api' / 'tests.py'
src = p.read_text(encoding='utf-8')
ns = {}
try:
    exec(compile(src, str(p), 'exec'), ns)
    print('EXEC OK')
    names = [k for k in ns.keys() if not k.startswith('__')]
    print('names:', names)
    if 'BookViewTests' in ns:
        cls = ns['BookViewTests']
        print('BookViewTests is class:', inspect.isclass(cls))
        methods = [n for n,_ in inspect.getmembers(cls, inspect.isfunction) if n.startswith('test')]
        print('test methods:', methods)
    else:
        print('BookViewTests not found in exec namespace')
except Exception as e:
    print('EXCEPTION:', type(e).__name__, e)
    import traceback; traceback.print_exc()
