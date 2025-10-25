from __future__ import annotations  # 因为ChessBlock类需要在未完成定义前引用自己，所以用了这个语法糖
import data

class ChessBlock:
    def __init__(self, y, x, initValue: data.Data):
        self.y = y
        self.x = x

        self.value = initValue.value  # -1表示这是个空的block
        self.rank = initValue.rank
        self.color = initValue.color

        self.isCenter = False

        # -todo： 还没理清楚，这个东西要clear状态在什么地方clear
        self.mergeVector = -1  # 1, 2, 3，左上右，标识这个block如果要发生聚合的话是往哪个方向聚合

    def update(self, value: data.Data | ChessBlock):
        self.value = value.value
        self.rank = value.rank
        self.color = value.color

    def getText(self) -> str:
        if self.value == -1:
            return ""

        return f"{round(self.value)}{self.rank}"

    def isSameWithBlock(self, block) -> bool:
        if block.value == self.value and block.rank == self.rank:
            return True
        return False

class Chessboard:
    def __init__(self):

        self.dataAlgorithm = data.DataAlgorithm()

        # load save
        gameSave = [line.strip().split(",") for line in open("./gameSave.csv", "r")]

        self.size_y = len(gameSave)  # 7行，每行5列
        self.size_x = len(gameSave[0])

        self.currentBlockRange = self.dataAlgorithm.getDataRange(gameSave)

        # 注意：board最后有一行是隐形的，如果到顶了，相同的色块照样往下合并，不同的就直接gg
        self.board = [[ChessBlock(y, x, self.dataAlgorithm.translateStrToData(gameSave[y][x])) for x in range(self.size_x)] for y in range(self.size_y)]
        self.board.append([ChessBlock(self.size_y, x, data.Data(-1, "")) for x in range(self.size_x)])

        # - todo: 这里应该是持续地生成nextBlockQueue的内容，现在只是放进去了测试的内容
        self.nextBlockQueue = [ChessBlock(0, 2, data.Data(333, "i")) for i in range(2)]  # self.createNextBlock
        self.slot = [ChessBlock(0, i, data.Data(-1, "")) for i in range(5)]
        self.slot[2] = self.nextBlockQueue[0]
        self.nextBlockSlotIndex = 2

        self.canGamerOperate = True

    def _createNextBlock(self):
        # 创建新的block塞到self.nextBlockQueue最后，然后把最前面的踢掉
        pass

    def printBoard(self):
        for line in self.board:
            print([b.getText() for b in line])
        print("==============")

    def sendBlock(self) -> bool:
        self.canGamerOperate = False

        didSend = False
        for y in range(self.size_y):
            # 完犊子又他妈是倒着来的……
            if self.board[y][self.nextBlockSlotIndex].value == -1:
                self.board[y][self.nextBlockSlotIndex].update(self.slot[self.nextBlockSlotIndex])
                self.board[y][self.nextBlockSlotIndex].isCenter = True
                didSend = True
                break

        self.slot[self.nextBlockSlotIndex] = ChessBlock(0, self.nextBlockSlotIndex, data.Data(-1, ""))

        self._createNextBlock()
        self.slot[2] = self.nextBlockQueue[0]
        self.nextBlockSlotIndex = 2

        self.canGamerOperate = True

        return didSend

    def moveSlot(self, key: str):
        self.canGamerOperate = False
        if key == "a" or key == "arrow left":
            self.slot = self.slot[1:] + [self.slot[0]]
            if self.nextBlockSlotIndex == 0:
                self.nextBlockSlotIndex = self.size_x - 1
            else:
                self.nextBlockSlotIndex -= 1
        elif key == "d" or key == "arrow right":
            self.slot = [self.slot[-1]] + self.slot[:-1]
            self.nextBlockSlotIndex = (self.nextBlockSlotIndex + 1) % self.size_x
        self.canGamerOperate = True

    def _erasureBlocks(self, blocks: list[ChessBlock]):
        for b in blocks:
            self.board[b.y][b.x].value = -1
            self.board[b.y][b.x].rank = ""
            self.board[b.y][b.x].color = "#B5B5B5"
            self.board[b.y][b.x].mergeVector = -1
        # self.updateView()

    def _erasureMergedBlocks(self, mergeCenter: ChessBlock, blocks: list[ChessBlock]):
        '''这个方法和_erasureBlocks的区别在于，会更新mergeVector然后擦除其他的信息'''

        def getRelativeDirection(s: [int], e: [int]) -> int:
            if s[0] == e[0]:
                if s[1] == e[1] - 1:
                    return 3
                elif s[1] == e[0] + 1:
                    return 1
            elif s[1] == e[1] and s[0] == e[0] + 1:
                return 2
            return -1

        for b in blocks:
            self.board[b.y][b.x].value = -1
            self.board[b.y][b.x].rank = ""
            self.board[b.y][b.x].color = "#B5B5B5"

            self.board[b.y][b.x].mergeVector = getRelativeDirection([b.y, b.x], [mergeCenter.y, mergeCenter.x])

    def _getNearbyCompateableBlocks(self, center: ChessBlock) -> list[ChessBlock]:
        '''
        把中心block周围相同值的block都给找出来
        '''
        nearbyCompateableBlock = []

        if 0 < center.x and center.isSameWithBlock(self.board[center.y][center.x - 1]):
            nearbyCompateableBlock.append(self.board[center.y][center.x - 1])
        if center.x < self.size_x and center.isSameWithBlock(self.board[center.y][center.x + 1]):
            nearbyCompateableBlock.append(self.board[center.y][center.x + 1])
        if 0 < center.y and center.isSameWithBlock(self.board[center.y - 1][center.x]):
            nearbyCompateableBlock.append(self.board[center.y - 1][center.x])
        if center.y < self.size_y and center.isSameWithBlock(self.board[center.y + 1][center.x]):
            nearbyCompateableBlock.append(self.board[center.y + 1][center.x])

        return nearbyCompateableBlock

    def _getNewCenterBlocks(self) -> list[ChessBlock]:
        newCenterBlocks = []
        for y in self.board:
            for x in y:
                if x.isCenter:
                    newCenterBlocks.append(x)

        return newCenterBlocks

    def checkChessboard(self) -> (bool, list[ChessBlock]):
        # merge-fall
        newCenterBlocks = self._getNewCenterBlocks()
        if len(newCenterBlocks) == 0:
            return False, []

        # 1.merge
        didFinishCheck = False
        toMergeBlocks = []
        for ncBlock in newCenterBlocks:
            nearbyCompateables = self._getNearbyCompateableBlocks(ncBlock)
            if len(nearbyCompateables) > 0:
                # -todo: 捋一捋这里面的逻辑啊，瞎写的
                mergedBlock = self.mergeBlocks(ncBlock, nearbyCompateables)
                self.board[ncBlock.y][ncBlock.x].update(mergedBlock)
                self._erasureBlocks(nearbyCompateables)

        # 2.fall

        return didFinishCheck, toMergeBlocks


    def mergeBlockData(self, blockData: data.Data, count: int) -> data.Data:
        mergedValue = (2 ** (count - 1)) * blockData.value

        mergedData = data.Data(mergedValue, blockData.rank)
        if mergedValue > 10000:
            mergedData.value = mergedData.value / 1000
            mergedData.upgradeRank()

        return mergedData

    def mergeBlocks(self, center: ChessBlock, blocks: list[ChessBlock]) -> ChessBlock:
        '''
        计算一下这几个block聚合之后落到哪里。聚合成什么Data的事情这里不用管
        :param blocks:
        :param count:
        :return: Data
        '''

        # 这个method应该跟mergeBlockData()合并成一个的……

        pass