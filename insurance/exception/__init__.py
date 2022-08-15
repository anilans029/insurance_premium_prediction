import os
import sys

class InsuranceException(Exception):

    def __init__(self,error_message:Exception, error_detail: sys):
        super().__init__(error_message)
        self.error_message= InsuranceException.get_detailed_error_message(error_message=error_message,
                                                                        error_detail=error_detail)

    @staticmethod
    def get_detailed_error_message(error_message:Exception, error_detail: sys)->str:
        """
        The get_detailed_error_message function accepts an error message and a traceback object as input. 
        It returns a detailed error message that includes the file name, line number, and original error message.

        :param error_message:Exception: Get the error message that was thrown by python
        :param error_detail:sys: Get the error message and line number

        :return: A detailed error message

        :doc-author: anil
        """

        _,_,exec_tb = error_detail.exc_info()

        exception_block_line_number = exec_tb.tb_frame.f_lineno
        try_block_line_number = exec_tb.tb_lineno
        file_name = exec_tb.tb_frame.f_code.co_filename
        error_message = f"""
        Error occured in script: 
        [ {file_name} ] at 
        try block line number: [{try_block_line_number}] and exception block line number: [{exception_block_line_number}] 
        error message: [{error_message}]
        """
        return error_message

    def __str__(self):
        return self.error_message

    def __repr__(self) -> str:
        return InsuranceException.__name__.str()