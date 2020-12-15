class Luhn:
    """Implementation of Luhn Algorithm

    **Example
    >>> luhn = Luhn()
    >>> cardNumber = luhn.create(accountNumber='400000945529612')
    >>> cardNumber
    '4000009455296122'
    >>> luhn.validate(cardNumber=cardNumber)
    True
    """

    # using Pointer Technique to reduce time complexity and space complexity
    # Time: O(n)
    # Space: O(1)
    @staticmethod
    def create(accountNumber) -> str:
        accountNumber_List = [int(char) for char in accountNumber]

        i = 0
        while i <= len(accountNumber_List):
            if i % 2 == 0:
                accountNumber_List[i] *= 2
            i += 1

        i = 0
        while i < len(accountNumber_List):
            if accountNumber_List[i] > 9:
                accountNumber_List[i] -= 9
            i += 1

        if sum(accountNumber_List) % 10 == 0:
            checkSum = 0
        else:
            checkSum = 10 - sum(accountNumber_List) % 10

        return accountNumber + str(checkSum)

    @staticmethod
    def validate(cardNumber: str) -> bool:
        cardNumber_list = [int(char) for char in cardNumber]
        checkSum = cardNumber_list.pop()

        # find the control number
        i = 0
        while i < len(cardNumber_list):
            if i % 2 == 0:
                cardNumber_list[i] *= 2
            i += 1

        i = 0
        while i < len(cardNumber_list):
            if cardNumber_list[i] > 9:
                cardNumber_list[i] -= 9
            i += 1

        controlNumber = sum(cardNumber_list)

        return (controlNumber + checkSum) % 10 == 0
