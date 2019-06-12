import inspect
import os


def addInfoLog(log_msg='', src=''):
    if log_msg.strip() != '':
        if not src:
            src = os.path.basename(inspect.stack()[1][1]).strip('.py')
        print 'Info Log in {src}. MSG: {msg}'.format(src='{0}.{1}'.format(src, inspect.stack()[1][3]), msg=log_msg)


def addExceptionLog(log_msg='', src=''):
    if log_msg.strip() != '':
        if not src:
            src = os.path.basename(inspect.stack()[1][1]).strip('.py')
        print 'Exception in {src}. MSG: {msg}'.format(src='{0}.{1}'.format(src, inspect.stack()[1][3]), msg=log_msg)


def addLogToCL(log_msg='', src='', new_line=True):
    if log_msg.strip() != '':
        if new_line:
            print src, log_msg
        else:
            print src, log_msg,
