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
        if isinstance(value, ChessBlock):
            self.isCenter = value.isCenter
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
        self.nextBlockQueue = [ChessBlock(0, 2, data.Data(1, "a")) for i in range(2)]  # self.createNextBlock
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
        print(" ")
        for line in self.board:
            row = []
            for b in line:
                if b.isCenter:
                    row.append("Y")
                else:
                    row.append("N")
            print(row)
        print("==============")

    def sendBlock(self) -> bool:
        self.canGamerOperate = False

        didSend = False
        for y in range(self.size_y):
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
        if center.x < self.size_x - 1 and center.isSameWithBlock(self.board[center.y][center.x + 1]):
            nearbyCompateableBlock.append(self.board[center.y][center.x + 1])
        if 0 < center.y and center.isSameWithBlock(self.board[center.y - 1][center.x]):
            nearbyCompateableBlock.append(self.board[center.y - 1][center.x])
        if center.y < self.size_y - 1 and center.isSameWithBlock(self.board[center.y + 1][center.x]):
            nearbyCompateableBlock.append(self.board[center.y + 1][center.x])

        return nearbyCompateableBlock

    def _getNewCenterBlocks(self) -> list[ChessBlock]:
        return [x for y in self.board for x in y if x.isCenter]
    
    def checkChessboard(self) -> data.Event:
        # merge & fall，这必须是一个自递归的方法，因为每一步的操作都得反馈给UI那边做渲染，不然就是丢一个方块看不到过程只能看到结果
        # 因为是自递归的，不要想着一次性干完所有事情，而是只干一次，剩下的下次再干。每次干的结果都要反馈给UI那边
        # 要反馈的东西有两类，发生了聚合、发生了下坠
        
        # 只有新聚合出现的block才被标记为newCenter。
        # 检查有没有newCenter，有就聚合并把新聚合出来的标记成newCenter并擦除被聚合的
        checkResultEvent = data.Event("", [])

        # 1.先找找有没有fall的
        didFall = False
        for x in range(self.size_x):
            # 先看看有没有空，确定到底有没有fall
            columnInfo = [1 if self.board[y][x].value > 0 else 0 for y in range(self.size_y)]
            while columnInfo and columnInfo[-1] == 0:
                columnInfo.pop()
            if len(columnInfo) > sum(columnInfo):
                didFall

            # 再去执行fall
            columnData = [self.board[y][x] for y in range(self.size_y) if self.board[y][x].value != -1]
            for y in range(0, len(columnData)):
                self.board[y][x].update(columnData[y])
                self.board[y][x].isCenter = True

            self._erasureBlocks([self.board[y][x] for y in range(len(columnData), self.size_y)])
        
        if didFall:
            return data.Event("fall", [])

        # 2.再找找有没有聚合的
        newCenterBlocks = self._getNewCenterBlocks()
        if newCenterBlocks == None:
            return data.Event("", [])
        
        didNewCenterBlockMerged = []
        toMergeBlocks = []  # - todo: 这个是需要传回给前端的东西，告诉前端哪些block需要有聚合的动画
        for ncBlock in newCenterBlocks:
            nearbyCompateables = self._getNearbyCompateableBlocks(ncBlock)
            if len(nearbyCompateables) > 0:
                didNewCenterBlockMerged.append(1)
                mergedBlock = self.mergeBlocks(ncBlock, nearbyCompateables)
                self.board[ncBlock.y][ncBlock.x].update(mergedBlock)
                self.board[ncBlock.y][ncBlock.x].isCenter = True
                self._erasureBlocks(nearbyCompateables)
                ncBlock.isCenter = True

                toMergeBlocks.append([[ncBlock] + nearbyCompateables])
            else:
                didNewCenterBlockMerged.append(0)
                ncBlock.isCenter = False
            
        if sum(didNewCenterBlockMerged) == 0:
            didFinishCheck = True
        return data.Event("merge", toMergeBlocks)

    def checkChessboard_old(self) -> (bool, list[[ChessBlock]]):
        # merge & fall，这必须是一个自递归的方法，因为每一步的操作都得反馈给UI那边做渲染，不然就是丢一个方块看不到过程只能看到结果
        # 因为是自递归的，不要想着一次性干完所有事情，而是只干一次，剩下的下次再干。每次干的结果都要反馈给UI那边
        # 要反馈的东西有两类，发生了聚合、发生了下坠
        
        # 只有新聚合出现的block才被标记为newCenter。
        # 检查有没有newCenter，有就聚合并把新聚合出来的标记成newCenter并擦除被聚合的，
        newCenterBlocks = self._getNewCenterBlocks()
        if newCenterBlocks == None:
            return True, []

        # 1.merge
        didFinishCheck = False
        didNewCenterBlockMerged = []

        toMergeBlocks = []  # - todo: 这个是需要传回给前端的东西，告诉前端哪些block需要有聚合的动画
        for ncBlock in newCenterBlocks:
            nearbyCompateables = self._getNearbyCompateableBlocks(ncBlock)
            if len(nearbyCompateables) > 0:
                didNewCenterBlockMerged.append(1)
                mergedBlock = self.mergeBlocks(ncBlock, nearbyCompateables)
                self.board[ncBlock.y][ncBlock.x].update(mergedBlock)
                self.board[ncBlock.y][ncBlock.x].isCenter = True
                self._erasureBlocks(nearbyCompateables)
                ncBlock.isCenter = True
            else:
                didNewCenterBlockMerged.append(0)
                ncBlock.isCenter = False
            
        if sum(didNewCenterBlockMerged) == 0:
            didFinishCheck = True

        # 2.fall
        for x in range(self.size_x):
            columnInfo = [data.Data(self.board[y][x].value, self.board[y][x].rank) for y in range(self.size_y) if self.board[y][x].value != -1]
            for y in range(0, len(columnInfo)):
                self.board[y][x].update(columnInfo[y])

            self._erasureBlocks([self.board[y][x] for y in range(len(columnInfo), self.size_y)])

        return didFinishCheck, toMergeBlocks

    def mergeBlocks(self, center: ChessBlock, blocks: list[ChessBlock]) -> ChessBlock:
        mergedValue = (2 ** (len(blocks))) * center.value
        print(f"mergeBlocks value: {center.value}, {len(blocks)}, {mergedValue}")
        mergedData = data.Data(mergedValue, center.rank)
        if mergedValue > 10000:
            mergedData.value = mergedData.value / 1000
            mergedData.upgradeRank()

        mergedBlock = ChessBlock(center.y, center.x, mergedData)
        mergedBlock.isCenter = True

        return mergedBlock