class Node:
    def __init__(self, value, priority):
        self.value = value
        self.priority = priority


class PQ:
    def __init__(self):
        self.values = []
    
    def enqueue(self, value, priority):
        newNode = Node(value, priority)
        self.values.append(newNode)
        index = len(self.values) - 1
        parentIndex = (index - 1) // 2
        while parentIndex >= 0:
            if(self.values[parentIndex].priority <= self.values[index].priority): break
            self.values[parentIndex], self.values[index] = self.values[index], self.values[parentIndex]
            index = parentIndex
            parentIndex = (index - 1) // 2
    
    def dequeue(self):
        if len(self.values) == 0: return None
        root = self.values[0]
        end = self.values.pop()
        if len(self.values) > 0:
            self.values[0] = end
            idx = 0
            length = len(self.values)
            sinkNode = self.values[0]
            while True:
                leftNodeIdx = 2*idx + 1
                rightNodeIdx = 2*idx + 2
                swap = None
                if leftNodeIdx < length:
                    leftNode = self.values[leftNodeIdx]
                    if leftNode.priority < sinkNode.priority:
                        swap = leftNodeIdx
                if rightNodeIdx < length:
                    rightNode = self.values[rightNodeIdx]
                    if((swap == None and rightNode.priority < sinkNode.priority) or (swap != None and rightNode.priority < leftNode.priority)):
                        swap = rightNodeIdx
                if swap == None: break
                self.values[idx] = self.values[swap]
                self.values[swap] = sinkNode
                idx = swap
        return root.value
