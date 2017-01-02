import sys
import time
import inspect


class Log:
    def __init__(self, log_path: str=None, append: bool=False, buffer_size: int=0, level: int=2):
        self.__log_path_pointer = None
        self.__log_buffer = ""
        self.__append = append
        self.__buffer_size = buffer_size
        self.__level = level
        self.__log_path = None
        self.set_log_path(log_path)

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
        log_time = time.strftime('%Y-%m-%d %H:%M:%S')
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
        log_object_string = str(log_object)
        if "\n" in log_object_string:
            log_object_string = log_object_string.replace('\n', '\n\t')
            log_object_string = ''.join(['\n', log_object_string, '\n'])
        log_string = '{}\t{}\t[{}: {}]\t<{}>\t{}\n'.format(
            log_time, filename, function_line_number, caller, code_line_number, log_object_string)
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

    def warning(self, exception_text: str):
        self.log('[WARNING] {}'.format(exception_text), log_level=1)

    def info(self, exception_text: str):
        self.log('[INFO] {}'.format(exception_text), log_level=2)
