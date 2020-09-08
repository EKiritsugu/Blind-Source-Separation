def matToArray(M):#对于所有的乱七八糟的都可以处理一下，将matrix格式转化为array格式
    try:
        M0=M.A
    except:
        M0=M
    finally:
        return M0