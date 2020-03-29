import pprint

class binary_group:
    """
    ビットの集合を持つ可換な加法群クラス
    """
    identity_element = 0

    def __init__(self, n_bits=8, signed=True):
        self.values = [0 for i in range(n_bits)]
        self.decimal_values = 0
        self.n_bits = n_bits
        self.signed = signed

        bit_range = (2**n_bits)
        if signed==True:
            self.max_num = int(bit_range/2)-1
            self.min_num = -int(bit_range/2)
        else:
            self.max_num = bit_range-1
            self.min_num = 0

    def __add__(self, other):
        """
        二項演算
        """
        res = binary_group(n_bits=self.n_bits,signed=self.signed)
        carry_bit = 0
        for i in range(self.n_bits)[::-1]:
            input_xor = self.values[i]^other.values[i]
            res.values[i] = input_xor^carry_bit
            carry_bit = (self.values[i]&other.values[i])|(input_xor&carry_bit)
        bit_range = (2**self.n_bits)
        if self.signed==True:
            res.decimal_values = (self.decimal_values+other.decimal_values+int(bit_range/2))%bit_range-int(bit_range/2)
        else:
            res.decimal_values = (self.decimal_values+other.decimal_values)%bit_range
        return res

    def __neg__(self):
        """
        逆元(単項演算)
        """
        if self.signed==True:
            part = [int(abs(self.decimal_values)/(2**(i)))%2 for i in range(self.n_bits-1)][::-1]
            for i,num in enumerate(part[::-1]):
                if num==1:
                    break
            self.values = [1^self.values[0]]+[1^p if j<self.n_bits-2-i else p for j,p in enumerate(part)]
            self.decimal_values = -self.decimal_values
            return self

    def tolist_binary_digits(self, decimal_num):
        if (self.min_num<=decimal_num) and (decimal_num<=self.max_num):
            if self.signed==True:
                part = [int(abs(decimal_num)/(2**(i)))%2 for i in range(self.n_bits-1)][::-1]
                if decimal_num>-1:
                    return [0]+part
                else:
                    for i,num in enumerate(part[::-1]):
                        if num==1:
                            break
                    return [1]+[1^p if j<self.n_bits-2-i else p for j,p in enumerate(part)]
            else:
                return [int(decimal_num/(2**(i)))%2 for i in range(self.n_bits)][::-1]
        else:
            print("Please check number range")

    def set_values(self, decimal_num):
        self.decimal_values = decimal_num
        self.values = self.tolist_binary_digits(decimal_num)

def delete_msb_group(group):
    """
    nビット群の最上位ビットを削除しn-1ビット群にする準同型写像
    """
    res = binary_group(n_bits=group.n_bits-1,signed=group.signed)
    if group.signed==True:
        if group.values[1]==1:
            res.decimal_values = group.decimal_values%-(2**(group.n_bits-1))
        else:
            res.decimal_values = group.decimal_values%(2**(group.n_bits-1))
        res.values = group.values[1:]
    return res

def shiftdown_group(group):
    """
    nビット軍をn-1ビット群にシフトダウンする準同型写像
    """
    res = binary_group(n_bits=group.n_bits-1,signed=group.signed)
    if group.signed==True:
        res.values = group.values[:1]+group.values[2:]
    else:
        res.values = group.values[1:]
    return res

def shiftup_group(group):
    """
    nビット軍をn+1ビット群にシフトアップする準同型写像
    """
    res = binary_group(n_bits=group.n_bits+1,signed=group.signed)
    if group.signed==True:
        res.values = group.values[:1]+group.values
    else:
        res.values = [0]+group.values
    res.decimal_values = group.decimal_values
    return res

if __name__ == "__main__":
    signed_group = binary_group(n_bits=8,signed=True)
    unsigned_group = binary_group(n_bits=8,signed=False)

    # print(signed_group.tolist_binary_digits(10))
    # print(signed_group.tolist_binary_digits(-5))
    # print(signed_group.tolist_binary_digits(-335))

    a = binary_group(n_bits=5,signed=True)
    b = binary_group(n_bits=5,signed=True)
    a.set_values(5)
    b.set_values(-9)

    c = a+b
    # print(c.values)
    # b.set_values(13)
    # print((c+b).values)
    # b = -b
    # print(b.values)

    f = delete_msb_group
    print(f(c).values)
    print((f(a)+f(b)).values)

    f = shiftup_group
    print(f(c).values)
    print((f(a)+f(b)).values)

    f = shiftdown_group
    print(f(c).values)
    print((f(a)+f(b)).values)

    # 群表のような準同型写像の条件成立表を作る
    truth_table = []
    a = binary_group(n_bits=4,signed=True)
    b = binary_group(n_bits=4,signed=True)
    for i in range(a.min_num,a.max_num+1):
        a.set_values(i)
        truth_row = []
        for j in range(b.min_num,b.max_num+1):
            b.set_values(j)
            truth_row.append(1 if f(a+b).values==(f(a)+f(b)).values else 0)
        truth_table.append(truth_row)
    pprint.pprint(truth_table)
