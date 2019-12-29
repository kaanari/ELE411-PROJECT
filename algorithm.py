import time

add = lambda a,b: a+b
sub = lambda a,b: a-b
mul = lambda a,b: a*b
div = lambda a,b: a/b if a % b == 0 else 0/0

operations = [ (add, '+'),
               (mul, '*'),
               (sub, '-'),
               (div, '/')]

def elapsed(): # Calculate the elapsed time.
    return round(time.time() - started_time,2)

def Evaluate(stack): #  Evaluate function is checking the stack is equal to result.
    try:
        total = 0
        lastOper = add
        for item in stack:
            if type(item) is int:
                total = lastOper(total, item)
            else:
                lastOper = item[0]

        return total
    except:
        return 0

def ReprStack(stack): # Infix stack i print ediyor.
    reps = [ str(item) if type(item) is int else item[1] for item in stack ]
    return ' '.join(reps)

def Recurse(stack, nums,Target,Result):   # Recurse function contains our essential algorithm.
    global Counter          # Global Counter declared to identify how many times call Recurse Function.
    Counter +=1
    for n in range(len(nums)):
        stack.append(nums[n]) # Add number array elements to stack
        remaining = nums[:n] + nums[n+1:]   # Get remaining elements

        if Evaluate(stack) == Target: # If stack result equal to target.
            Result.append(ReprStack(stack))

        if len(remaining) > 0:
            for op in operations: # Add operators into the stack one by one
                stack.append(op)
                stack = Recurse(stack, remaining,Target,Result)
                stack = stack[:-1]

        stack = stack[:-1]
    return stack

def Solve(Target, Numbers): # Main Function to report some infos and call the Recursion Function.
    global Counter,started_time
    started_time = time.time()
    Counter = 0
    Result = []
    Recurse([], Numbers,Target,Result)
    return Result,elapsed(),Counter

