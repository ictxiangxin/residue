import sys
import time
import inspect
from residue.object import singleton

"""
    Common log tool
        - Logging script information to file.
        - Use GlobalLog() generate global(shared) log.
"""


class Log:
    def __init__(self, log_path: str=None, append: bool=False, buffer_size: int=0, level: int=2):
        self.__log_path_pointer = None
        self.__log_buffer = ""
        self.__append = append
        self.__buffer_size = buffer_size
        self.__level = level
        self.__log_path = None
        self.set_log_path(log_path)
        self.watch = self.flexible_watch(False, True)
        self.guard = self.flexible_watch(True, True)

    def _close_log_file(self):
        if self.__log_path_pointer is not None:
            self._write_back_buffer()
            self.__log_path_pointer.close()

    def _write_back_buffer(self):
        if self.__log_buffer:
            self.__log_path_pointer.write(self.__log_buffer)
            self.__log_buffer = ""

    def get_log_path(self):
        return self.__log_path

    def set_log_path(self, log_path: str):
        self._close_log_file()
        self.__log_path = log_path
        if self.__log_path:
            self.__log_path_pointer = open(log_path, 'a' if self.__append else 'w', encoding='utf-8')

    log_path = property(get_log_path, set_log_path)

    def get_append(self):
        return self.__append

    def set_append(self, append: bool):
        self.__append = append

    append = property(get_append, set_append)

    def get_buffer_size(self):
        return self.__buffer_size

    def set_buffer_size(self, buffer_size: int):
        self._write_back_buffer()
        self.__buffer_size = buffer_size

    buffer_size = property(get_buffer_size, set_buffer_size)

    def get_level(self):
        return self.__level

    def set_level(self, level: int):
        self.__level = level

    level = property(get_level, set_level)

    def log(self, log_object, log_level: int=0, line_number: int=None):
        if log_level > self.__level:
            return
        log_frame = inspect.currentframe().f_back
        log_code = log_frame.f_code
        caller = log_code.co_name
        filename = log_code.co_filename
        if caller in ['error', 'warning', 'info', 'exception'] and filename == log_frame.f_code.co_filename:
            log_frame = log_frame.f_back
            log_code = log_frame.f_code
            caller = log_code.co_name
            filename = log_code.co_filename
        function_line_number = log_code.co_firstlineno
        code_line_number = log_frame.f_lineno if line_number is None else line_number
        self._record(log_object, filename, function_line_number, caller, code_line_number)

    def _record(self, log_object, filename, function_line_number, caller, code_line_number):
        log_time = time.strftime('%Y-%m-%d %H:%M:%S')
        log_object_string = str(log_object)
        if "\n" in log_object_string:
            log_object_string = log_object_string.replace('\n', '\n\t')
            log_object_string = ''.join(['\n', log_object_string, '\n'])
        log_string = '{}\t{}\t[{} @ {}]\t<Line: {}>\t{}\n'.format(
            log_time, filename, caller, function_line_number, code_line_number, log_object_string)
        if self.__buffer_size > 1:
            self.__log_buffer = log_string
        else:
            self.__log_buffer += log_string
        if len(self.__log_buffer) >= self.buffer_size:
            if self.__log_path_pointer is not None:
                record_pointer = self.__log_path_pointer
            else:
                record_pointer = sys.stdout
            record_pointer.write(self.__log_buffer)
            record_pointer.flush()
            self.__log_buffer = ''

    def error(self, log_text: str):
        self.log('[ERROR] {}'.format(log_text), log_level=0)

    def exception(self, exception_text: str=None):
        exception_class, exception_message, exception_traceback = sys.exc_info()
        if exception_class is None or exception_traceback is None:
            return
        if exception_text is None:
            exception_text = '{}: {}'.format(exception_class.__name__, exception_message)
        self.log('[EXCEPTION] {}'.format(exception_text), line_number=exception_traceback.tb_lineno, log_level=0)

    def warning(self, log_text: str):
        self.log('[WARNING] {}'.format(log_text), log_level=1)

    def info(self, log_text: str):
        self.log('[INFO] {}'.format(log_text), log_level=2)

    def flexible_watch(self, protect, with_arguments):
        def _watch(function):
            def __watch(*args, **kwargs):
                log_frame = inspect.currentframe().f_back
                log_code = log_frame.f_code
                caller = log_code.co_name
                filename = log_code.co_filename
                function_line_number = log_code.co_firstlineno
                code_line_number = log_frame.f_lineno
                if with_arguments:
                    arguments = ', '.join(str(arg) for arg in args) + \
                                ', '.join('{}={}'.format(key, value) for key, value in kwargs.items())
                else:
                    arguments = ''
                start_time = time.time()
                try:
                    function_return = function(*args, **kwargs)
                except:
                    exception_class, exception_message, exception_traceback = sys.exc_info()
                    exception_frame = exception_traceback.tb_next.tb_frame
                    exception_code = exception_frame.f_code
                    exception_caller = exception_code.co_name
                    exception_filename = exception_code.co_filename
                    exception_function_line_number = exception_code.co_firstlineno
                    exception_code_line_number = exception_frame.f_lineno
                    exception_text = '{}: {}'.format(exception_class.__name__, exception_message)
                    self._record('[EXCEPTION] {}'.format(exception_text),
                                 exception_filename,
                                 exception_function_line_number,
                                 exception_caller,
                                 exception_code_line_number)
                    if not protect:
                        raise
                    end_time = time.time()
                    pass_time = end_time - start_time
                    log_text = '[WATCH] <FAIL> {:.2f}ms {}({})'.format(pass_time, function.__name__, arguments)
                    function_return = None
                else:
                    end_time = time.time()
                    pass_time = end_time - start_time
                    log_text = '[WATCH] <OK> {:.2f}ms {}({})'.format(pass_time, function.__name__, arguments)
                self._record(log_text, filename, function_line_number, caller, code_line_number)
                return function_return
            return __watch
        return _watch

    def message(self, message_text: str):
        def _message(function):
            def __message(*args, **kwargs):
                log_frame = inspect.currentframe().f_back
                log_code = log_frame.f_code
                caller = log_code.co_name
                filename = log_code.co_filename
                function_line_number = log_code.co_firstlineno
                code_line_number = log_frame.f_lineno
                self._record(message_text, filename, function_line_number, caller, code_line_number)
                return function(*args, **kwargs)
            return __message
        return _message


"""
    Global log tool
        - Generate singleton log as global log.
"""


@singleton
class GlobalLog(Log):
    pass
