from functools import wraps
import time
from django.http import HttpResponseBadRequest, HttpResponseForbidden

def user_is_active(view_func):
    @wraps(view_func)
    def _decorator(self, request, *args, **kwargs):
        print(request.user)
        if not request.user.is_active: 
            return HttpResponseForbidden("Sua conta está desativada.")
        
        return view_func(self, request, *args, **kwargs)
    
    return _decorator


def user_is_superuser(view_func):
    @wraps(view_func)
    def _decorator(self, request, *args, **kwargs):
        print(request.user)
        if not request.user.is_superuser: 
            return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
        
        return view_func(self, request, *args, **kwargs)
    
    return _decorator


def log_db_queries ( f ) :
    """
    verificar a velocidade do redis
    """
    from django.db import connection
    def new_f ( * args , ** kwargs ) :
        start_time = time.time()
        res = f ( * args , ** kwargs )
        print ( "\n\n" )
        print ( "-"*80 )
        print ("db queries log for %s:\n" % (f.__name__))
        print ( " TOTAL COUNT : % s " % len ( connection.queries ) )
        for q in connection.queries :
            print ("%s: %s\n" % (q["time"] , q["sql"]))
        end_time = time.time ()
        duration = end_time - start_time
        print ('\n Total time: {:.3f} ms'.format(duration * 1000.0))
        print ("-"*80)
        return res
    return new_f