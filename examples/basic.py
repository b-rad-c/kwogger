import kwogger


def main():
    kwogger.configure(__name__)
    logger = kwogger.log(__name__)

    # basic
    logger.info('Sample message')

    # key values
    logger.info('Sample message', key1='hello', key2='world')

    # various data types in key values
    logger.info('Sample message', a=None, b=True, c=1, d=1.1, e='string', f=open)

    x, y = 1, 0
    try:
        z = x / y
    except ZeroDivisionError:
        # automatically gets exception data and traceback from sys module
        logger.error_exc('Problem dividing', x=x, y=y)


if __name__ == '__main__':
    main()
