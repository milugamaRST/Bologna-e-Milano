#
# Common functions
#

import logging, datetime


class Numbers():
    # This static method ensures that a number has been entered, not a string. The function will only terminate if a number was entered...
    @staticmethod
    def inputInt(promptLine):
        repeatInput = True
        
        while repeatInput:
            inputValue = input(promptLine)
            try:
                return int(inputValue)
            except ValueError:
                print("The input was not a number. Please re-enter:")
                
    # this method return the result of a division between number (num) and denominator(denom), but limited to a max value of 10
    @staticmethod
    def limit10(num, denom):
        val = int(num / denom)
        
        if val > 10:
            return 10
        
        return val



class Common():
    # named singletons
    _Base_ = ''
    _Logger_ = None
    _Separator_ = '__'
    
    @staticmethod
    def getBase(prefix = ''):
        if Common._Base_ == '':
            Common._Base_ = prefix + Common._Separator_ + '{date:%Y%m%d%H%M%S}'.format(date=datetime.datetime.now())
            Common.createDirectory('.', Common._Base_)
        return Common._Base_
    
    @staticmethod
    def getLogger(name = 'default', prefix = ''):
        if Common._Logger_ == None:
            # create the logger
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)
            
            # create file handler
            fileHandler = logging.FileHandler(Common.getBase(prefix) + '/' + prefix + '.log')
            fileHandler.setLevel(logging.INFO)
            
            # create console handler
            consoleHandler = logging.StreamHandler()
            consoleHandler(logging.INFO)
            
            # create + add formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fileHandler.setFormatter(formatter)
            consoleHandler.setFormatter(formatter)
            
            logger.addHandler(fileHandler)
            logger.addHandler(consoleHandler)
            
            Common._Logger_ = logger
            
        return Common._Logger_